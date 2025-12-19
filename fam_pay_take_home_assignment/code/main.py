from load_data import load_data
from aggregator import aggregate_monthly
from indicators import add_technical_indicators
from writer import write_per_ticker


DATA_PATH = "/Users/dionsaldanha/PycharmProjects/fam_pay_take_home_assignment/data/output_file.csv"
OUTPUT_DIR = "./output"


def main():
    df = load_data(DATA_PATH)
    monthly_df = aggregate_monthly(df)
    final_df = add_technical_indicators(monthly_df)
    write_per_ticker(final_df, OUTPUT_DIR)


if __name__ == "__main__":
    main()
