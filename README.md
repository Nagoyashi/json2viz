# json2viz

A lightweight Python command-line utility for converting nested JSON or JSON Lines (JSONL/NDJSON) data into a flattened, tabular CSV format suitable for inspection, visualization, or easy conversion to other formats.

# 🚀 Key Features

1. Flattening: Uses pandas.json_normalize to automatically flatten nested objects into columns using a custom separator (default: __).

2. JSONL Support: Automatically detects and loads JSON Lines files.

3. CSV Output: Natively supports saving the flattened table to a CSV file using the --output flag.

4. Data Cleaning: Cleans cells to remove unsafe control characters and stringifies complex objects (like nested lists/dicts) to ensure compatibility with tabular outputs.

# 📦 Installation

Since this project is designed as a command-line tool, it's installed directly from the source repository.

## Prerequisites

You need Python 3.6+ and pip installed.

## Install the Tool

Colleagues can install the tool using one simple command that pulls directly from GitHub:

pip install git+[https://github.com/Nagoyashi/json2viz.git](https://github.com/Nagoyashi/json2viz.git)


# 💡 Usage

The tool takes a single required argument: the path to your input JSON or JSONL file.

## Basic Syntax

json2viz <INPUT_FILE> [OPTIONS]


## Key Examples (List Format for Easy Copying)

The tool supports two primary modes: displaying data for quick inspection, or saving the output for visualization.

### Quick View (Default):

Goal: Displays the first 10 rows of the flattened data in the terminal.

Command: json2viz data.json

### Save to CSV (Auto):

Goal: Saves all data to a CSV file in your Downloads folder. This is the recommended mode for visualization.

Command: json2viz data.json -o

Output Behavior: File is saved as ~/Downloads/data_flat.csv.

### Save to Specific Path:

Goal: Saves all data to a specified CSV file path.

Command: json2viz data.json -o output/report.csv

### Custom Separator:

Goal: Keys are flattened using a dot (.), e.g., user.id instead of user__id.

Command: json2viz survey.json --sep . -o

### Show All Rows in Terminal:

Goal: Displays all records directly in the terminal (useful for smaller files).

Command: json2viz data.json -n 0


## Command-Line Arguments (List Format for Easy Copying)

### INPUT.json

Description: Path to the input JSON or JSON Lines file.

Default: (Required)

### --sep

Description: Separator used to join nested keys (e.g., user__id).

Default: __

### -n, --rows

Description: Number of rows to display when not saving to a file.

Default: 10

### -o, --output

Description: Optional. Path to output CSV file. If used without a path, saves to ~/Downloads/<input_name>_flat.csv.

Default: (Display mode)

# 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.