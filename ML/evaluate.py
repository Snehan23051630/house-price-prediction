"""
ml/evaluate.py
--------------
Evaluate the trained model with cross-validation and common metrics.

Run from project root:
    python -m ml.evaluate
"""

import pickle
import os
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
from .data import get_X_y

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')


def load_model(path: str = MODEL_PATH):
    with open(path, 'rb') as f:
        return pickle.load(f)


def evaluate(model=None) -> dict:
    """
    Compute MAE, RMSE, R² and 5-fold CV R² for the model.
    Returns a dict of metric names → values.
    """
    if model is None:
        model = load_model()

    X, y = get_X_y()
    y_pred = model.predict(X)

    mae  = mean_absolute_error(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    r2   = r2_score(y, y_pred)
    cv_r2 = cross_val_score(model, X, y, cv=min(5, len(y)), scoring='r2').mean()

    return {
        'MAE':     round(mae, 2),
        'RMSE':    round(rmse, 2),
        'R2':      round(r2, 4),
        'CV_R2':   round(cv_r2, 4),
    }


def main():
    print("Evaluating model...")
    metrics = evaluate()
    for name, val in metrics.items():
        print(f"  {name:8s}: {val}")


if __name__ == '__main__':
    main()
