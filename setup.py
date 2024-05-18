from setuptools import setup, find_packages

setup(
    name='brainboost_data_tools_json_package',
    version='1.0.0',
    author='Pablo Tomas Borda',
    author_email='pablotomasborda@hotmail.com',
    description='Processes JSON data',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'mocker',  # Example dependency
        # Add more dependencies as needed
    ],
    project_urls={
        'Source': 'https://github.com/your_username/my_package',  # Replace with your repository URL
    },
)
