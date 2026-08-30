# RecoverAI 🚀

## Payment Recovery System

RecoverAI is a project that helps decide what to do when a payment fails.

Instead of retrying every failed payment in the same way, RecoverAI looks at the transaction details, estimates the chance of recovery, and suggests the next step.

For example, depending on the situation, the system may recommend retrying the payment immediately, trying again later, using another gateway, asking the customer to authenticate, or stopping the recovery attempt.

---

## Why I Built This

A failed payment does not always mean that the payment cannot be recovered.

Some failures are temporary, while others may require the customer to take an action. Repeatedly retrying every failed transaction can also result in unnecessary attempts.

The goal of RecoverAI is to make this decision more intelligently by using the transaction information available at the time of failure.

---

## How It Works

The project follows a simple flow:

```text
Failed Payment
      |
Transaction Details
      |
Recovery Prediction
      |
Recovery Decision
      |
Recovery Action
      |
Result on Dashboard

---

## What RecoverAI Can Do

- Analyze failed payment transactions
- Predict recovery probability
- Classify transactions into low, medium, and high recovery levels
- Suggest a suitable recovery action
- Display the result through an interactive dashboard
- Provide recovery analytics
- Run automated tests

---

## Example Results

### Low Recovery

Recovery Probability: 46.70%

Action: STOP

Status: RECOVERY_STOPPED

### Medium Recovery

Recovery Probability: 53.39%

Action: RETRY_LATER

Status: RETRY_SCHEDULED

### High Recovery

Recovery Probability: 84.50%

Action: RETRY_NOW

Status: RETRY_INITIATED

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Streamlit

---

---

## Theme Support

RecoverAI provides both **Light Mode** and **Dark Mode** to make the dashboard comfortable to use in different working environments.

- ☀️ **Light Mode** — Suitable for daytime use and well-lit environments, providing a bright and clear interface.
- 🌙 **Dark Mode** — Designed for users working during night shifts or in low-light environments, making the dashboard more comfortable to view.

Users can choose the mode that best suits their working conditions and personal preference, whether they are using RecoverAI during the day or working late at night.

This user-focused design helps make RecoverAI comfortable and accessible across different work schedules and environments.

---

## How to Run

```powershell
python -m pip install -r requirements.txt
python -m streamlit run dashboard\app.py
```

Run the tests with:

```powershell
python -m pytest -q
```

Current result:

```text
2 passed
```

The tests cover the Recovery Agent and Recovery Engine.

---

## Future Improvements

- Real payment gateway integration
- Automatic retry scheduling
- Customer notifications
- Real-time transaction monitoring
- Multiple payment gateway support
- Model retraining with real transaction data
- API deployment
- Cloud deployment
- More detailed analytics

---

## Built For

RecoverAI was developed as a buildathon project to explore how transaction data and machine learning can be used to make better payment recovery decisions.
