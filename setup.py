from setuptools import setup, find_packages

setup(
    # --- Identification ---
    name='json2viz',
    version='0.1.0',
    description='A utility to flatten nested JSON/JSONL data into a flat table for visualization.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Nagoyashi/json2viz',
    author='Robert Kiss',
    
    # --- Dependencies and Code ---
    packages=find_packages(), # Automatically finds the 'json2viz' folder with __init__.py
    install_requires=[
        'pandas',
    ],
    
    # --- Entry Point ---
    entry_points={
        # This defines the command your colleagues will run in the terminal:
        'console_scripts': [
            'json2viz=json2viz.cli:main', 
        ],
    },
    
    # --- Classifier Metadata (Optional, but good for publishing) ---
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    python_requires='>=3.6', # Specify minimum required Python version
)