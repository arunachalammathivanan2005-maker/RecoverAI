import numpy as np
import pandas as pd
from pathlib import Path

# Make the dataset reproducible
np.random.seed(42)

# Number of synthetic transactions
NUM_TRANSACTIONS = 10_000
# Number of unique customers
NUM_CUSTOMERS = 3_000

# Generate customer IDs
customer_ids = np.arange(1, NUM_CUSTOMERS + 1)

# Assign each transaction to a customer
transaction_customer_ids = np.random.choice(
    customer_ids,
    size=NUM_TRANSACTIONS
)

# Generate payment history for each customer
customer_previous_success = np.random.poisson(
    lam=8,
    size=NUM_CUSTOMERS
)

customer_previous_failure = np.random.poisson(
    lam=2,
    size=NUM_CUSTOMERS
)

# Calculate each customer's historical success rate
customer_total_attempts = (
    customer_previous_success +
    customer_previous_failure
)

customer_success_rate = np.divide(
    customer_previous_success,
    customer_total_attempts,
    out=np.zeros(NUM_CUSTOMERS, dtype=float),
    where=customer_total_attempts != 0
)

# Map each customer's history to their transactions
customer_index = transaction_customer_ids - 1

previous_success_count = customer_previous_success[customer_index]
previous_failure_count = customer_previous_failure[customer_index]
historical_success_rate = customer_success_rate[customer_index]


# Generate transaction IDs
transaction_ids = [
    f"TXN_{i:06d}" for i in range(1, NUM_TRANSACTIONS + 1)
]


# Generate transaction amounts
amounts = np.round(
    np.random.lognormal(mean=6.5, sigma=0.8, size=NUM_TRANSACTIONS),
    2
)

# Keep transaction amounts within a reasonable range
amounts = np.clip(amounts, 100, 50_000)
# Generate payment methods
payment_methods = np.random.choice(
    ["UPI", "Credit Card", "Debit Card", "Net Banking", "Wallet"],
    size=NUM_TRANSACTIONS,
    p=[0.45, 0.25, 0.15, 0.10, 0.05]
)
# Generate payment failure reasons
failure_reasons = np.random.choice(
    [
        "Insufficient Funds",
        "Network Timeout",
        "Bank Decline",
        "Expired Card",
        "Authentication Failure",
        "Gateway Error"
    ],
    size=NUM_TRANSACTIONS,
    p=[0.20, 0.20, 0.15, 0.10, 0.15, 0.20]
)
# Generate number of previous retry attempts
retry_count = np.random.poisson(
    lam=1.2,
    size=NUM_TRANSACTIONS
)

# Keep retry count between 0 and 5
retry_count = np.clip(retry_count, 0, 5)
# Generate device types
device_types = np.random.choice(
    ["Mobile", "Desktop", "Tablet"],
    size=NUM_TRANSACTIONS,
    p=[0.65, 0.30, 0.05]
)
# Generate transaction channels
channels = np.random.choice(
    ["App", "Web"],
    size=NUM_TRANSACTIONS,
    p=[0.70, 0.30]
)
# Generate transaction hour
transaction_hours = np.random.randint(
    0,
    24,
    size=NUM_TRANSACTIONS
)
# Start with a base recovery score
recovery_score = np.full(
    NUM_TRANSACTIONS,
    0.50,
    dtype=float
)
# Customer history adjustment
recovery_score += (
    historical_success_rate - 0.50
) * 0.60
# Failure reason adjustment
recovery_score += np.select(
    [
        failure_reasons == "Network Timeout",
        failure_reasons == "Gateway Error",
        failure_reasons == "Authentication Failure",
        failure_reasons == "Bank Decline",
        failure_reasons == "Insufficient Funds",
        failure_reasons == "Expired Card"
    ],
    [
        0.18,
        0.15,
        0.05,
        -0.10,
        -0.15,
        -0.25
    ],
    default=0.0
)
# Retry count adjustment
recovery_score -= retry_count * 0.07
# Transaction amount adjustment
amount_factor = np.clip(
    (amounts - 5_000) / 20_000,
    -1,
    1
)

recovery_score -= amount_factor * 0.05
# Keep recovery probability between 0 and 1
recovery_probability = np.clip(
    recovery_score,
    0.05,
    0.95
)
# Simulate whether the payment is recovered
recovered = np.random.binomial(
    1,
    recovery_probability
)
# Calculate recovered revenue
recovered_amount = np.where(
    recovered == 1,
    amounts,
    0
)
# Create the final transaction DataFrame
df = pd.DataFrame({
    "transaction_id": transaction_ids,
    "customer_id": transaction_customer_ids,
    "amount": amounts,
    "payment_method": payment_methods,
    "failure_reason": failure_reasons,
    "retry_count": retry_count,
    "previous_success_count": previous_success_count,
    "previous_failure_count": previous_failure_count,
    "historical_success_rate": historical_success_rate,
    "device_type": device_types,
    "channel": channels,
    "transaction_hour": transaction_hours,
    "recovery_probability": recovery_probability,
    "recovered": recovered,
    "recovered_amount": recovered_amount
})
# Define the output directory
output_dir = Path("data/raw")

# Create the directory if it doesn't exist
output_dir.mkdir(parents=True, exist_ok=True)
# Save the dataset as a CSV file
output_file = output_dir / "payment_transactions.csv"

df.to_csv(
    output_file,
    index=False
)
# Display dataset information
print(f"Dataset created successfully: {output_file}")
print(f"Number of rows: {len(df):,}")
print(f"Number of columns: {len(df.columns)}")
print("\nFirst 5 rows:")
print(df.head())

