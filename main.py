import sys
from cleaner import clean_csv


def usage():
    print("Usage: python main.py <input_csv> <output_csv> <report_txt>")
    print('Example: python main.py sample_data.csv cleaned_data.csv summary_report.txt')


if __name__ == "__main__":
    if len(sys.argv) != 4:
        usage()
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    report_file = sys.argv[3]

    clean_csv(input_file, output_file, report_file)
    print(f"✅ Cleaned file saved to: {output_file}")
    print(f"✅ Summary report saved to: {report_file}")
