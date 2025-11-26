from setuptools import setup, find_packages

setup(
    name='json2csv',
    version='0.1.0', # Start with 0.1.0 and increment for future updates
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    entry_points={
        # This creates the command-line script 'json2csv'
        'console_scripts': [
            'json2csv=json2csv.cli:main',
        ],
    },
    # Metadata for PyPI (Optional, but good practice)
    author='Robert Kiss', 
    description='A utility to flatten JSON and JSONL files into CSV format.',
    url='https://github.com/YourGitHubUsername/json2csv', # Replace with your GitHub URL
)