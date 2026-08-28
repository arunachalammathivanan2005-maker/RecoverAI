from src.recovery.recovery_engine import execute_recovery


def test_recovery_engine():

    transaction = {
        "amount": 5000,
        "retry_count": 1,
        "previous_success_count": 8,
        "previous_failure_count": 2,
        "historical_success_rate": 0.80,
        "transaction_hour": 14,
        "payment_method": "UPI",
        "failure_reason": "Gateway Error",
        "device_type": "Mobile",
        "channel": "App"
    }

    result = execute_recovery(
        transaction,
        "Gateway Error"
    )

    print("\nRecoverAI Recovery Engine Test")
    print("=" * 45)

    print(
        f"Recovery Probability: "
        f"{result['recovery_probability']:.4f}"
    )

    print(
        f"Failure Reason: "
        f"{result['failure_reason']}"
    )

    print(
        f"Recommended Action: "
        f"{result['recommended_action']}"
    )

    print(
        f"Execution Status: "
        f"{result['execution_status']}"
    )

    # Validate probability
    assert 0 <= result["recovery_probability"] <= 1

    # Validate action
    assert result["recommended_action"] in [
        "RETRY_NOW",
        "RETRY_LATER",
        "RETRY_WITH_ALTERNATE_GATEWAY",
        "REQUEST_AUTHENTICATION",
        "SUGGEST_ALTERNATE_PAYMENT",
        "REQUEST_CARD_UPDATE",
        "STOP"
    ]

    # Validate execution status
    assert result["execution_status"] in [
        "RETRY_INITIATED",
        "RETRY_SCHEDULED",
        "ALTERNATE_GATEWAY_SELECTED",
        "AUTHENTICATION_REQUIRED",
        "ALTERNATE_PAYMENT_SUGGESTED",
        "CARD_UPDATE_REQUIRED",
        "RECOVERY_STOPPED"
    ]


if __name__ == "__main__":
    test_recovery_engine()