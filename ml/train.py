import numpy as np
import pickle
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.metrics import (
    mean_absolute_error,
    r2_score
)

BASE_DIR = Path(__file__).resolve().parent.parent

PROC_DIR = BASE_DIR / "data" / "processed"

MODEL_DIR = BASE_DIR / "ml" / "models"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================
# Load data
# ==========================

X_train=np.load(
    PROC_DIR/"X_train.npy"
)

X_test=np.load(
    PROC_DIR/"X_test.npy"
)

y_train=np.load(
    PROC_DIR/"y_train.npy"
)

y_test=np.load(
    PROC_DIR/"y_test.npy"
)


# ==========================
# Models
# ==========================

models={

"LinearRegression":

LinearRegression(),

"RandomForest":

RandomForestRegressor(

n_estimators=100,

max_depth=15,

random_state=42,

n_jobs=-1

),

"GradientBoosting":

GradientBoostingRegressor(

n_estimators=100,

learning_rate=0.1,

random_state=42

)

}


best_model=None
best_mae=float("inf")


print("\nTraining Models...\n")


for name,model in models.items():

    print(f"Training {name}")

    model.fit(
        X_train,
        y_train
    )

    predictions=model.predict(
        X_test
    )

    mae=mean_absolute_error(
        y_test,
        predictions
    )

    r2=r2_score(
        y_test,
        predictions
    )

    print(
        f"MAE: {mae:.2f}"
    )

    print(
        f"R²: {r2:.4f}"
    )

    print("-"*30)

    if mae<best_mae:

        best_mae=mae

        best_model=model


# ==========================
# Save best model
# ==========================

for name,model in models.items():

    print(f"Training {name}")

    model.fit(
        X_train,
        y_train
    )

    predictions=model.predict(
        X_test
    )

    mae=mean_absolute_error(
        y_test,
        predictions
    )

    r2=r2_score(
        y_test,
        predictions
    )

    print(
        f"MAE: {mae:.2f}"
    )

    print(
        f"R²: {r2:.4f}"
    )

    print("-"*30)

    with open(

        MODEL_DIR/f"{name}.pkl",

        "wb"

    ) as file:

        pickle.dump(
            model,
            file
        )

    print(
        f"{name} saved"
    )