from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Folder paths
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROC_DIR = BASE_DIR / "data" / "processed"

INPUT_FILE = str(
    RAW_DIR / "job_market_raw.parquet"
)

OUTPUT_FILE = str(
    PROC_DIR / "job_market_clean.parquet"
)

AGG_FILE = str(
    PROC_DIR / "job_market_analytics.parquet"
)


def transform():

    print("Starting transformation...")

    # Start Spark
    spark = SparkSession.builder \
        .appName("JobMarketTransform") \
        .getOrCreate()

    # Read extracted data
    df = spark.read.parquet(INPUT_FILE)

    print("Original rows:", df.count())

    # Remove duplicates
    df = df.dropDuplicates()

    # Fill missing values
    df = df.fillna({
        "salary": 0,
        "years_of_experience": 0
    })

    # Lowercase country
    df = df.withColumn(
        "country",
        lower(col("country"))
    )

    # Create experience level
    df = df.withColumn(
        "experience_level",
        when(
            col("years_of_experience") < 2,
            "Junior"
        )
        .when(
            col("years_of_experience") < 5,
            "Mid"
        )
        .otherwise("Senior")
    )

    # Create salary category
    df = df.withColumn(
        "salary_level",
        when(
            col("salary") < 30000,
            "Low"
        )
        .when(
            col("salary") < 70000,
            "Medium"
        )
        .otherwise("High")
    )

    # Save cleaned data
    PROC_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.write.mode(
        "overwrite"
    ).parquet(
        OUTPUT_FILE
    )

    print("Cleaned dataset saved")

    # Analytics table
    analytics = df.groupBy(
        "country"
    ).agg(
        avg("salary").alias(
            "average_salary"
        ),
        count("*").alias(
            "total_jobs"
        )
    )

    analytics.write.mode(
        "overwrite"
    ).parquet(
        AGG_FILE
    )

    print("Analytics dataset saved")

    spark.stop()

    print("Transformation completed")


if __name__ == "__main__":
    transform()