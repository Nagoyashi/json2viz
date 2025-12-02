# json2viz

A lightweight Python command-line utility for converting nested JSON or JSON Lines (JSONL/NDJSON) data into a flattened, tabular CSV format suitable for inspection, visualization, or easy conversion to other formats.

## 🚀 Key Features

* **Flattening:** Uses `pandas.json_normalize` to automatically flatten nested objects into columns using a custom separator (default: `__`).
* **JSONL Support:** Automatically detects and loads JSON Lines files.
* **CSV Output:** Natively supports saving the flattened table to a CSV file using the `--output` flag.
* **Data Cleaning:** Cleans cells to remove unsafe control characters and stringifies complex objects (like nested lists/dicts) to ensure compatibility with tabular outputs.

## 📦 Installation

Since this project is designed as a command-line tool, your colleagues can install it directly from your GitHub repository using `pip`.

### Prerequisites

You need Python 3.6+ and pip installed.

### Install the Tool

```bash
pip install git+[https://github.com/Nagoyashi/json2viz.git](https://github.com/Nagoyashi/json2viz.git)