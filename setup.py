from setuptools import setup, find_packages

setup(
    name='json2viz',  # <--- CHANGED: Package name is now 'json2viz'
    version='0.1.0',
    packages=find_packages(), 
    install_requires=[
        'pandas',
    ],
    entry_points={
        # This creates the command-line script 'json2viz'
        'console_scripts': [
            'json2viz=json2viz.cli:main', # <--- CHANGED: Command name is 'json2viz' and references the 'json2viz' package
        ],
    },
    # Metadata for PyPI
    author='Robert Kiss', 
    description='A utility to flatten JSON and JSONL files into a tabular format for visualization.',
    url='https://github.com/Nagoyashi/json2viz', # <--- CHANGED: Updated URL to match your repo name
)