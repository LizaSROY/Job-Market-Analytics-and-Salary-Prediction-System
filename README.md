# Job Market Analytics & Salary Prediction System

An end-to-end Data Engineering and Machine Learning project that processes large-scale job market data, builds a data warehouse, analyzes hiring trends, and predicts salaries using machine learning models.

## Overview

This project demonstrates a complete modern data pipeline using Apache Airflow, Apache Spark, MySQL, and Streamlit.

The pipeline ingests raw job market data, transforms it into a multi-layer warehouse architecture (Bronze, Silver, Gold), stores analytical datasets in MySQL, and serves interactive analytics dashboards and salary predictions through Streamlit applications.

---

## Architecture

```text
Raw Dataset (500K+ Records)
            │
            ▼
      Extract Layer
         (Python)
            │
            ▼
    Apache Spark Cluster
     (Transform Layer)
            │
            ▼
 ┌─────────────────────┐
 │   Bronze Layer      │
 │ Raw Processed Data  │
 └─────────────────────┘
            │
            ▼
 ┌─────────────────────┐
 │    Silver Layer     │
 │ Cleaned Data Model  │
 └─────────────────────┘
            │
            ▼
 ┌─────────────────────┐
 │     Gold Layer      │
 │ Business Metrics    │
 └─────────────────────┘
            │
            ▼
      MySQL Warehouse
            │
      ┌─────┴─────┐
      ▼           ▼
 Analytics     Salary
 Dashboard    Prediction
 (Streamlit)  (ML Model)
            │
            ▼
      Apache Airflow
      Orchestration
```

---

## Features

### Data Engineering

* Automated ETL pipeline using Apache Airflow
* Distributed data processing with Apache Spark
* Bronze, Silver, and Gold warehouse architecture
* MySQL data warehouse
* Dockerized environment

### Analytics

* Job market KPI dashboard
* Average salary analysis by country
* Top occupations analysis
* Education distribution analysis
* Warehouse layer monitoring

### Machine Learning

* Salary prediction system
* Feature engineering and preprocessing pipeline
* One-Hot Encoding for categorical variables
* Standardization for numerical variables
* Model evaluation using MAE and R²

---

## Technology Stack

### Data Engineering

* Python
* Apache Spark
* Apache Airflow
* MySQL
* Docker

### Data Processing

* Pandas
* NumPy
* PyArrow

### Machine Learning

* Scikit-learn
* Random Forest Regressor
* Gradient Boosting Regressor
* Linear Regression

### Frontend

* Streamlit
* Plotly

---

## Project Structure

```text
job_market/

├── extraction/
│   └── extract.py
│
├── transformation/
│   └── transform.py
│
├── loading/
│   └── load.py
│
├── ml/
│   ├── preprocessing.py
│   ├── train.py
│   ├── predict.py
│   └── models/
│
├── streamlit_app/
│   ├── app.py
│   └── pages/
│       ├── analytics.py
│       └── prediction.py
│
├── dags/
│   └── job_market_pipeline.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile.airflow
│   └── Dockerfile.streamlit
│
├── requirements.txt
└── README.md
```

---

## Warehouse Layers

### Bronze Layer

Raw extracted dataset stored in parquet format.

### Silver Layer

Cleaned and standardized dataset after:

* Duplicate removal
* Missing value handling
* Feature engineering
* Data normalization

### Gold Layer

Business-ready analytical datasets:

* Salary by country
* Top occupations
* Education distribution

---

## Machine Learning Pipeline

### Input Features

* Years of Experience
* Country
* City
* Occupation
* Field
* Employment Type
* Education Level
* Gender
* Company Size
* Experience Level
* Year
* Month

### Models Evaluated

* Linear Regression
* Random Forest Regressor
* Gradient Boosting Regressor

The best-performing model is automatically selected and deployed for salary prediction.

---

## Running the Project

Clone the repository:

```bash
git clone <https://github.com/LizaSROY/Job-Market-Analytics-and-Salary-Prediction-System.git>

cd job_market/docker
```

Build and start services:

```bash
docker compose up -d --build
```

---

## Services

| Service             | URL                   |
| ------------------- | --------------------- |
| Airflow             | http://localhost:8080 |
| Streamlit Dashboard | http://localhost:8501 |
| Spark Master UI     | http://localhost:8081 |

---

## Airflow Login

```text
Username: admin
Password: admin
```

---

## Pipeline Execution

1. Start all Docker services
2. Open Airflow
3. Trigger `job_market_pipeline`
4. Verify Bronze, Silver, and Gold tables are loaded into MySQL
5. Open Streamlit dashboard
6. Explore analytics and generate salary predictions

---

## Future Improvements

* Real-time job market ingestion using Kafka
* Automated model retraining pipeline
* MLflow model tracking
* Cloud deployment (AWS/GCP/Azure)
* Advanced forecasting and trend analysis
* Data quality monitoring framework

---

## Author

Liza SROY

Data Engineering • Data Analytics • Machine Learning


