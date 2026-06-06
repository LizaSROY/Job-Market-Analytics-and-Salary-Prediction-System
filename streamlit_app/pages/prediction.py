import streamlit as st
import pandas as pd
import pickle
import mysql.connector

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_DIR = BASE_DIR / "ml" / "models"
PROC_DIR = BASE_DIR / "data" / "processed"

st.set_page_config(
    page_title="Salary Prediction",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<style>

[data-testid="stMetricValue"] {
    font-size: 40px;
}

.main {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

st.title("💰 Salary Prediction Engine")

st.markdown("""
Predict expected annual salary using the best-performing machine learning model trained on 500K+ job market records.
""")


@st.cache_data
def load_reference_data():

    conn = mysql.connector.connect(
        host="mysql",
        user="jobuser",
        password="jobpassword",
        database="job_market"
    )

    df = pd.read_sql(
        """
        SELECT
            country,
            city,
            occupation,
            field,
            employment_type,
            education_level,
            gender,
            company_size,
            experience_level
        FROM silver_job_market
        """,
        conn
    )

    conn.close()

    return df


reference_df = load_reference_data()

with st.sidebar:

    st.header("Model Information")

    st.success(
        "Best Model Loaded"
    )

    st.info(
        "Training Dataset: 500K+ Records"
    )

    st.caption(
        "Model selected automatically during training"
    )

    st.divider()

    st.write(
        "This prediction is generated using the best-performing machine learning model based on MAE evaluation."
    )


with st.form("prediction_form"):

    st.subheader(
        "Job Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        years_of_experience = st.number_input(
            "Years of Experience",
            min_value=0,
            max_value=50,
            value=5
        )

        country = st.selectbox(
            "Country",
            sorted(
                reference_df["country"]
                .dropna()
                .unique()
            )
        )

        city = st.selectbox(
            "City",
            sorted(
                reference_df["city"]
                .dropna()
                .unique()
            )
        )

        occupation = st.selectbox(
            "Occupation",
            sorted(
                reference_df["occupation"]
                .dropna()
                .unique()
            )
        )

        field = st.selectbox(
            "Field",
            sorted(
                reference_df["field"]
                .dropna()
                .unique()
            )
        )

        year = st.number_input(
            "Year",
            min_value=2020,
            max_value=2035,
            value=2025
        )

    with col2:

        month = st.number_input(
            "Month",
            min_value=1,
            max_value=12,
            value=6
        )

        employment_type = st.selectbox(
            "Employment Type",
            sorted(
                reference_df["employment_type"]
                .dropna()
                .unique()
            )
        )

        education_level = st.selectbox(
            "Education Level",
            sorted(
                reference_df["education_level"]
                .dropna()
                .unique()
            )
        )

        gender = st.selectbox(
            "Gender",
            sorted(
                reference_df["gender"]
                .dropna()
                .unique()
            )
        )

        company_size = st.selectbox(
            "Company Size",
            sorted(
                reference_df["company_size"]
                .dropna()
                .unique()
            )
        )

        experience_level = st.selectbox(
            "Experience Level",
            sorted(
                reference_df["experience_level"]
                .dropna()
                .unique()
            )
        )

    submitted = st.form_submit_button(
        "🚀 Predict Salary",
        use_container_width=True
    )


if submitted:

    with open(
        MODEL_DIR / "best_model.pkl",
        "rb"
    ) as file:

        model = pickle.load(file)

    with open(
        PROC_DIR / "preprocessor.pkl",
        "rb"
    ) as file:

        preprocessor = pickle.load(file)

    input_df = pd.DataFrame([{

        "years_of_experience": years_of_experience,
        "year": year,
        "month": month,
        "country": country,
        "city": city,
        "occupation": occupation,
        "field": field,
        "employment_type": employment_type,
        "education_level": education_level,
        "gender": gender,
        "company_size": company_size,
        "experience_level": experience_level

    }])

    transformed = preprocessor.transform(
        input_df
    )

    prediction = model.predict(
        transformed
    )

    salary = float(
        prediction[0]
    )

    st.divider()

    st.metric(
        "Estimated Annual Salary",
        f"${salary:,.0f}"
    )

    if salary < 70000:

        st.warning(
            "📉 Below average salary range"
        )

    elif salary < 200000:

        st.info(
            "📊 Average market salary range"
        )

    else:

        st.success(
            "🚀 High salary range"
        )

    st.caption(
        "Prediction generated using the best-performing machine learning model."
    )