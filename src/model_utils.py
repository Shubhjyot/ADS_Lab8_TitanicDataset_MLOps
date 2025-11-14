# src/model_utils.py
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Feature order used in training and in the API
FEATURE_ORDER = ["Age", "Fare", "Sex", "Embarked", "Pclass"]

def load_titanic(path: str):
    """
    Expects Kaggle Titanic train.csv (columns: PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked)
    """
    df = pd.read_csv(path)
    return df

def build_preprocessor():
    numeric_features = ["Age", "Fare"]
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_features = ["Sex", "Embarked", "Pclass"]
    # treat Pclass as categorical too (string)
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse=False))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ])

    return preprocessor