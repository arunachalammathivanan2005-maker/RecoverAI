import sys
import textwrap
from pathlib import Path

import streamlit as st
import pandas as pd


# ============================================================
# 1. PROJECT PATH
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ============================================================
# 2. IMPORT RECOVERY ENGINE
# ============================================================

try:
    from src.recovery.recovery_engine import execute_recovery
except Exception as e:
    execute_recovery = None
    ENGINE_ERROR = str(e)


# ============================================================
# 3. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RecoverAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 4. HTML HELPER
# ============================================================

def render_html(html):
    st.html(textwrap.dedent(html).strip())


# ============================================================
# 5. LOAD DATASET
# ============================================================

DATA_PATH = (
    ROOT_DIR
    / "data"
    / "raw"
    / "payment_transactions.csv"
)

try:
    df = pd.read_csv(DATA_PATH)
except Exception:
    df = pd.DataFrame()


# ============================================================
# 6. DATASET METRICS
# ============================================================

total_transactions = len(df)

recovered_transactions = 0
recovery_rate = 0.0
recovered_revenue = 0.0


if not df.empty:

    # --------------------------------------------------------
    # Find recovery column
    # --------------------------------------------------------

    recovery_column = None

    possible_recovery_columns = [
        "recovered",
        "is_recovered",
        "recovered_transaction",
        "recovery_status",
        "recovered_amount",
    ]

    for column in possible_recovery_columns:

        if column in df.columns:
            recovery_column = column
            break


    # --------------------------------------------------------
    # Calculate recovery metrics
    # --------------------------------------------------------

    if recovery_column:

        values = df[recovery_column]

        if recovery_column == "recovered_amount":

            recovered_mask = values.fillna(0) > 0

            recovered_transactions = int(
                recovered_mask.sum()
            )

            recovered_revenue = float(
                values.fillna(0).sum()
            )

        else:

            recovered_mask = (
                values.astype(str)
                .str.lower()
                .isin(
                    [
                        "1",
                        "true",
                        "yes",
                        "recovered",
                        "success",
                        "successful",
                    ]
                )
            )

            recovered_transactions = int(
                recovered_mask.sum()
            )

            if "amount" in df.columns:

                recovered_revenue = float(
                    df.loc[
                        recovered_mask,
                        "amount"
                    ].sum()
                )


    # --------------------------------------------------------
    # Recovery rate
    # --------------------------------------------------------

    if total_transactions > 0:

        recovery_rate = (
            recovered_transactions
            / total_transactions
        ) * 100


# ============================================================
# 7. CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   GLOBAL
   ========================================================== */

.stApp {

    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(25, 100, 255, 0.15),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(140, 50, 255, 0.13),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #050811,
            #080b14
        );

    color: #f5f7fb;
}


/* Main container */

.block-container {

    max-width: 1450px;

    padding-top: 2rem;
    padding-bottom: 5rem;
}


/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* ==========================================================
   HERO
   ========================================================== */

.hero {

    padding: 55px 55px;

    border-radius: 30px;

    margin-bottom: 42px;

    background:
        linear-gradient(
            135deg,
            rgba(17, 35, 70, 0.98),
            rgba(11, 17, 32, 0.98)
        );

    border:
        1px solid
        rgba(85, 145, 255, 0.28);

    box-shadow:
        0 25px 80px
        rgba(0, 0, 0, 0.45),

        inset 0 1px 0
        rgba(255,255,255,0.04);
}


/* Hero title */

.hero-title {

    font-size: 58px;

    font-weight: 850;

    letter-spacing: -2px;

    line-height: 1.1;

    margin-bottom: 14px;
}


.hero-title span {

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #74a9ff,
            #b68cff
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}


/* Subtitle */

.hero-subtitle {

    font-size: 21px;

    color: #aebbd3;

    margin-bottom: 25px;
}


/* Status */

.status-pill {

    display: inline-block;

    padding: 9px 18px;

    border-radius: 999px;

    background:
        rgba(30, 220, 130, 0.08);

    border:
        1px solid
        rgba(30, 220, 130, 0.25);

    color: #55e59a;

    font-size: 13px;

    font-weight: 700;

    letter-spacing: 1px;
}


/* ==========================================================
   SECTION TITLE
   ========================================================== */

.section-title {

    font-size: 29px;

    font-weight: 800;

    margin-top: 20px;

    margin-bottom: 22px;

    letter-spacing: -0.5px;
}


/* ==========================================================
   KPI CARDS
   ========================================================== */

.kpi-card {

    min-height: 165px;

    padding: 28px;

    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(17, 27, 50, 0.98),
            rgba(9, 15, 29, 0.98)
        );

    border:
        1px solid
        rgba(100, 135, 190, 0.18);

    box-shadow:
        0 15px 45px
        rgba(0,0,0,0.30);

    transition:
        transform 0.2s ease,
        border-color 0.2s ease;
}


.kpi-card:hover {

    transform:
        translateY(-4px);

    border-color:
        rgba(100, 160, 255, 0.40);
}


