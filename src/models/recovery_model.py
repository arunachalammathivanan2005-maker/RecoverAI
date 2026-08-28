import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


# Features used by the recovery model
NUMERIC_FEATURES = [
    "amount",
    "retry_count",
    "previous_success_count",
    "previous_failure_count",
    "historical_success_rate",
    "transaction_hour"
]

CATEGORICAL_FEATURES = [
    "payment_method",
    "failure_reason",
    "device_type",
    "channel"
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def create_model():
    """
    Create the RecoverAI Logistic Regression model.
    """

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                NUMERIC_FEATURES
            ),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES
            )
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                    random_state=42
                )
            )
        ]
    )

    return model


def train_model(X_train, y_train):
    """
    Train the RecoverAI model.
    """

    model = create_model()

    model.fit(
        X_train,
        y_train
    )

    return model
