# src/train.py
import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from model_utils import load_titanic, build_preprocessor, FEATURE_ORDER

DATA_PATH = os.environ.get("DATA_PATH", "../data/train.csv")  # when run from src/ folder, this points to ../data/train.csv
MODEL_OUT = os.environ.get("MODEL_OUT", "model.joblib")       # saved next to src/

def prepare_X_y(df: pd.DataFrame):
    df = df.copy()
    # minimal feature engineering: ensure required columns exist
    df["Pclass"] = df["Pclass"].astype(str)
    df["Embarked"] = df["Embarked"].fillna("S")
    df["Sex"] = df["Sex"].astype(str)

    y = df["Survived"]
    X = df[FEATURE_ORDER]
    return X, y

def train_and_save(data_path=DATA_PATH, outfile=MODEL_OUT):
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Please place Titanic train.csv there.")
    df = load_titanic(data_path)
    X, y = prepare_X_y(df)
    preprocessor = build_preprocessor()
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("clf", clf)
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))
    # Save pipeline + feature order into a dictionary so app can load with metadata
    to_save = {"pipeline": pipeline, "feature_order": FEATURE_ORDER}
    joblib.dump(to_save, outfile)
    print(f"Saved model bundle to {outfile}")

if __name__ == "__main__":
    train_and_save()