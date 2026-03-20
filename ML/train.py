"""
ml/train.py
-----------
Train the LinearRegression model and save it to ml/model.pkl.

Run from project root:
    python -m ml.train
"""

import os
import pickle
from sklearn.linear_model import LinearRegression
from .data import get_X_y, FEATURES

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')


def train() -> LinearRegression:
    """Fit a LinearRegression on the training data and return it."""
    X, y = get_X_y()
    model = LinearRegression()
    model.fit(X, y)
    return model


def save(model: LinearRegression, path: str = MODEL_PATH) -> None:
    """Persist the trained model to disk with pickle."""
    with open(path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved → {path}")


def main():
    print("Training model...")
    model = train()

    coefs = dict(zip(FEATURES, model.coef_))
    print(f"  Coefficients : {coefs}")
    print(f"  Intercept    : {model.intercept_:.2f}")

    # Quick sanity check
    import numpy as np
    sample = np.array([[1500, 3]])
    pred = model.predict(sample)[0]
    print(f"  Sample pred  : 1500 sqft, 3 bed → ${pred:,.0f}")

    save(model)
    print("Done.")


if __name__ == '__main__':
    main()