.kpi-label {

    color: #8fa7cc;

    font-size: 12px;

    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 1.2px;
}


.kpi-value {

    font-size: 38px;

    font-weight: 850;

    margin-top: 12px;
}


.kpi-description {

    color: #7084a8;

    font-size: 13px;

    margin-top: 7px;
}


/* ==========================================================
   PANELS
   ========================================================== */

.panel {

    padding: 30px;

    border-radius: 25px;

    background:
        linear-gradient(
            145deg,
            rgba(16, 26, 48, 0.96),
            rgba(8, 14, 27, 0.96)
        );

    border:
        1px solid
        rgba(100, 140, 210, 0.20);

    box-shadow:
        0 20px 60px
        rgba(0,0,0,0.30);
}


/* ==========================================================
   AI RESULT
   ========================================================== */

.ai-result {

    padding: 34px;

    border-radius: 27px;

    background:
        radial-gradient(
            circle at top right,
            rgba(90, 120, 255, 0.20),
            transparent 45%
        ),
        linear-gradient(
            145deg,
            #111c33,
            #080e1b
        );

    border:
        1px solid
        rgba(105, 150, 255, 0.30);

    box-shadow:
        0 25px 80px
        rgba(0,0,0,0.42);
}


.probability-label {

    color: #91a7cc;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 1.5px;
}


.probability {

    font-size: 58px;

    font-weight: 900;

    margin-top: 5px;
}


.recovery-level {

    font-size: 16px;

    font-weight: 700;

    color: #8ea6cb;

    margin-top: 8px;

    margin-bottom: 25px;
}


/* ==========================================================
   ACTION CARDS
   ========================================================== */

.action-card {

    padding: 18px 20px;

    margin-top: 12px;

    border-radius: 16px;

    background:
        rgba(255,255,255,0.035);

    border:
        1px solid
        rgba(255,255,255,0.07);
}


.action-label {

    color: #8498ba;

    font-size: 11px;

    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 1px;
}


.action-value {

    font-size: 21px;

    font-weight: 800;

    margin-top: 7px;
}


/* ==========================================================
   ANALYSIS CARD
   ========================================================== */

.analysis-card {

    padding: 28px;

    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(15,25,46,0.96),
            rgba(8,13,25,0.96)
        );

    border:
        1px solid
        rgba(100,140,210,0.18);

    margin-top: 25px;
}


/* ==========================================================
   FOOTER
   ========================================================== */

.footer {

    text-align: center;

    color: #536580;

    margin-top: 60px;

    font-size: 13px;

    line-height: 1.8;
}


/* ==========================================================
   STREAMLIT INPUTS
   ========================================================== */

div[data-baseweb="select"] > div {

    background-color:
        rgba(20, 25, 40, 0.95);
}


div[data-testid="stNumberInput"] input {

    background-color:
        rgba(20, 25, 40, 0.95);
}


div[data-testid="stSlider"] {

    padding-top: 10px;
}


/* Button */

.stButton > button {

    height: 55px;

    border-radius: 15px;

    font-size: 16px;

    font-weight: 800;

    border: none;

    box-shadow:
        0 10px 30px
        rgba(50,100,255,0.20);
}


</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# 8. HERO
# ============================================================

render_html(
    """
    <div class="hero">

        <div class="hero-title">
            🤖 <span>RecoverAI</span>
        </div>

        <div class="hero-subtitle">
            AI-Powered Payment Recovery Intelligence
        </div>

        <div class="status-pill">
            ● AI ENGINE ONLINE
        </div>

    </div>
    """
)


# ============================================================
# 9. RECOVERY INTELLIGENCE
# ============================================================

render_html(
    """
    <div class="section-title">
        📊 Recovery Intelligence
    </div>
    """
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Transactions
            </div>

            <div class="kpi-value">
                {total_transactions:,}
            </div>

            <div class="kpi-description">
                Analyzed transactions
            </div>

        </div>
        """
    )


with col2:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Recovery Rate
            </div>

            <div class="kpi-value">
                {recovery_rate:.2f}%
            </div>

            <div class="kpi-description">
                Successful recoveries
            </div>

        </div>
        """
    )


with col3:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Recovered
            </div>

            <div class="kpi-value">
                {recovered_transactions:,}
            </div>

            <div class="kpi-description">
                Transactions recovered
            </div>

        </div>
        """
    )


with col4:

    revenue_lakh = recovered_revenue / 100000

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Recovered Revenue
            </div>

            <div class="kpi-value">
                ₹{revenue_lakh:.2f}L
            </div>

            <div class="kpi-description">
                Potentially recovered value
            </div>

        </div>
        """
    )


# ============================================================
# 10. TRANSACTION INTELLIGENCE
# ============================================================

render_html(
    """
    <div class="section-title">
        ⚡ Transaction Intelligence
    </div>
    """
)


left_col, right_col = st.columns(
    [1.05, 0.95],
    gap="large"
)


# ============================================================
# 11. LEFT SIDE — TRANSACTION
# ============================================================

