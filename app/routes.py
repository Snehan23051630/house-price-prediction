import pickle
import numpy as np
from flask import current_app


def load_model():
    """Load the trained model from disk. Called once at app startup."""
    model_path = current_app.config['MODEL_PATH']
    with open(model_path, 'rb') as f:
        return pickle.load(f)


def predict_price(model, sqft: float, bedrooms: float) -> dict:
    """
    Run a prediction and return a result dict.

    Args:
        model:    Loaded sklearn model object.
        sqft:     Square footage (float).
        bedrooms: Number of bedrooms (float).

    Returns:
        dict with keys 'price' (float) and 'formatted' (str).

    Raises:
        ValueError: If inputs are out of acceptable range.
    """
    if sqft <= 0:
        raise ValueError('Square footage must be greater than 0.')
    if not (1 <= bedrooms <= 10):
        raise ValueError('Bedrooms must be between 1 and 10.')

    features = np.array([[sqft, bedrooms]])
    raw = model.predict(features)[0]
    price = float(max(raw, 500_000))   # floor at ₹5,00,000

    return {
        'price':     round(price, 2),
        'formatted': f'${price:,.0f}',
    }
