from __future__ import annotations

import pandas as pd
from pathlib import Path


def clean_csv(input_path: str, output_path: str, report_path: str) -> None:
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {e}")

    original_rows = len(df)

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Trim whitespace in string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()
        # Convert literal "nan" strings back to NA (can happen after astype(str))
        df[col] = df[col].replace("nan", pd.NA)

    # Convert empty strings to NA
    df = df.replace("", pd.NA)

    # Drop rows that are fully empty
    df = df.dropna(how="all")

    # Remove duplicates
    before_dupes = len(df)
    df = df.drop_duplicates()
    removed_duplicates = before_dupes - len(df)

    cleaned_rows = len(df)

    # Save cleaned output
    df.to_csv(output_path, index=False)

    # Generate report
    generate_report(
        report_path=report_path,
        original_rows=original_rows,
        cleaned_rows=cleaned_rows,
        removed_duplicates=removed_duplicates,
        columns=list(df.columns),
        null_counts=df.isna().sum().to_dict(),
    )


def generate_report(
    report_path: str,
    original_rows: int,
    cleaned_rows: int,
    removed_duplicates: int,
    columns: list[str],
    null_counts: dict,
) -> None:
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("CSV Cleaning Summary Report\n")
        f.write("===========================\n\n")
        f.write(f"Original rows: {original_rows}\n")
        f.write(f"Cleaned rows:  {cleaned_rows}\n")
        f.write(f"Duplicates removed: {removed_duplicates}\n\n")

        f.write("Columns:\n")
        for c in columns:
            f.write(f"- {c}\n")

        f.write("\nMissing values per column:\n")
        for col, count in null_counts.items():
            f.write(f"- {col}: {count}\n")