with left_col:

    render_html(
        """
        <div class="panel">

            <div class="section-title">
                💳 Transaction Details
            </div>

        </div>
        """
    )

    amount = st.number_input(
        "Transaction Amount (₹)",
        min_value=1.0,
        value=10000.0,
        step=100.0
    )

    payment_method = st.selectbox(
        "Payment Method",
        [
            "UPI",
            "Credit Card",
            "Debit Card",
            "Net Banking",
            "Wallet"
        ]
    )

    failure_reason = st.selectbox(
        "Failure Reason",
        [
            "Network Timeout",
            "Gateway Error",
            "Authentication Failure",
            "Insufficient Funds",
            "Expired Card",
            "Bank Decline"
        ]
    )

    retry_count = st.number_input(
        "Retry Attempts",
        min_value=0,
        max_value=10,
        value=3,
        step=1
    )


# ============================================================
# 12. RIGHT SIDE — CUSTOMER HISTORY
# ============================================================

with right_col:

    render_html(
        """
        <div class="panel">

            <div class="section-title">
                🧠 Customer Intelligence
            </div>

        </div>
        """
    )

    previous_success_count = st.number_input(
        "Previous Successful Payments",
        min_value=0,
        value=10,
        step=1
    )

    previous_failure_count = st.number_input(
        "Previous Failed Payments",
        min_value=0,
        value=5,
        step=1
    )

    device_type = st.selectbox(
        "Device Type",
        [
            "Mobile",
            "Desktop",
            "Tablet"
        ]
    )

    channel = st.selectbox(
        "Transaction Channel",
        [
            "App",
            "Web",
            "POS"
        ]
    )

    transaction_hour = st.slider(
        "Transaction Hour",
        min_value=0,
        max_value=23,
        value=14
    )


# ============================================================
# 13. ANALYZE BUTTON
# ============================================================

st.write("")

button_left, button_center, button_right = st.columns(
    [1, 2, 1]
)


with button_center:

    analyze = st.button(
        "🚀  ANALYZE PAYMENT",
        use_container_width=True,
        type="primary"
    )


# ============================================================
# 14. RUN AI ANALYSIS
# ============================================================

