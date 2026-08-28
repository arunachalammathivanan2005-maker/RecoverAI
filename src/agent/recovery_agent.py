import joblib
import pandas as pd
from pathlib import Path


# Locate the trained RecoverAI model
MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "recovery_model.pkl"
)


# Load the trained model
model = joblib.load(MODEL_PATH)


def predict_recovery(transaction):
    """
    Predict the recovery probability for a failed transaction.
    """

    # Convert dictionary to pandas DataFrame
    if isinstance(transaction, dict):
        transaction = pd.DataFrame([transaction])

    probability = model.predict_proba(
        transaction
    )[0, 1]

    return probability


def get_recovery_action(probability, failure_reason):
    """
    Decide the best recovery action.
    """

    if probability >= 0.75:
        return "RETRY_NOW"

    elif probability >= 0.50:

        if failure_reason == "Network Timeout":
            return "RETRY_LATER"

        elif failure_reason == "Gateway Error":
            return "RETRY_WITH_ALTERNATE_GATEWAY"

        elif failure_reason == "Authentication Failure":
            return "REQUEST_AUTHENTICATION"

        elif failure_reason == "Insufficient Funds":
            return "SUGGEST_ALTERNATE_PAYMENT"

        elif failure_reason == "Expired Card":
            return "REQUEST_CARD_UPDATE"

        elif failure_reason == "Bank Decline":
            return "SUGGEST_ALTERNATE_PAYMENT"

    return "STOP"


def analyze_transaction(transaction, failure_reason):
    """
    Analyze a failed transaction and return
    a recovery recommendation.
    """

    # Get recovery probability from ML model
    probability = predict_recovery(transaction)

    # Decide the best recovery action
    action = get_recovery_action(
        probability,
        failure_reason
    )

    return {
        "recovery_probability": probability,
        "failure_reason": failure_reason,
        "recommended_action": action
    }