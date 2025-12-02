#!/usr/bin/env python3
"""
json2viz — Convert JSON (or JSON Lines) to a flat table and display/save it.

This script flattens deeply nested JSON structures (common in API responses)
into a single, wide, tabular DataFrame, suitable for analysis and visualization.

Usage:
  # To display the first 10 rows in the terminal:
  # json2viz INPUT.json

  # To save all rows to a CSV file in the Downloads folder:
  # json2viz INPUT.json -o
"""

import argparse
import json
import re
import sys
from pathlib import Path
import pandas as pd
from pandas import json_normalize
import os 
# Although os is imported, we rely on pathlib.Path.home() for portability, 
# which is generally preferred for path manipulation.


# --- Utility Functions: Data Cleaning and Loading ---

# Regex pattern to identify characters illegal in CSV/Excel/OpenPyXL formats.
ILLEGAL = re.compile(r"[\x00-\x08\x0B-\x1F\x7F]")


def clean_cell(v):
    """
    Sanitizes values to ensure they are safe for CSV/Excel export.

    1. Stringifies complex types (lists/dicts) into JSON strings.
    2. Removes illegal control characters and normalizes newlines in strings.
    
    Args:
        v: The cell value (string, list, dict, number, etc.).
    Returns:
        The cleaned, CSV-safe value.
    """
    if isinstance(v, (dict, list)):
        # If the cell contains a nested structure, serialize it to a JSON string
        # to ensure it occupies a single, safe cell in the table.
        try:
            return json.dumps(v, ensure_ascii=False)
        except Exception:
            return str(v)
    if isinstance(v, str):
        # Normalize newlines to universal line feeds and remove characters 
        # (like NULL, vertical tab) that break older CSV/Excel parsers.
        v = v.replace("\r\n", "\n").replace("\r", "\n")
        v = ILLEGAL.sub("", v)
        return v
    return v


