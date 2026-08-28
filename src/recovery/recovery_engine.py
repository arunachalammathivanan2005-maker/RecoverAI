from src.agent.recovery_agent import analyze_transaction


def execute_recovery(transaction, failure_reason):
    """
    Analyze a failed transaction and determine
    the recovery action to execute.
    """

    # Get AI recommendation
    recommendation = analyze_transaction(
        transaction,
        failure_reason
    )

    probability = recommendation["recovery_probability"]
    action = recommendation["recommended_action"]

    # Simulate the recovery action
    if action == "RETRY_NOW":
        status = "RETRY_INITIATED"

    elif action == "RETRY_LATER":
        status = "RETRY_SCHEDULED"

    elif action == "RETRY_WITH_ALTERNATE_GATEWAY":
        status = "ALTERNATE_GATEWAY_SELECTED"

    elif action == "REQUEST_AUTHENTICATION":
        status = "AUTHENTICATION_REQUIRED"

    elif action == "SUGGEST_ALTERNATE_PAYMENT":
        status = "ALTERNATE_PAYMENT_SUGGESTED"

    elif action == "REQUEST_CARD_UPDATE":
        status = "CARD_UPDATE_REQUIRED"

    else:
        status = "RECOVERY_STOPPED"

    return {
        "recovery_probability": probability,
        "failure_reason": failure_reason,
        "recommended_action": action,
        "execution_status": status
    }