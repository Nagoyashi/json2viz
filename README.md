json2viz

A lightweight Python command-line utility for converting nested JSON or JSON Lines (JSONL/NDJSON) data into a flattened, tabular CSV format suitable for inspection, visualization, or easy conversion to other formats.

🚀 Key Features

Flattening: Uses pandas.json_normalize to automatically flatten nested objects into columns using a custom separator (default: __).

JSONL Support: Automatically detects and loads JSON Lines files.

CSV Output: Natively supports saving the flattened table to a CSV file using the --output flag.

Data Cleaning: Cleans cells to remove unsafe control characters and stringifies complex objects (like nested lists/dicts) to ensure compatibility with tabular outputs.

📦 Installation

Since this project is designed as a command-line tool, it's installed directly from the source repository.

Prerequisites

You need Python 3.6+ and pip installed.

Install the Tool

Colleagues can install the tool using one simple command that pulls directly from GitHub:

pip install git+[https://github.com/Nagoyashi/json2viz.git](https://github.com/Nagoyashi/json2viz.git)


💡 Usage

The tool takes a single required argument: the path to your input JSON or JSONL file.

Basic Syntax

json2viz <INPUT_FILE> [OPTIONS]


Key Examples

The tool supports two primary modes: displaying data for quick inspection, or saving the output for visualization.

Goal

Command

Output Behavior

Quick View (Default)

json2viz data.json

Displays the first 10 rows of the flattened data in the terminal.

Save to CSV (Auto)

json2viz data.json -o

Saves all data to ~/Downloads/data_flat.csv. This is the recommended mode for visualization.

Save to Specific Path

json2viz data.json -o output/report.csv

Saves all data to the specified CSV file path.

Custom Separator

json2viz survey.json --sep . -o

Keys are flattened using a dot (.), e.g., user.id instead of user__id.

Show All Rows in Terminal

json2viz data.json -n 0

Displays all records directly in the terminal (useful for smaller files).

Command-Line Arguments

Argument

Description

Default

INPUT.json

Path to the input JSON or JSON Lines file.

(Required)

--sep

Separator used to join nested keys (e.g., user__id).

__

-n, --rows

Number of rows to display when not saving to a file.

10

-o, --output

Optional. Path to output CSV file. If used without a path, saves to ~/Downloads/<input_name>_flat.csv.

(Display mode)

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.