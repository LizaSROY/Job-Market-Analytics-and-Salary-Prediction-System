import pandas as pd
from pathlib import Path

# Folder paths
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

SOURCE_FILE = RAW_DIR / "job_market_dataset.csv"

OUTPUT_FILE = RAW_DIR / "job_market_raw.parquet"


def extract():

    print("Starting extraction...")

    # Check file exists
    if not SOURCE_FILE.exists():
        print("Dataset not found")
        return

    # Read CSV
    df = pd.read_csv(SOURCE_FILE)

    print("Dataset loaded successfully")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    # Check missing values
    print("\nMissing values:")
    print(df.isnull().sum())

    # Create raw folder if not exist
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # Save as parquet
    df.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print("\nParquet file saved:")
    print(OUTPUT_FILE)

    print("\nExtraction completed")


if __name__ == "__main__":
    extract()