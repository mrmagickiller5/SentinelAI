import pandas as pd
import joblib
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = ROOT_DIR / "models" / "sentinel_rf_model.pkl"
FEATURE_FILE = ROOT_DIR / "models" / "model_features.pkl"


def load_model():
    """Load the trained SentinelAI model."""

    model = joblib.load(MODEL_FILE)
    features = joblib.load(FEATURE_FILE)

    return model, features


def predict_network_data(data: pd.DataFrame):
    """
    Predict whether network traffic is BENIGN or ATTACK.
    """

    model, features = load_model()

    data = data.copy()

    # Remove spaces from column names
    data.columns = data.columns.str.strip()

    # Keep only features used during training
    available_features = [
        feature
        for feature in features
        if feature in data.columns
    ]
    print("AVAILABLE FEATURES:", len(available_features))
    if not available_features:
     raise ValueError(
        "Invalid dataset: Required network traffic features were not found. "
        "Please upload a compatible network traffic CSV."
    )

    X = data[available_features].copy()

    # Fill invalid values
    X = X.replace(
        [float("inf"), float("-inf")],
        float("nan")
    )

    X = X.fillna(0)

    # Predictions
    predictions = model.predict(X)

    # Prediction probabilities
    probabilities = model.predict_proba(X)

    confidence = probabilities.max(axis=1)

    # Create result
    result = data.copy()

    result["Prediction"] = [
        "ATTACK" if prediction == 1
        else "BENIGN"
        for prediction in predictions
    ]

    result["Confidence"] = confidence * 100

    # Add actual label when available
    if "Label" in result.columns:

        result["Actual"] = (
            result["Label"]
            .astype(str)
            .str.strip()
            .str.upper()
            .apply(
                lambda x:
                "BENIGN"
                if x == "BENIGN"
                else "ATTACK"
            )
        )

    return result


if __name__ == "__main__":
    print(
        "SentinelAI predictor module loaded successfully."
    )