from flask import Flask, render_template, request
import pandas as pd
import pickle
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "ml" / "models"

PROC_DIR = BASE_DIR / "data" / "processed"


# =============================
# Load models
# =============================

models = {

    "LinearRegression":
    pickle.load(
        open(
            MODEL_DIR/"LinearRegression.pkl",
            "rb"
        )
    ),

    "RandomForest":
    pickle.load(
        open(
            MODEL_DIR/"RandomForest.pkl",
            "rb"
        )
    ),

    "GradientBoosting":
    pickle.load(
        open(
            MODEL_DIR/"GradientBoosting.pkl",
            "rb"
        )
    )

}


with open(
    PROC_DIR/"preprocessor.pkl",
    "rb"
) as f:

    preprocessor=pickle.load(f)



# =============================
# Main page
# =============================

@app.route("/")

def home():

    return render_template(
        "prediction.html"
    )



# =============================
# Prediction
# =============================

@app.route("/predict",methods=["POST"])

def predict():

    data={

        "years_of_experience":
        [float(request.form["experience"])],

        "year":
        [2026],

        "month":
        [5],

        "country":
        [request.form["country"]],

        "city":
        [request.form["city"]],

        "occupation":
        [request.form["occupation"]],

        "field":
        [request.form["field"]],

        "employment_type":
        [request.form["employment_type"]],

        "education_level":
        [request.form["education_level"]],

        "gender":
        [request.form["gender"]],

        "company_size":
        [request.form["company_size"]],

        "experience_level":
        [request.form["experience_level"]]

    }

    df=pd.DataFrame(data)

    X=preprocessor.transform(df)

    model_name=request.form["model"]

    model=models[model_name]

    prediction=model.predict(X)[0]


    return render_template(

        "prediction.html",

        predicted_salary=
        round(
            prediction,
            2
        ),

        selected_model=
        model_name

    )



if __name__=="__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False

    )