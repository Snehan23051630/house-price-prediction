"""
ml/data.py
----------
Single source of truth for training data.
Swap this out with a real CSV / database loader in production.
"""

import pandas as pd

# Raw training samples
RAW = {
    'sqft': [
         600,  800, 1000, 1200, 1500,
        1800, 2000, 2200, 2500, 2800,
        3000, 3500, 4000,
    ],
    'bedrooms': [
        1, 2, 2, 3, 3,
        3, 4, 4, 4, 5,
        5, 5, 6,
    ],
    'price': [
        120_000, 160_000, 200_000, 240_000, 300_000,
        360_000, 400_000, 440_000, 500_000, 560_000,
        600_000, 700_000, 800_000,
    ],
}

FEATURES = ['sqft', 'bedrooms']
TARGET   = 'price'


def load_dataframe() -> pd.DataFrame:
    """Return training data as a DataFrame."""
    return pd.DataFrame(RAW)


def get_X_y(df: pd.DataFrame = None):
    """Return feature matrix X and target vector y."""
    if df is None:
        df = load_dataframe()
    return df[FEATURES], df[TARGET]
