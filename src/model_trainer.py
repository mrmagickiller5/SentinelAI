import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)


# Project root
ROOT_DIR = Path(__file__).resolve().parent.parent

# Folder where trained model will be saved
MODEL_DIR = ROOT_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_FILE = MODEL_DIR / "sentinel_rf_model.pkl"
FEATURE_FILE = MODEL_DIR / "model_features.pkl"
METRICS_FILE = MODEL_DIR / "model_metrics.pkl"


def prepare_data(data: pd.DataFrame):
    """
    Prepare network data for machine learning.
    """

    data = data.copy()

    # Remove spaces from column names
    data.columns = data.columns.str.strip()

    # Replace infinity values
    data = data.replace(
        [float("inf"), float("-inf")],
        float("nan")
    )

    # Remove invalid rows
    data = data.dropna()

    # Clean labels
    data["Label"] = (
        data["Label"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Convert labels:
    # BENIGN = 0
    # Everything else (DDoS etc.) = 1
    data["Label"] = data["Label"].apply(
        lambda x: 0 if x == "BENIGN" else 1
    )

    # Separate features and target
    X = data.drop(columns=["Label"])
    y = data["Label"]

    # Keep only numeric features
    X = X.select_dtypes(include=["number"])

    return X, y


def train_model(X, y):
    """
    Train and save the SentinelAI Random Forest model.
    """

    print("\nStarting SentinelAI model training...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    # Train model
    model.fit(X_train, y_train)

    # Test model
    predictions = model.predict(X_test)

    # Calculate performance metrics
    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    print("\n==============================")
    print("SENTINELAI MODEL RESULTS")
    print("==============================")

    print(f"\nAccuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=["BENIGN", "ATTACK"],
            zero_division=0
        )
    )

    # Save trained model
    joblib.dump(
        model,
        MODEL_FILE
    )

    # Save feature names
    joblib.dump(
        list(X.columns),
        FEATURE_FILE
    )

    # Save model metrics
    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }

    joblib.dump(
        metrics,
        METRICS_FILE
    )

    print("\nModel saved successfully!")
    print(f"Model   : {MODEL_FILE}")
    print(f"Features: {FEATURE_FILE}")
    print(f"Metrics : {METRICS_FILE}")

    return model


def load_model():
    """
    Load the previously trained SentinelAI model.
    """

    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            "Trained model not found. Please train the model first."
        )

    return joblib.load(MODEL_FILE)


def predict_data(data: pd.DataFrame):
    """
    Predict whether network traffic is BENIGN or ATTACK.
    """

    model = load_model()

    data = data.copy()

    data.columns = data.columns.str.strip()

    # Remove Label if it exists
    if "Label" in data.columns:
        data = data.drop(columns=["Label"])

    # Keep numeric features
    data = data.select_dtypes(
        include=["number"]
    )

    # Load exact features used during training
    features = joblib.load(
        FEATURE_FILE
    )

    # Match training features
    data = data.reindex(
        columns=features,
        fill_value=0
    )

    predictions = model.predict(data)

    results = [
        "BENIGN" if prediction == 0 else "ATTACK"
        for prediction in predictions
    ]

    return results


if __name__ == "__main__":
    print(
        "SentinelAI model trainer loaded successfully."
    )