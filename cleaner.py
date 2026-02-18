import pandas as pd


def clean_csv(input_path: str, output_path: str) -> None:
    df = pd.read_csv(input_path)

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Trim whitespace in string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Convert empty strings to NA (so they count as empty)
    df = df.replace("", pd.NA)

    # Drop rows that are fully empty
    df = df.dropna(how="all")

    # Remove duplicates
    df = df.drop_duplicates()

    # Save cleaned output
    df.to_csv(output_path, index=False)
