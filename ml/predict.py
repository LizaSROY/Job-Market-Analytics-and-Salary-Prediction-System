import pickle
import numpy as np

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PROC_DIR = BASE_DIR / "data" / "processed"

MODEL_DIR = BASE_DIR / "ml" / "models"


def predict():

    print("Predicting salary...")


    with open(
        MODEL_DIR/"salary_model.pkl",
        "rb"
    ) as file:

        model=pickle.load(
            file
        )


    with open(
        PROC_DIR/"scaler.pkl",
        "rb"
    ) as file:

        scaler=pickle.load(
            file
        )


    data=[[5,2025,6]]

    data=scaler.transform(
        data
    )


    prediction=model.predict(
        data
    )

    print(
        "Predicted Salary:"
    )

    print(
        round(
            prediction[0],
            2
        )
    )


if __name__=="__main__":
    predict()