if analyze:

    # --------------------------------------------------------
    # Transaction data
    # --------------------------------------------------------

    # Calculate historical success rate
    historical_total = (
            previous_success_count
            + previous_failure_count
    )

    if historical_total > 0:
        historical_success_rate = (
                previous_success_count
                / historical_total
        )
    else:
        historical_success_rate = 0.0

    # Calculate historical success rate
    historical_total = (
            previous_success_count
            + previous_failure_count
    )

    if historical_total > 0:
        historical_success_rate = (
                previous_success_count / historical_total
        )
    else:
        historical_success_rate = 0.0

    # Build transaction data
    transaction = {
        "amount": amount,

        "previous_success_count":
            previous_success_count,

        "previous_failure_count":
            previous_failure_count,

        "historical_success_rate":
            historical_success_rate,

        "retry_count":
            retry_count,

        "payment_method":
            payment_method,

        "failure_reason":
            failure_reason,

        "device_type":
            device_type,

        "channel":
            channel,

        "transaction_hour":
            transaction_hour
    }


    # --------------------------------------------------------
    # Check engine
    # --------------------------------------------------------

    if execute_recovery is None:

        st.error(
            "Recovery engine could not be imported."
        )

        st.code(ENGINE_ERROR)

        st.stop()


    # --------------------------------------------------------
    # Execute recovery
    # --------------------------------------------------------

    try:

        result = execute_recovery(
            transaction,
            failure_reason
        )

    except TypeError:

        # Compatibility fallback if your engine
        # accepts only the transaction dictionary.

        try:

            transaction["failure_reason"] = (
                failure_reason
            )

            result = execute_recovery(
                transaction
            )

        except Exception as e:

            st.error(
                f"Recovery engine error: {e}"
            )

            st.stop()

    except Exception as e:

        st.error(
            f"Recovery engine error: {e}"
        )

        st.stop()


    # ========================================================
    # 15. EXTRACT RESULT
    # ========================================================

    probability = float(
        result.get(
            "recovery_probability",
            0
        )
    )

    action = result.get(
        "recommended_action",
        "STOP"
    )

    execution_status = result.get(
        "execution_status",
        None
    )


    # --------------------------------------------------------
    # Generate execution status if engine doesn't return it
    # --------------------------------------------------------

    if execution_status is None:

        status_map = {

            "RETRY_NOW":
                "RETRY_INITIATED",

            "RETRY_LATER":
                "RETRY_SCHEDULED",

            "RETRY_WITH_ALTERNATE_GATEWAY":
                "ALTERNATE_GATEWAY_SELECTED",

            "REQUEST_AUTHENTICATION":
                "AUTHENTICATION_REQUIRED",

            "SUGGEST_ALTERNATE_PAYMENT":
                "ALTERNATE_PAYMENT_SUGGESTED",

            "REQUEST_CARD_UPDATE":
                "CARD_UPDATE_REQUIRED",

            "STOP":
                "RECOVERY_STOPPED"
        }

        execution_status = status_map.get(
            action,
            "RECOVERY_STOPPED"
        )


    # ========================================================
    # 16. RECOVERY LEVEL
    # ========================================================

    if probability >= 0.75:

        recovery_level = "HIGH RECOVERY"
        recovery_symbol = "🟢"

    elif probability >= 0.50:

        recovery_level = "MEDIUM RECOVERY"
        recovery_symbol = "🟡"

    else:

        recovery_level = "LOW RECOVERY"
        recovery_symbol = "🔴"


    # ========================================================
    # 17. RECOMMENDATION
    # ========================================================

    render_html(
        f"""
        <div class="section-title">

            🤖 RecoverAI Recommendation

        </div>

        <div class="ai-result">

            <div class="probability-label">

                AI RECOVERY PROBABILITY

            </div>

            <div class="probability">

                {probability * 100:.2f}%

            </div>
<div style="
    margin-top: 18px;
    margin-bottom: 25px;
">

    <div style="
        display:flex;
        justify-content:space-between;
        font-size:12px;
        color:#8fa8d6;
        margin-bottom:8px;
        letter-spacing:1px;
    ">
        <span>LOW RECOVERY</span>
        <span>AI CONFIDENCE</span>
        <span>HIGH RECOVERY</span>
    </div>

    <div style="
        width:100%;
        height:12px;
        background:#182238;
        border-radius:20px;
        overflow:hidden;
        border:1px solid rgba(120,150,220,0.15);
    ">

        <div style="
            width:{max(3, min(probability * 100, 100)):.2f}%;
            height:100%;
            border-radius:20px;
            background:linear-gradient(
                90deg,
                #ff4d5a,
                #ffc857,
                #35e58a
            );
            box-shadow:0 0 15px rgba(80,160,255,0.35);
        ">
        </div>

    </div>

    <div style="
        display:flex;
        justify-content:space-between;
        margin-top:8px;
        font-size:12px;
        color:#657da8;
    ">
        <span>0%</span>
        <span>50%</span>
        <span>100%</span>
    </div>

</div>
            <div class="recovery-level">

                {recovery_symbol}
                {recovery_level}

            </div>


            <div class="action-card">

                <div class="action-label">

                    Recommended Action

                </div>

                <div class="action-value">

                    {action}

                </div>

            </div>


            <div class="action-card">

                <div class="action-label">

                    Execution Status

                </div>

                <div class="action-value">

                    {execution_status}

                </div>

            </div>

        </div>
        """
    )
    # ========================================================
    # 17.5 AI DECISION EXPLANATION
    # ========================================================

    # Determine explanation based on the model decision
    if action == "RETRY_NOW":
        decision_reason = (
            "The AI estimates a high probability of recovery. "
            "An immediate retry is therefore recommended."
        )

        decision_factors = [
            ("Recovery confidence", f"{probability * 100:.2f}%", "HIGH"),
            ("Failure type", failure_reason, "RETRYABLE"),
            ("Recommended strategy", "Immediate retry", "ACTION"),
        ]

    elif action == "RETRY_LATER":
        decision_reason = (
            "The AI detected a moderate recovery probability. "
            "Because the failure may be temporary, RecoverAI recommends "
            "waiting before attempting the transaction again."
        )

        decision_factors = [
            ("Recovery confidence", f"{probability * 100:.2f}%", "MEDIUM"),
            ("Failure type", failure_reason, "TEMPORARY"),
            ("Recommended strategy", "Scheduled retry", "ACTION"),
        ]

    elif action == "RETRY_WITH_ALTERNATE_GATEWAY":
        decision_reason = (
            "The current payment gateway may be responsible for the failure. "
            "RecoverAI recommends attempting recovery through an alternate gateway."
        )

        decision_factors = [
            ("Recovery confidence", f"{probability * 100:.2f}%", "MEDIUM"),
            ("Failure type", failure_reason, "GATEWAY"),
            ("Recommended strategy", "Alternate gateway", "ACTION"),
        ]

    elif action == "REQUEST_AUTHENTICATION":
        decision_reason = (
            "The transaction requires additional customer authentication "
            "before another recovery attempt should be made."
        )

        decision_factors = [
            ("Recovery confidence", f"{probability * 100:.2f}%", "MEDIUM"),
            ("Failure type", failure_reason, "AUTH"),
            ("Recommended strategy", "Customer authentication", "ACTION"),
        ]

    elif action == "SUGGEST_ALTERNATE_PAYMENT":
        decision_reason = (
            "The current payment method has a low chance of succeeding. "
            "RecoverAI recommends using an alternate payment method."
        )

        decision_factors = [
            ("Recovery confidence", f"{probability * 100:.2f}%", "MEDIUM"),
            ("Failure type", failure_reason, "PAYMENT"),
            ("Recommended strategy", "Alternate payment", "ACTION"),
        ]

    elif action == "REQUEST_CARD_UPDATE":
        decision_reason = (
            "The payment method appears to require an update before "
            "another transaction attempt can succeed."
        )

        decision_factors = [
            ("Recovery confidence", f"{probability * 100:.2f}%", "MEDIUM"),
            ("Failure type", failure_reason, "CARD"),
            ("Recommended strategy", "Update payment method", "ACTION"),
        ]

    else:
        decision_reason = (
            "The predicted recovery probability is too low to justify "
            "another automated recovery attempt."
        )

        decision_factors = [
            ("Recovery confidence", f"{probability * 100:.2f}%", "LOW"),
            ("Failure type", failure_reason, "RISK"),
            ("Recommended strategy", "Stop recovery", "ACTION"),
        ]


    render_html(
        f"""
        <div class="analysis-card">

            <div class="section-title">
                🧠 Why RecoverAI Made This Decision
            </div>

            <div class="action-card">

                <div class="action-label">
                    AI Reasoning
                </div>

                <div style="
                    font-size:18px;
                    line-height:1.7;
                    color:#dbe5f7;
                    margin-top:10px;
                ">
                    {decision_reason}
                </div>

            </div>

            <div style="
                display:grid;
                grid-template-columns:repeat(3,1fr);
                gap:14px;
                margin-top:16px;
            ">

                <div class="action-card">
                    <div class="action-label">
                        {decision_factors[0][0]}
                    </div>

                    <div class="action-value">
                        {decision_factors[0][1]}
                    </div>
                </div>


                <div class="action-card">
                    <div class="action-label">
                        {decision_factors[1][0]}
                    </div>

                    <div class="action-value">
                        {decision_factors[1][1]}
                    </div>
                </div>


                <div class="action-card">
                    <div class="action-label">
                        {decision_factors[2][0]}
                    </div>

                    <div class="action-value">
                        {decision_factors[2][1]}
                    </div>
                </div>

            </div>

            <div style="
                margin-top:22px;
                padding:18px;
                border-radius:16px;
                background:rgba(90,120,255,0.08);
                border:1px solid rgba(90,140,255,0.16);
            ">

                <div class="action-label">
                    DECISION PIPELINE
                </div>

                <div style="
                    margin-top:12px;
                    font-size:15px;
                    color:#a9bbd8;
                ">
                    Transaction Data
                    <span style="color:#647cff;"> → </span>
                    ML Prediction
                    <span style="color:#647cff;"> → </span>
                    Recovery Probability
                    <span style="color:#647cff;"> → </span>
                    Decision Engine
                    <span style="color:#647cff;"> → </span>
                    <strong style="color:#ffffff;">
                        {action}
                    </strong>
                </div>

            </div>

        </div>
        """
    )
    # ========================================================
    # 17.6 AI KEY FACTORS
    # ========================================================
    # ========================================================
    # CALCULATE HISTORICAL SUCCESS RATE
    # ========================================================

    historical_total = (
            previous_success_count
            + previous_failure_count
    )

    if historical_total > 0:
        historical_rate = (
                                  previous_success_count
                                  / historical_total
                          ) * 100
    else:
        historical_rate = 0
    # ========================================================
    # 17.7 RECOVERY ANALYTICS
    # ========================================================

    estimated_recovery_value = amount * probability

    if probability >= 0.75:
        risk_label = "LOW RISK"
        risk_symbol = "🟢"
    elif probability >= 0.50:
        risk_label = "MODERATE RISK"
        risk_symbol = "🟡"
    else:
        risk_label = "HIGH RISK"
        risk_symbol = "🔴"

    render_html(
        f"""
        <div class="analysis-card">

            <div class="section-title">
                📈 Recovery Analytics
            </div>

            <div style="
                display:grid;
                grid-template-columns:repeat(3,1fr);
                gap:16px;
                margin-top:20px;
            ">

                <!-- Estimated Recovery -->
                <div class="action-card">

                    <div class="action-label">
                        ESTIMATED RECOVERABLE VALUE
                    </div>

                    <div class="action-value">
                        ₹{estimated_recovery_value:,.2f}
                    </div>

                    <div style="
                        margin-top:10px;
                        color:#8fa8d6;
                        font-size:13px;
                    ">
                        Based on predicted recovery probability
                    </div>

                </div>


                <!-- Recovery Probability -->
                <div class="action-card">

                    <div class="action-label">
                        RECOVERY PROBABILITY
                    </div>

                    <div class="action-value">
                        {probability * 100:.2f}%
                    </div>

                    <div style="
                        margin-top:10px;
                        color:#8fa8d6;
                        font-size:13px;
                    ">
                        ML model prediction
                    </div>

                </div>


                <!-- Risk -->
                <div class="action-card">

                    <div class="action-label">
                        RECOVERY RISK
                    </div>

                    <div class="action-value">
                        {risk_symbol} {risk_label}
                    </div>

                    <div style="
                        margin-top:10px;
                        color:#8fa8d6;
                        font-size:13px;
                    ">
                        Decision risk classification
                    </div>

                </div>

            </div>


            <!-- Recovery Progress -->
            <div style="
                margin-top:22px;
                padding:20px;
                border-radius:16px;
                background:rgba(20,35,70,0.55);
                border:1px solid rgba(100,130,255,0.15);
            ">

                <div class="action-label">
                    RECOVERY POTENTIAL
                </div>

                <div style="
                    margin-top:12px;
                    height:10px;
                    width:100%;
                    background:#182238;
                    border-radius:20px;
                    overflow:hidden;
                ">

                    <div style="
                        width:{max(2, min(probability * 100, 100)):.2f}%;
                        height:100%;
                        background:linear-gradient(
                            90deg,
                            #ff4d5a,
                            #ffc857,
                            #35e58a
                        );
                        border-radius:20px;
                    ">
                    </div>

                </div>

                <div style="
                    display:flex;
                    justify-content:space-between;
                    margin-top:8px;
                    color:#7188b2;
                    font-size:12px;
                ">
                    <span>0%</span>
                    <span>{probability * 100:.2f}% predicted</span>
                    <span>100%</span>
                </div>

            </div>

        </div>
        """
    )

    # ========================================================
    # 17.8 WHAT HAPPENS NEXT
    # ========================================================

    render_html(
        f"""
        <div class="analysis-card">

            <div class="section-title">
                ⚡ What Happens Next?
            </div>

            <div style="
                display:grid;
                grid-template-columns:repeat(4,1fr);
                gap:12px;
                margin-top:22px;
            ">

                <div class="action-card"
                     style="text-align:center;">

                    <div style="
                        font-size:30px;
                        margin-bottom:10px;
                    ">
                        1️⃣
                    </div>

                    <div class="action-label">
                        ANALYZE
                    </div>

                    <div style="
                        margin-top:8px;
                        color:#9eb2d5;
                        font-size:13px;
                    ">
                        Transaction data evaluated
                    </div>

                </div>


                <div class="action-card"
                     style="text-align:center;">

                    <div style="
                        font-size:30px;
                        margin-bottom:10px;
                    ">
                        2️⃣
                    </div>

                    <div class="action-label">
                        PREDICT
                    </div>

                    <div style="
                        margin-top:8px;
                        color:#9eb2d5;
                        font-size:13px;
                    ">
                        ML predicts recovery probability
                    </div>

                </div>


                <div class="action-card"
                     style="text-align:center;">

                    <div style="
                        font-size:30px;
                        margin-bottom:10px;
                    ">
                        3️⃣
                    </div>

                    <div class="action-label">
                        DECIDE
                    </div>

                    <div style="
                        margin-top:8px;
                        color:#9eb2d5;
                        font-size:13px;
                    ">
                        Recovery engine selects action
                    </div>

                </div>


                <div class="action-card"
                     style="text-align:center;
                            border-color:rgba(80,150,255,0.35);">

                    <div style="
                        font-size:30px;
                        margin-bottom:10px;
                    ">
                        4️⃣
                    </div>

                    <div class="action-label">
                        EXECUTE
                    </div>

                    <div style="
                        margin-top:8px;
                        color:#ffffff;
                        font-size:14px;
                        font-weight:700;
                    ">
                        {execution_status}
                    </div>

                </div>

            </div>


            <div style="
                margin-top:20px;
                padding:18px 20px;
                border-radius:16px;
                background:linear-gradient(
                    135deg,
                    rgba(70,100,255,0.10),
                    rgba(30,210,170,0.06)
                );
                border:1px solid rgba(90,130,255,0.18);
            ">

                <div class="action-label">
                    CURRENT RECOVERY DECISION
                </div>

                <div style="
                    margin-top:8px;
                    font-size:22px;
                    font-weight:800;
                    color:#ffffff;
                ">
                    {action}
                </div>

                <div style="
                    margin-top:6px;
                    color:#8fa8d6;
                    font-size:14px;
                ">
                    Execution status: {execution_status}
                </div>

            </div>

        </div>
        """
    )
    render_html(
        f"""
        <div class="analysis-card">

            <div class="section-title">
                📊 AI Key Factors
            </div>

            <div style="
                display:grid;
                grid-template-columns:repeat(2,1fr);
                gap:16px;
                margin-top:20px;
            ">

                <!-- Historical Success -->
                <div class="action-card">

                    <div class="action-label">
                        HISTORICAL SUCCESS RATE
                    </div>

                    <div class="action-value">
                        {historical_rate:.2f}%
                    </div>

                    <div style="
                        margin-top:14px;
                        height:7px;
                        background:#182238;
                        border-radius:10px;
                        overflow:hidden;
                    ">

                        <div style="
                            width:{max(2,min(historical_rate,100)):.2f}%;
                            height:100%;
                            background:linear-gradient(
                                90deg,
                                #667cff,
                                #35d6ff
                            );
                            border-radius:10px;
                        ">
                        </div>

                    </div>

                </div>


                <!-- Successful Payments -->
                <div class="action-card">

                    <div class="action-label">
                        PREVIOUS SUCCESSFUL PAYMENTS
                    </div>

                    <div class="action-value">
                        {previous_success_count}
                    </div>

                    <div style="
                        margin-top:14px;
                        color:#8fa8d6;
                        font-size:13px;
                    ">
                        Successful payment history
                    </div>

                </div>


                <!-- Failed Payments -->
                <div class="action-card">

                    <div class="action-label">
                        PREVIOUS FAILED PAYMENTS
                    </div>

                    <div class="action-value">
                        {previous_failure_count}
                    </div>

                    <div style="
                        margin-top:14px;
                        color:#8fa8d6;
                        font-size:13px;
                    ">
                        Historical failure attempts
                    </div>

                </div>


                <!-- Retry Attempts -->
                <div class="action-card">

                    <div class="action-label">
                        RETRY ATTEMPTS
                    </div>

                    <div class="action-value">
                        {retry_count}
                    </div>

                    <div style="
                        margin-top:14px;
                        color:#8fa8d6;
                        font-size:13px;
                    ">
                        Attempts already made
                    </div>

                </div>


                <!-- Failure Type -->
                <div class="action-card">

                    <div class="action-label">
                        FAILURE TYPE
                    </div>

                    <div class="action-value">
                        {failure_reason}
                    </div>

                    <div style="
                        margin-top:14px;
                        color:#8fa8d6;
                        font-size:13px;
                    ">
                        Primary transaction failure signal
                    </div>

                </div>


                <!-- Payment Method -->
                <div class="action-card">

                    <div class="action-label">
                        PAYMENT METHOD
                    </div>

                    <div class="action-value">
                        {payment_method}
                    </div>

                    <div style="
                        margin-top:14px;
                        color:#8fa8d6;
                        font-size:13px;
                    ">
                        Transaction payment channel
                    </div>

                </div>

            </div>


            <!-- AI Summary -->
            <div style="
                margin-top:20px;
                padding:20px;
                border-radius:16px;
                background:linear-gradient(
                    135deg,
                    rgba(72,104,255,0.10),
                    rgba(35,210,170,0.05)
                );
                border:1px solid rgba(100,130,255,0.16);
            ">

                <div class="action-label">
                    🤖 AI ASSESSMENT
                </div>

                <div style="
                    margin-top:10px;
                    color:#dbe5f7;
                    font-size:16px;
                    line-height:1.6;
                ">
                    RecoverAI evaluated the transaction using its
                    historical payment behaviour, failure characteristics,
                    retry history and recovery probability before selecting
                    <strong style="color:#ffffff;">
                        {action}
                    </strong>.
                </div>

            </div>

        </div>
        """
    )
    # ========================================================
    # 18. DECISION ANALYSIS
    # ========================================================

    historical_total = (
        previous_success_count
        + previous_failure_count
    )


    if historical_total > 0:

        historical_rate = (
            previous_success_count
            / historical_total
        ) * 100

    else:

        historical_rate = 0


    st.write("")


    render_html(
        f"""
        <div class="analysis-card">

            <div class="section-title">

                🔎 Decision Analysis

            </div>


            <div class="action-card">

                <div class="action-label">

                    Failure Reason

                </div>

                <div class="action-value">

                    {failure_reason}

                </div>

            </div>


            <div class="action-card">

                <div class="action-label">

                    Transaction Amount

                </div>

                <div class="action-value">

                    ₹{amount:,.2f}

                </div>

            </div>


            <div class="action-card">

                <div class="action-label">

                    Payment Method

                </div>

                <div class="action-value">

                    {payment_method}

                </div>

            </div>


            <div class="action-card">

                <div class="action-label">

                    Retry Attempts

                </div>

                <div class="action-value">

                    {retry_count}

                </div>

            </div>


            <div class="action-card">

                <div class="action-label">

                    Historical Success Rate

                </div>

                <div class="action-value">

                    {historical_rate:.2f}%

                </div>

            </div>


            <div class="action-card">

                <div class="action-label">

                    RecoverAI Decision

                </div>

                <div class="action-value">

                    {action}

                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # 19. USER MESSAGE
    # ========================================================

    if action == "RETRY_NOW":

        st.success(
            "🟢 RecoverAI recommends retrying "
            "the transaction immediately."
        )

    elif action == "STOP":

        st.warning(
            "🔴 RecoverAI recommends stopping "
            "further recovery attempts."
        )

    elif action == "RETRY_LATER":

        st.info(
            "🟡 RecoverAI recommends scheduling "
            "a retry for later."
        )

    elif action == "RETRY_WITH_ALTERNATE_GATEWAY":

        st.info(
            "🔵 RecoverAI recommends using "
            "an alternate payment gateway."
        )

    elif action == "REQUEST_AUTHENTICATION":

        st.info(
            "🔐 RecoverAI recommends requesting "
            "authentication from the customer."
        )

    elif action == "SUGGEST_ALTERNATE_PAYMENT":

        st.info(
            "💳 RecoverAI recommends suggesting "
            "an alternate payment method."
        )

    elif action == "REQUEST_CARD_UPDATE":

        st.info(
            "💳 RecoverAI recommends requesting "
            "a card update."
        )


# ============================================================
# 20. FOOTER
# ============================================================

render_html(
    """
    <div class="footer">

        <strong>RecoverAI</strong>
        <br>

        AI-Powered Payment Recovery System
        <br>

        Intelligent • Data-Driven • Automated

    </div>
    """
)
st.markdown("""
<style>
/* ==========================================================
   FINAL UI POLISH
   ========================================================== */

/* Overall page spacing */
.block-container {
    max-width: 1400px !important;
    padding-top: 1rem !important;
    padding-bottom: 3rem !important;
}

/* Hero */
.hero {
    padding: 38px 42px !important;
    margin-bottom: 28px !important;
    border-radius: 24px !important;
}

/* Hero typography */
.hero-title {
    font-size: 48px !important;
}

.hero-subtitle {
    font-size: 18px !important;
    margin-bottom: 18px !important;
}

/* Section headings */
.section-title {
    font-size: 24px !important;
    margin-top: 14px !important;
    margin-bottom: 16px !important;
}

/* KPI cards */
.kpi-card {
    min-height: 135px !important;
    padding: 22px !important;
    border-radius: 18px !important;
}

.kpi-value {
    font-size: 32px !important;
}

/* General panels */
.panel {
    padding: 24px !important;
    border-radius: 20px !important;
}

/* AI result */
.ai-result {
    padding: 28px !important;
    border-radius: 22px !important;
}

/* Probability */
.probability {
    font-size: 52px !important;
}

/* Action cards */
.action-card {
    padding: 15px 18px !important;
    margin-top: 9px !important;
}

/* Analysis */
.analysis-card {
    padding: 22px !important;
    margin-top: 18px !important;
    border-radius: 19px !important;
}

/* Footer */
.footer {
    margin-top: 35px !important;
}

/* ==========================================================
   RESPONSIVE LAYOUT
   ========================================================== */

@media (max-width: 900px) {

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .hero {
        padding: 28px !important;
    }

    .hero-title {
        font-size: 38px !important;
    }

    .hero-subtitle {
        font-size: 16px !important;
    }

    .section-title {
        font-size: 21px !important;
    }

    .kpi-card {
        min-height: 115px !important;
        padding: 18px !important;
    }

    .kpi-value {
        font-size: 27px !important;
    }

    .ai-result {
        padding: 22px !important;
    }

    .probability {
        font-size: 44px !important;
    }
}
/* ==========================================================
   STREAMLIT INPUTS — FINAL
   ========================================================== */

/* Labels */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label {
    color: #8fa6cc !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    margin-bottom: 6px !important;
}

/* Number input outer box */
div[data-testid="stNumberInput"] > div {
    background: #151c2d !important;
    border: 1px solid #293653 !important;
    border-radius: 10px !important;
    min-height: 44px !important;
}

/* Number input field */
div[data-testid="stNumberInput"] input {
    background: #151c2d !important;
    color: #f4f7ff !important;
    border: none !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* Number input buttons */
div[data-testid="stNumberInput"] button {
    background: #1c263a !important;
    color: #dce7ff !important;
    border: none !important;
}

div[data-testid="stNumberInput"] button:hover {
    background: #263554 !important;
}

/* Selectbox */
/* ==========================================================
   SELECT BOXES — FORCE DARK THEME
   ========================================================== */

div[data-baseweb="select"] {
    width: 100% !important;
}

div[data-baseweb="select"] > div {
    background-color: #151c2d !important;
    background: #151c2d !important;
    border: 1px solid #293653 !important;
    border-radius: 10px !important;
    color: #f4f7ff !important;
    min-height: 44px !important;
}

div[data-baseweb="select"] [role="combobox"] {
    background-color: #151c2d !important;
    color: #f4f7ff !important;
}

div[data-baseweb="select"] [data-baseweb="select"] {
    background-color: #151c2d !important;
}

div[data-baseweb="select"] span {
    color: #f4f7ff !important;
}

div[data-baseweb="select"] svg {
    color: #9fb3d8 !important;
    fill: #9fb3d8 !important;
}

/* Selectbox text */
div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
    color: #f4f7ff !important;
}

/* Selectbox arrow */
div[data-testid="stSelectbox"] svg {
    color: #9fb3d8 !important;
}

/* Slider */
div[data-testid="stSlider"] {
    padding-top: 4px !important;
}

div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
    color: #ff5258 !important;
    font-weight: 800 !important;
}

/* Analyze button */
.stButton > button {
    width: 100% !important;
    height: 48px !important;
    border-radius: 10px !important;
    background: #ff4d55 !important;
    color: white !important;
    border: none !important;
    font-size: 13px !important;
    font-weight: 800 !important;
}

.stButton > button:hover {
    background: #ff6269 !important;
}

/* Compact spacing */
div[data-testid="stNumberInput"],
div[data-testid="stSelectbox"],
div[data-testid="stSlider"] {
    margin-bottom: 8px !important;
}
</style>
""",
unsafe_allow_html=True
)