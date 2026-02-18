from cleaner import clean_csv


if __name__ == "__main__":
    input_file = "sample_data.csv"
    output_file = "cleaned_data.csv"


    clean_csv(input_file, output_file)
    print(f"Cleaned file saved to: {output_file}")