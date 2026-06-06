from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

BASE_DIR = Path(__file__).resolve().parent.parent

PROC_DIR = BASE_DIR / "data" / "processed"

BRONZE_FILE = str(
    PROC_DIR / "bronze_job_market.parquet"
)

SILVER_FILE = str(
    PROC_DIR / "silver_job_market.parquet"
)

GOLD_COUNTRY_FILE = str(
    PROC_DIR / "gold_salary_country.parquet"
)

GOLD_OCCUPATION_FILE = str(
    PROC_DIR / "gold_top_occupations.parquet"
)

GOLD_EDUCATION_FILE = str(
    PROC_DIR / "gold_education_distribution.parquet"
)


def transform():

    spark = (
        SparkSession.builder
        .master(
            "spark://spark-master:7077"
        )
        .appName(
            "JobMarketTransform"
        )
        .getOrCreate()
    )

    df = spark.read.parquet(
        BRONZE_FILE
    )

    print("Bronze rows:", df.count())

    silver_df = (
        df
        .dropDuplicates()
        .fillna({
            "salary": 0,
            "years_of_experience": 0
        })
        .withColumn(
            "country",
            lower(col("country"))
        )
        .withColumn(
            "experience_level",
            when(
                col("years_of_experience") < 2,
                "Junior"
            )
            .when(
                col("years_of_experience") < 5,
                "Mid"
            )
            .otherwise(
                "Senior"
            )
        )
        .withColumn(
            "salary_level",
            when(
                col("salary") < 30000,
                "Low"
            )
            .when(
                col("salary") < 70000,
                "Medium"
            )
            .otherwise(
                "High"
            )
        )
    )

    silver_df.write.mode(
        "overwrite"
    ).parquet(
        SILVER_FILE
    )

    gold_country = (
        silver_df
        .groupBy("country")
        .agg(
            avg("salary").alias(
                "average_salary"
            ),
            count("*").alias(
                "total_jobs"
            )
        )
    )

    gold_country.write.mode(
        "overwrite"
    ).parquet(
        GOLD_COUNTRY_FILE
    )

    gold_occupation = (
        silver_df
        .groupBy("occupation")
        .count()
    )

    gold_occupation.write.mode(
        "overwrite"
    ).parquet(
        GOLD_OCCUPATION_FILE
    )

    gold_education = (
        silver_df
        .groupBy("education_level")
        .count()
    )

    gold_education.write.mode(
        "overwrite"
    ).parquet(
        GOLD_EDUCATION_FILE
    )

    spark.stop()