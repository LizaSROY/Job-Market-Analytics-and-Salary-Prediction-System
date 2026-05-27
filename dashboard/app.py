from flask import Flask, render_template, jsonify
import pandas as pd
from pathlib import Path

app = Flask(__name__)

# ==================================
# Paths
# ==================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROC_DIR = BASE_DIR / "data" / "processed"

DATA_FILE = PROC_DIR / "job_market_clean.parquet"

# ==================================
# Load dataset
# ==================================

print("Loading dataset...")

df = pd.read_parquet(DATA_FILE)

print(f"Rows loaded: {len(df)}")


# ==================================
# Home page
# ==================================

@app.route("/")
def dashboard():

    return render_template(

        "index.html",

        total_jobs=len(df),

        average_salary=round(
            df["salary"].mean(),
            2
        ),

        countries=df["country"].nunique(),

        occupations=df["occupation"].nunique()

    )


# ==================================
# 1 Salary by Country
# ==================================

@app.route("/api/country-salary")
def country_salary():

    result=(

        df.groupby(
            "country"
        )

        .agg(
            total_jobs=("country","count"),
            average_salary=("salary","mean")
        )

        .reset_index()

        .sort_values(
            "average_salary",
            ascending=False
        )

        .head(10)

    )

    return jsonify(
        result.to_dict(
            orient="records"
        )
    )


# ==================================
# 2 Top Occupations
# ==================================

@app.route("/api/top-occupations")
def top_occupations():

    result=(

        df.groupby(
            "occupation"
        )

        .agg(
            total_jobs=("occupation","count"),
            average_salary=("salary","mean")
        )

        .reset_index()

        .sort_values(
            "average_salary",
            ascending=False
        )

        .head(10)

    )

    return jsonify(
        result.to_dict(
            orient="records"
        )
    )


# ==================================
# 3 Education vs Salary
# ==================================

@app.route("/api/education")
def education():

    result=(

        df.groupby(
            "education_level"
        )

        .agg(
            total_jobs=("education_level","count"),
            average_salary=("salary","mean")
        )

        .reset_index()

    )

    return jsonify(
        result.to_dict(
            orient="records"
        )
    )


# ==================================
# 4 Experience vs Salary
# ==================================

@app.route("/api/experience")
def experience():

    result=(

        df.groupby(
            "experience_level"
        )

        .agg(
            total_jobs=("experience_level","count"),
            average_salary=("salary","mean")
        )

        .reset_index()

    )

    return jsonify(

        result.to_dict(
            orient="records"
        )

    )


# ==================================
# 5 Monthly Trend
# ==================================

@app.route("/api/monthly")
def monthly():

    result=(

        df.groupby(
            ["year","month"]
        )

        .size()

        .reset_index(
            name="total_jobs"
        )

        .sort_values(
            ["year","month"]
        )

    )

    return jsonify(
        result.to_dict(
            orient="records"
        )
    )


# ==================================
# 6 Top Cities
# ==================================

@app.route("/api/cities")
def cities():

    result=(

        df.groupby(
            ["city","country"]
        )

        .size()

        .reset_index(
            name="total_jobs"
        )

        .sort_values(
            "total_jobs",
            ascending=False
        )

        .head(10)

    )

    return jsonify(
        result.to_dict(
            orient="records"
        )
    )


# ==================================
# 7 Salary Band Distribution
# ==================================

@app.route("/api/salary-band")
def salary_band():

    result=(

        df.groupby(
            "salary_level"
        )

        .size()

        .reset_index(
            name="count"
        )

    )

    return jsonify(

        result.to_dict(
            orient="records"
        )

    )


# ==================================
# 8 Company Size
# ==================================

@app.route("/api/company")
def company():

    result=(

        df.groupby(
            "company_size"
        )

        .agg(
            total_jobs=("company_size","count"),
            average_salary=("salary","mean")
        )

        .reset_index()

    )

    return jsonify(
        result.to_dict(
            orient="records"
        )
    )


# ==================================
# Run Flask
# ==================================

if __name__=="__main__":

    app.run(

        host="0.0.0.0",
        port=5000,
        debug=False

    )