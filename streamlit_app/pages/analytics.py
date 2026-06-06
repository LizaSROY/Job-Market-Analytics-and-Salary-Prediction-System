import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.set_page_config(
    page_title="Analytics Dashboard",
    layout="wide"
)

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.big-title {
    font-size: 34px;
    font-weight: 700;
}

.subtitle {
    font-size: 18px;
    color: gray;
}

[data-testid="stMetricValue"] {
    font-size: 32px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='big-title'>
📊 Job Market Analytics Dashboard
</div>

<div class='subtitle'>
Data Engineering • Apache Spark • Airflow • Machine Learning
</div>
""", unsafe_allow_html=True)


@st.cache_data
def get_data():

    conn = mysql.connector.connect(
        host="mysql",
        user="jobuser",
        password="jobpassword",
        database="job_market"
    )

    silver_df = pd.read_sql(
        "SELECT * FROM silver_job_market",
        conn
    )

    country_df = pd.read_sql(
        "SELECT * FROM gold_salary_country",
        conn
    )

    occupation_df = pd.read_sql(
        "SELECT * FROM gold_top_occupations",
        conn
    )

    education_df = pd.read_sql(
        "SELECT * FROM gold_education_distribution",
        conn
    )

    bronze_count = pd.read_sql(
        "SELECT COUNT(*) cnt FROM bronze_job_market",
        conn
    )

    silver_count = pd.read_sql(
        "SELECT COUNT(*) cnt FROM silver_job_market",
        conn
    )

    conn.close()

    return (
        silver_df,
        country_df,
        occupation_df,
        education_df,
        bronze_count,
        silver_count
    )


(
    silver_df,
    country_df,
    occupation_df,
    education_df,
    bronze_count,
    silver_count
) = get_data()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Jobs",
    f"{len(silver_df):,}"
)

c2.metric(
    "Average Salary",
    f"${silver_df['salary'].mean():,.0f}"
)

c3.metric(
    "Highest Salary",
    f"${silver_df['salary'].max():,.0f}"
)

c4.metric(
    "Lowest Salary",
    f"${silver_df['salary'].min():,.0f}"
)

st.divider()

fig_country = px.bar(

    country_df
    .sort_values(
        "average_salary",
        ascending=True
    )
    .tail(10),

    x="average_salary",
    y="country",

    orientation="h",

    title="Top Countries by Average Salary"
)

st.plotly_chart(
    fig_country,
    use_container_width=True
)

col1, col2 = st.columns(2)

with col1:

    fig_occ = px.bar(

        occupation_df.sort_values(
            "count",
            ascending=False
        ).head(10),

        x="occupation",

        y="count",

        title="Top Occupations"
    )

    st.plotly_chart(
        fig_occ,
        use_container_width=True
    )

with col2:

    fig_edu = px.pie(

        education_df,

        names="education_level",

        values="count",

        title="Education Distribution"
    )

    st.plotly_chart(
        fig_edu,
        use_container_width=True
    )

st.divider()

st.divider()

fig_salary = px.histogram(

    silver_df,

    x="salary",

    nbins=50,

    title="Salary Distribution"
)

st.plotly_chart(
    fig_salary,
    use_container_width=True
)

st.subheader(
    "Warehouse Overview"
)

w1, w2, w3, w4, w5 = st.columns(5)

w1.metric(
    "Bronze",
    int(bronze_count.iloc[0, 0])
)

w2.metric(
    "Silver",
    int(silver_count.iloc[0, 0])
)

w3.metric(
    "Country Gold",
    len(country_df)
)

w4.metric(
    "Occupation Gold",
    len(occupation_df)
)

w5.metric(
    "Education Gold",
    len(education_df)
)