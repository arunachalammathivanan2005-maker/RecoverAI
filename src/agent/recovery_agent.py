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
    Decide the safest recovery action using
    ML recovery probability and failure reason.
    """

    # Normalize the failure reason
    reason = str(failure_reason).strip().lower()

    # ------------------------------------------------------------
    # HIGH RECOVERY PROBABILITY
    # ------------------------------------------------------------
    if probability >= 0.75:

        if reason == "expired card":
            return "REQUEST_CARD_UPDATE"

        elif reason in ["insufficient funds", "bank decline"]:
            return "SUGGEST_ALTERNATE_PAYMENT"

        elif reason == "authentication failure":
            return "REQUEST_AUTHENTICATION"

        elif reason == "gateway error":
            return "RETRY_WITH_ALTERNATE_GATEWAY"

        elif reason == "network timeout":
            return "RETRY_NOW"

        else:
            return "RETRY_NOW"

    # ------------------------------------------------------------
    # MEDIUM RECOVERY PROBABILITY
    # ------------------------------------------------------------
    elif probability >= 0.50:

        if reason == "network timeout":
            return "RETRY_LATER"

        elif reason == "gateway error":
            return "RETRY_WITH_ALTERNATE_GATEWAY"

        elif reason == "authentication failure":
            return "REQUEST_AUTHENTICATION"

        elif reason in ["insufficient funds", "bank decline"]:
            return "SUGGEST_ALTERNATE_PAYMENT"

        elif reason == "expired card":
            return "REQUEST_CARD_UPDATE"

        else:
            return "RETRY_LATER"

    # ------------------------------------------------------------
    # LOW RECOVERY PROBABILITY
    # ------------------------------------------------------------
    else:
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