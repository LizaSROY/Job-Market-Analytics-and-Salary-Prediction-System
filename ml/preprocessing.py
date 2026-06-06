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

# Train from Silver layer
INPUT_FILE = PROC_DIR / "silver_job_market.parquet"


def preprocess():

    print("Starting preprocessing...")

    df = pd.read_parquet(INPUT_FILE)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    # ==========================
    # Features
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
    # Preprocessor
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

    print(
        f"Feature count after encoding: {X.shape[1]}"
    )

    # ==========================
    # Train/Test Split
    # ==========================

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.2,

        random_state=42

    )

    print(
        f"Train Rows: {len(X_train):,}"
    )

    print(
        f"Test Rows: {len(X_test):,}"
    )

    # ==========================
    # Save Arrays
    # ==========================

    np.save(
        PROC_DIR / "X_train.npy",
        X_train
    )

    np.save(
        PROC_DIR / "X_test.npy",
        X_test
    )

    np.save(
        PROC_DIR / "y_train.npy",
        y_train
    )

    np.save(
        PROC_DIR / "y_test.npy",
        y_test
    )

    # ==========================
    # Save Preprocessor
    # ==========================

    with open(
        PROC_DIR / "preprocessor.pkl",
        "wb"
    ) as file:

        pickle.dump(
            preprocessor,
            file
        )

    # Save feature names for debugging
    feature_names = (
        preprocessor
        .get_feature_names_out()
    )

    np.save(
        PROC_DIR / "feature_names.npy",
        feature_names
    )

    print(
        "Preprocessing completed successfully"
    )


if __name__ == "__main__":

    preprocess()