import pandas as pd
import numpy as np
import pickle

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder
)
from sklearn.compose import ColumnTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

PROC_DIR = BASE_DIR / "data" / "processed"

INPUT_FILE = PROC_DIR / "job_market_clean.parquet"


def preprocess():

    print("Starting preprocessing...")

    df = pd.read_parquet(INPUT_FILE)

    # ==========================
    # Feature selection
    # ==========================

    numeric_cols = [

        "years_of_experience",
        "year",
        "month"

    ]

    categorical_cols = [

        "country",
        "city",
        "occupation",
        "field",
        "employment_type",
        "education_level",
        "gender",
        "company_size",
        "experience_level"

    ]

    X = df[
        numeric_cols +
        categorical_cols
    ]

    y = df["salary"]


    # ==========================
    # Preprocessing
    # ==========================

    preprocessor = ColumnTransformer(

        [

            (

                "num",

                StandardScaler(),

                numeric_cols

            ),

            (

                "cat",

                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                    
                ),

                categorical_cols

            )

        ]

    )

    X = preprocessor.fit_transform(X)


    # ==========================
    # Train test split
    # ==========================

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.2,

        random_state=42

    )


    # ==========================
    # Save files
    # ==========================

    np.save(
        PROC_DIR/"X_train.npy",
        X_train
    )

    np.save(
        PROC_DIR/"X_test.npy",
        X_test
    )

    np.save(
        PROC_DIR/"y_train.npy",
        y_train
    )

    np.save(
        PROC_DIR/"y_test.npy",
        y_test
    )

    with open(
        PROC_DIR/"preprocessor.pkl",
        "wb"
    ) as file:

        pickle.dump(
            preprocessor,
            file
        )

    print("Preprocessing completed")


if __name__=="__main__":

    preprocess()