import os
import logging
from pyspark.sql import SparkSession

MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_PORT = "3306"
MYSQL_DB = "job_market"
MYSQL_USER = "jobuser"
MYSQL_PASSWORD = "jobpassword"

MYSQL_URL = (
    f"jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def write_table(df, table_name):

    log.info(f"Writing {table_name}...")

    (
        df.write
        .format("jdbc")
        .option("url", MYSQL_URL)
        .option("dbtable", table_name)
        .option("user", MYSQL_USER)
        .option("password", MYSQL_PASSWORD)
        .option("driver", "com.mysql.cj.jdbc.Driver")
        .option("batchsize", 10000)
        .mode("overwrite")
        .save()
    )

    log.info(f"{table_name} written successfully")


def load():

    spark = (
        SparkSession.builder
        .master(
            "spark://spark-master:7077"
        )
        .appName(
            "Load Job Market Warehouse"
        )
        .config(
            "spark.jars",
            "/opt/spark/jars/mysql-connector-j-8.3.0.jar"
        )
        .getOrCreate()
    )

    try:

        log.info("Reading warehouse parquet files...")

        bronze_df = spark.read.parquet(
            "data/processed/bronze_job_market.parquet"
        )

        silver_df = spark.read.parquet(
            "data/processed/silver_job_market.parquet"
        )

        gold_country_df = spark.read.parquet(
            "data/processed/gold_salary_country.parquet"
        )

        gold_occupation_df = spark.read.parquet(
            "data/processed/gold_top_occupations.parquet"
        )

        gold_education_df = spark.read.parquet(
            "data/processed/gold_education_distribution.parquet"
        )

        log.info(
            f"Bronze rows: {bronze_df.count()}"
        )

        log.info(
            f"Silver rows: {silver_df.count()}"
        )

        write_table(
            bronze_df,
            "bronze_job_market"
        )

        write_table(
            silver_df,
            "silver_job_market"
        )

        write_table(
            gold_country_df,
            "gold_salary_country"
        )

        write_table(
            gold_occupation_df,
            "gold_top_occupations"
        )

        write_table(
            gold_education_df,
            "gold_education_distribution"
        )

        log.info(
            "Warehouse loading completed"
        )

    except Exception as e:

        log.error(str(e))
        raise

    finally:

        spark.stop()


if __name__ == "__main__":
    load()