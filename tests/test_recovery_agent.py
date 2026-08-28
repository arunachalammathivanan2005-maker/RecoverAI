from src.agent.recovery_agent import analyze_transaction


def test_recovery_agent():

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

    result = analyze_transaction(
        transaction,
        "Gateway Error"
    )

    print("\nRecoverAI Agent Test")
    print("=" * 40)
    print(f"Recovery Probability: {result['recovery_probability']:.4f}")
    print(f"Failure Reason: {result['failure_reason']}")
    print(f"Recommended Action: {result['recommended_action']}")

    assert 0 <= result["recovery_probability"] <= 1
    assert result["recommended_action"] in [
        "RETRY_NOW",
        "RETRY_LATER",
        "RETRY_WITH_ALTERNATE_GATEWAY",
        "REQUEST_AUTHENTICATION",
        "SUGGEST_ALTERNATE_PAYMENT",
        "REQUEST_CARD_UPDATE",
        "STOP"
    ]
if __name__ == "__main__":
    test_recovery_agent()