def load_json_any(path: Path):
    """
    Loads JSON data from a file, supporting both standard JSON and JSON Lines (NDJSON).
    
    Tries standard JSON parsing first. If that fails, it assumes the file is JSON Lines
    (one JSON object per line) and parses each line individually.
    
    Args:
        path (Path): Path to the input file.
    Returns:
        list or dict: The parsed JSON data.
    Raises:
        json.JSONDecodeError: If neither standard JSON nor JSON Lines parsing succeeds.
    """
    text = path.read_text(encoding="utf-8")
    try:
        # Attempt standard single-object JSON parsing first
        return json.loads(text)
    except json.JSONDecodeError:
        # Fall back to JSONL/NDJSON parsing
        records = []
        for i, line in enumerate(text.splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
        
        # If we failed to parse the initial JSON but found no records via JSONL, re-raise the error.
        if not records:
            raise
        return records


def normalize(data, sep="__") -> pd.DataFrame:
    """
    Flattens deeply nested dictionary and list structures into a flat pandas DataFrame.
    
    Uses json_normalize to create columns by joining nested keys with the specified separator (`sep`).
    
    Args:
        data (list or dict): The parsed JSON data.
        sep (str): Separator to use for nested keys (e.g., 'address__city').
    Returns:
        pd.DataFrame: A flattened tabular representation of the data.
    """
    if isinstance(data, list):
        # Standard case: The root is a list of objects (most common API response format)
        return json_normalize(data, sep=sep)
    
    if isinstance(data, dict):
        # Handles dictionaries (single object root)
        
        # Check if the dictionary contains exactly one key whose value is a list.
        # This is a common pattern: {"meta": {...}, "records": [...]}.
        list_keys = [k for k, v in data.items() if isinstance(v, list)]
        
        if len(list_keys) == 1:
            # If so, treat the list as the primary data source and flatten it.
            key = list_keys[0]
            df = json_normalize(data.get(key, []), sep=sep)
            
            # Carry over all other top-level dictionary fields as 'meta' columns.
            for k, v in data.items():
                if k == key:
                    continue
                # Meta fields are also serialized if complex to preserve data
                df[f"meta{sep}{k}"] = (
                    json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
                )
            return df
        
        # If no clear list of records, flatten the single dictionary object.
        return json_normalize(data, sep=sep)
    
    # Primitive root (e.g., JSON is just a number or string) -> single column DataFrame
    return pd.DataFrame({"value": [data]})


# --- Execution Logic (Main Entry Point) ---

def main():
    """
    Parses command-line arguments, loads the data, flattens it, cleans it, 
    and then either displays the results or saves them to a CSV file.
    """
    p = argparse.ArgumentParser(description="Convert JSON/JSONL to a flat table for display or saving.")
    p.add_argument("input", help="Path to input JSON/JSONL file")
    p.add_argument("--sep", default="__", help="Separator for nested keys (default: __)")
    p.add_argument("-n", "--rows", type=int, default=10, help="Number of rows to display (default: 10)")
    
    # Defines the optional output file argument.
    # nargs='?' makes the argument optional (user can use -o without a value).
    # const='auto' is the value assigned if -o is present but no path is given.
    p.add_argument("-o", "--output", nargs='?', const='auto', default=None,
                   help="Optional path to output CSV file. If provided without a path, it defaults to '<input_name>_flat.csv' in the Downloads folder.")
    args = p.parse_args()

    # 1. Input Validation
    in_path = Path(args.input).expanduser().resolve()
    if not in_path.exists():
        print(f"Error: input file not found: {in_path}", file=sys.stderr)
        sys.exit(2)

    # 2. Data Loading (supports standard JSON and JSON Lines)
    try:
        data = load_json_any(in_path)
    except Exception as e:
        print(f"Error: failed to parse JSON/JSON Lines: {e}", file=sys.stderr)
        sys.exit(3)

    # 3. Data Flattening and Cleaning
    df = normalize(data, sep=args.sep)
    if not df.empty:
        # Apply the cleaning function to every cell in the DataFrame.
        # .map() is used instead of the deprecated .applymap().
        df = df.map(clean_cell)

    if df.empty:
        print(f"No records found in {in_path}.", file=sys.stderr)
        sys.exit(0)

    # 4. Output Logic: Save to CSV or Display to Terminal
    out_file = None
    
    if args.output is not None:
        # User supplied the -o or --output flag, so we save the file.
        
        if args.output == 'auto':
            # Case 1: -o was used without a path (auto-save mode)
            
            # Determine the Downloads folder path universally across OSs
            home_dir = Path.home()
            downloads_dir = home_dir / "Downloads"
            
            # Construct a safe output name based on the input file's name
            base_name = in_path.stem # 'stem' gets the file name without the extension
            out_file = downloads_dir / f"{base_name}_flat.csv"
        else:
            # Case 2: -o was used with a specific output path
            out_file = Path(args.output).expanduser().resolve()

        # Save the file
        try:
            # Save the entire DataFrame to the target path.
            # index=False prevents writing the pandas row numbers (0, 1, 2, ...) to the CSV.
            df.to_csv(out_file, index=False, encoding='utf-8')
            print(f"Success! Flattened data saved to {out_file.as_posix()} (Rows: {len(df)}).")
        except Exception as e:
            # Handle potential file permission or path errors
            print(f"Error: Failed to save file to {out_file.as_posix()}: {e}", file=sys.stderr)
            sys.exit(4)
        
    else:
        # --- ORIGINAL DISPLAY LOGIC (if no output argument is used) ---
        print(f"--- Data from {in_path} (Total Rows: {len(df)}, Columns: {len(df.columns)}) ---")

        # Display the DataFrame based on the --rows argument
        if len(df) > args.rows:
            print(f"\nShowing the first {args.rows} rows:")
            # .to_string() ensures clean formatting in the terminal
            print(df.head(args.rows).to_string())
        else:
            print("\nShowing all rows:")
            print(df.to_string())


if __name__ == "__main__":
    # Ensures the main function is called when the script is run directly
    main()