import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROC_DIR = BASE_DIR / "data" / "processed"

SOURCE_FILE = RAW_DIR / "job_market_dataset.csv"

BRONZE_FILE = PROC_DIR / "bronze_job_market.parquet"


def extract():

    print("Starting extraction...")

    if not SOURCE_FILE.exists():
        raise FileNotFoundError(
            f"{SOURCE_FILE} not found"
        )

    df = pd.read_csv(SOURCE_FILE)

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    PROC_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_parquet(
        BRONZE_FILE,
        index=False
    )

    print("Bronze layer created")


if __name__ == "__main__":
    extract()