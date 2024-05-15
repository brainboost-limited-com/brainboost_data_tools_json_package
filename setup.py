from setuptools import setup, find_packages

setup(
    name='brainboost_data_tools_json_package',  # Replace 'my_package' with your package name
    version='1.0.0',  # Replace with your package version

    author='Pablo Tomas Borda',
    author_email='pablotomasborda@hotmail.com',

    description='Processes JSon data',

    # Define your package's main content directory
    packages=find_packages(),

    # Specify package dependencies
    install_requires=[
        'json',  # Example dependency with version requirement
        'mocker'
        # Add more dependencies as needed
    ],



    # Optional: Define additional project URLs
    project_urls={
        'Source': 'https://github.com/your_username/my_package',  # Replace with your repository URL
    },
)
