import pandas as pd
import json
from pathlib import Path

# Folder paths
BASE_DIR = Path(__file__).resolve().parent.parent

PROC_DIR = BASE_DIR / "data" / "processed"

INPUT_FILE = PROC_DIR / "job_market_clean.parquet"

OUTPUT_FILE = PROC_DIR / "kpis.json"


def generate_kpis():

    print("Generating KPIs...")

    # Read cleaned dataset
    df = pd.read_parquet(INPUT_FILE)

    kpis = {

        # Total jobs
        "total_jobs": len(df),

        # Average salary
        "average_salary":
        round(
            df["salary"].mean(),
            2
        ),

        # Highest salary
        "highest_salary":
        round(
            df["salary"].max(),
            2
        ),

        # Lowest salary
        "lowest_salary":
        round(
            df["salary"].min(),
            2
        ),

        # Top 5 countries
        "top_countries":

        df.groupby(
            "country"
        )
        .size()
        .sort_values(
            ascending=False
        )
        .head(5)
        .to_dict(),

        # Top 5 occupations
        "top_occupations":

        df.groupby(
            "occupation"
        )
        .size()
        .sort_values(
            ascending=False
        )
        .head(5)
        .to_dict(),

        # Education level
        "education_distribution":

        df.groupby(
            "education_level"
        )
        .size()
        .to_dict()

    }

    # Save KPIs
    with open(
        OUTPUT_FILE,
        "w"
    ) as file:

        json.dump(
            kpis,
            file,
            indent=4
        )

    print("KPIs saved")
    print(OUTPUT_FILE)

    return OUTPUT_FILE


if __name__ == "__main__":
    generate_kpis()