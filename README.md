# Job Market Analytics & Salary Prediction System

End-to-end Data Engineering and Machine Learning project for analyzing job market trends and predicting salaries.

## Architecture

```text
Dataset
   ↓
Extract (Python)
   ↓
Transform (PySpark)
   ↓
Load (MySQL)
   ↓
Analytics + ML
   ↓
Dashboard + Prediction App
   ↓
Airflow Orchestration
```

## Tech Stack

* Python
* PySpark
* Flask
* Scikit-learn
* MySQL
* Apache Airflow
* Docker
* Chart.js

## Project Structure

```text
job_market/

├── analytics/
├── dashboard/
├── prediction_app/
├── extraction/
├── transform/
├── load/
├── ml/
├── dags/
├── data/
├── docker/
└── requirements.txt
```

## Run Project

```bash
git clone <YOUR_REPOSITORY_URL>

cd job_market/docker

docker compose up -d --build
```

## Applications

| Service        | URL                   |
| -------------- | --------------------- |
| Airflow        | http://localhost:8080 |
| Dashboard      | http://localhost:5001 |
| Prediction App | http://localhost:5002 |

Airflow Login:

```text
Username: admin
Password: admin
```

## ML Models

* Linear Regression
* Random Forest
* Gradient Boosting

