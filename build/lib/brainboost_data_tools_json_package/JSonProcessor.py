import json
import os
from datetime import datetime
from tinydb import TinyDB, where
from alive_progress import alive_bar

class JSonProcessor:

    def __init__(self):
        self.my_db = None

    def load_json_files_recursively(self, from_path):
        merged_json_array = []  # List to store merged JSON arrays

        # Walk through the directory tree recursively
        for root, dirs, files in os.walk(from_path):
            for filename in files:
                if filename.endswith('.json'):  # Check if the file is a JSON file
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'r') as json_file:
                            # Load JSON content from the file
                            json_data = json.load(json_file)
                            if isinstance(json_data, list):
                                # If the loaded JSON data is a list, extend the merged array
                                merged_json_array.extend(json_data)
                            else:
                                # If the loaded JSON data is not a list, append it to the merged array
                                merged_json_array.append(json_data)
                    except Exception as e:
                        print(f"Error loading JSON file '{file_path}': {e}")

        return merged_json_array

    def collect_values_of_particular_key_to_set(self, json_array, key):
        values_set = set()

        for item in json_array:
            if key in item:
                values_set.add(item[key])

        return values_set

    def write(self, json_data, output_file_path=None):

        def generate_default_filename():
            # Get the name of the last folder in the current directory path
            last_folder_name = os.path.basename(os.getcwd())

            # Generate filename with current timestamp
            timestamp = datetime.now().strftime('%Y%m%d%H%M')
            default_filename = f"{last_folder_name}-{timestamp}.json"

            return default_filename

        if output_file_path is None:
            # Generate default filename based on the last folder of the path and current timestamp
            output_file_path = generate_default_filename()

        try:
            with open(output_file_path, 'w') as output_file:
                json.dump(json_data, output_file, indent=4)
            return True
        except Exception as e:
            print(f"Error writing JSON data to file '{output_file_path}': {e}")
            return False

    def add_calculated_field_to_the_objects_from_an_array(self, records, field_name, calculation_func):
        # Iterate over each record in the array
        for record in records:
            # Apply the calculation function to compute the value for the new field
            calculated_value = calculation_func(record)
            # Add the calculated value as a new field to the record
            record[field_name] = calculated_value

        # Return the updated list of records with the new field added
        return records

    def write_to_json_file(self, data, output_file):

        try:
            with open(output_file, 'w') as file:
                json.dump(data, file, indent=4)  # Serialize data to JSON and write to file
            print(f"Data successfully written to {output_file}")
        except Exception as e:
            print(f"Error occurred while writing to {output_file}: {e}")

    def to_tinydb(self, from_path, to_tinydb_json_file, log=False):
        if self.my_db is None:
            self.my_db = TinyDB(to_tinydb_json_file)

        json_array = self.load_json_files_recursively(from_path=from_path)
        existing_count = len(self.my_db.all())

        if log:
            print('Amount of elements to insert: ' + str(len(json_array) - existing_count))

        counter_log = existing_count
        total_to_process = len(json_array)
        index = existing_count
        print('Starting from the last processed element: ' + str(index))
        print('CData' + str(json_array[index]))

        with alive_bar(total=total_to_process - index, title='Inserting') as bar:
            bar(index)  # Set the initial value of the bar to the starting index
            for i in range(index, total_to_process):
                self.my_db.insert(json_array[i])
                bar()
                if counter_log % 1000 == 0:
                    print('Processed ' + str(counter_log) + ' elements. Continue...')
                counter_log += 1

        return self.my_db
