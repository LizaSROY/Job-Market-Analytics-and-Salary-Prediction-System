import os
import logging
from pyspark.sql import SparkSession

# MySQL settings
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


def load():

    spark = (
        SparkSession.builder
        .appName("Load Job Market")
        .config(
            "spark.jars",
            "/opt/spark/jars/mysql-connector-j-8.3.0.jar"
        )
        .getOrCreate()
    )

    try:

        log.info("Reading processed files...")

        clean_df = spark.read.parquet(
            "data/processed/job_market_clean.parquet"
        )

        analytics_df = spark.read.parquet(
            "data/processed/job_market_analytics.parquet"
        )

        log.info(f"Clean rows: {clean_df.count()}")
        log.info(f"Analytics rows: {analytics_df.count()}")

        # ----------------------------
        # Write cleaned table
        # ----------------------------

        log.info("Writing cleaned table...")

        clean_df.write \
            .format("jdbc") \
            .option("url", MYSQL_URL) \
            .option("dbtable", "job_market_clean") \
            .option("user", MYSQL_USER) \
            .option("password", MYSQL_PASSWORD) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .option("batchsize", 10000) \
            .mode("overwrite") \
            .save()

        log.info("Clean table written successfully")

        # ----------------------------
        # Write analytics table
        # ----------------------------

        log.info("Writing analytics table...")

        analytics_df.write \
            .format("jdbc") \
            .option("url", MYSQL_URL) \
            .option("dbtable", "job_market_analytics") \
            .option("user", MYSQL_USER) \
            .option("password", MYSQL_PASSWORD) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .option("batchsize", 10000) \
            .mode("overwrite") \
            .save()

        log.info("Analytics table written successfully")
        log.info("Load complete")

    except Exception as e:

        log.error("ERROR OCCURRED:")
        log.error(str(e))

        raise

    finally:

        spark.stop()


if __name__ == "__main__":
    load()