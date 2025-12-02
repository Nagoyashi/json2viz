#!/usr/bin/env python3
"""
json2viz — Convert JSON (or JSON Lines) to a flat table and display/save it.

Usage:
  json2viz INPUT.json
  # OR if running the script directly:
  # python json2viz.py INPUT.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
import pandas as pd
from pandas import json_normalize


# --- Utility Functions (Kept from Original Code) ---

ILLEGAL = re.compile(r"[\x00-\x08\x0B-\x1F\x7F]")  # Excel/OpenPyXL-unsafe control chars


def clean_cell(v):
    """Make values CSV/Excel-safe: stringify lists/dicts and strip control chars from strings."""
    if isinstance(v, (dict, list)):
        try:
            return json.dumps(v, ensure_ascii=False)
        except Exception:
            return str(v)
    if isinstance(v, str):
        # Normalize newlines and remove illegal characters
        v = v.replace("\r\n", "\n").replace("\r", "\n")
        v = ILLEGAL.sub("", v)
        return v
    return v


def load_json_any(path: Path):
    """Load standard JSON; fall back to JSON Lines (NDJSON)."""
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try JSONL/NDJSON: one JSON object per non-empty line
        records = []
        for i, line in enumerate(text.splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
        if not records:
            raise
        return records


def normalize(data, sep="__") -> pd.DataFrame:
    """Flatten dict/list into a table with nested keys joined by `sep`."""
    if isinstance(data, list):
        return json_normalize(data, sep=sep)
    if isinstance(data, dict):
        list_keys = [k for k, v in data.items() if isinstance(v, list)]
        if len(list_keys) == 1:
            key = list_keys[0]
            df = json_normalize(data.get(key, []), sep=sep)
            # carry other top-level fields as meta_*
            for k, v in data.items():
                if k == key:
                    continue
                df[f"meta{sep}{k}"] = (
                    json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
                )
            return df
        return json_normalize(data, sep=sep)
    # primitive root -> single column
    return pd.DataFrame({"value": [data]})


# --- Execution Logic (Modified to Display) ---

def main():
    p = argparse.ArgumentParser(description="Convert JSON/JSONL to a flat table for display.")
    p.add_argument("input", help="Path to input JSON/JSONL file")
    p.add_argument("--sep", default="__", help="Separator for nested keys (default: __)")
    # New argument to control how many rows to display
    p.add_argument("-n", "--rows", type=int, default=10, help="Number of rows to display (default: 10)")
    args = p.parse_args()

    in_path = Path(args.input).expanduser().resolve()
    if not in_path.exists():
        print(f"Error: input file not found: {in_path}", file=sys.stderr)
        sys.exit(2)

    try:
        data = load_json_any(in_path)
    except Exception as e:
        print(f"Error: failed to parse JSON/JSON Lines: {e}", file=sys.stderr)
        sys.exit(3)

    df = normalize(data, sep=args.sep)
    if not df.empty:
        # Apply cleaning function to ensure safe display
        df = df.map(clean_cell)

    if df.empty:
        print(f"No records found in {in_path}.", file=sys.stderr)
        sys.exit(0)

    print(f"--- Data from {in_path} (Total Rows: {len(df)}, Columns: {len(df.columns)}) ---")

    # Display the DataFrame using the pandas 'to_string' or 'head' methods
    if len(df) > args.rows:
        print(f"\nShowing the first {args.rows} rows:")
        print(df.head(args.rows).to_string())
    else:
        print("\nShowing all rows:")
        print(df.to_string())


if __name__ == "__main__":
    main()