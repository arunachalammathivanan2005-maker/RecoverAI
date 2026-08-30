
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
# DARK MODE SWITCH
# ============================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

st.toggle(
    "🌙 Dark Mode",
    key="dark_mode",
    help="Switch between Light and Dark themes"
)


# ============================================================
# DARK BLUE THEME
# ============================================================

if st.session_state.dark_mode:

    st.markdown(
        """
        <style>

        .stApp {
            background:
                radial-gradient(
                    circle at 10% 5%,
                    rgba(40, 90, 180, 0.25),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 90% 10%,
                    rgba(100, 50, 180, 0.18),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    #050914,
                    #091326,
                    #050914
                ) !important;

            color: #f5f7ff !important;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }

        .stApp p,
        .stApp span,
        .stApp label,
        .stApp h1,
        .stApp h2,
        .stApp h3 {
            color: #f5f7ff !important;
        }

        .hero {
            background:
                linear-gradient(
                    145deg,
                    #101d38,
                    #091326
                ) !important;

            border: 1px solid #315991 !important;

            box-shadow:
                0 20px 50px rgba(0,0,0,.45) !important;
        }

        .hero-title {
            color: #ffffff !important;
        }

        .hero-title span {
            color: #79a9ff !important;
        }

        .hero-subtitle {
            color: #9bbcff !important;
        }

        .section-title {
            color: #ffffff !important;
        }

        .kpi-card {
            background:
                linear-gradient(
                    145deg,
                    #101c33,
                    #0a1326
                ) !important;

            border: 1px solid #263f69 !important;

            box-shadow:
                0 12px 30px rgba(0,0,0,.40) !important;
        }

        .kpi-label {
            color: #7faeff !important;
        }

        .kpi-value {
            color: #ffffff !important;
        }

        .kpi-description {
            color: #8ca3c7 !important;
        }

        .panel,
        .analysis-card,
        .ai-result {
            background:
                linear-gradient(
                    145deg,
                    #0c172c,
                    #080f20
                ) !important;

            border: 1px solid #29466f !important;

            box-shadow:
                0 15px 35px rgba(0,0,0,.42) !important;
        }

        .action-card {
            background: #111c30 !important;
            border: 1px solid #29415f !important;
        }

        .action-label {
            color: #82a7dc !important;
        }

        .action-value {
            color: #ffffff !important;
        }

        .probability-label {
            color: #78a9ff !important;
        }

        .probability {
            color: #ffffff !important;
        }

        .recovery-level {
            color: #9ab8e5 !important;
        }

        div[data-testid="stNumberInput"] > div {
            background: #151e31 !important;
            background-color: #151e31 !important;
            border: 1px solid #385780 !important;
        }

        div[data-testid="stNumberInput"] input {
            background: transparent !important;
            color: #ffffff !important;
            font-weight: 700 !important;
        }

        div[data-testid="stNumberInput"] button {
            background: #1c2b45 !important;
            color: #dce9ff !important;
        }

        div[data-testid="stSelectbox"]
        [data-baseweb="select"] > div {
            background: #151e31 !important;
            background-color: #151e31 !important;
            border: 1px solid #385780 !important;
        }

        div[data-testid="stSelectbox"]
        [data-baseweb="select"]
        span {
            color: #ffffff !important;
        }

        div[data-testid="stSelectbox"]
        [data-baseweb="select"]
        svg {
            color: #8db7ff !important;
            fill: #8db7ff !important;
        }

        div[data-testid="stNumberInput"] label,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSlider"] label {
            color: #91b8f0 !important;
            font-weight: 750 !important;
        }

        div[data-testid="stSlider"]
        [data-testid="stSliderThumbValue"] {
            color: #ff5260 !important;
            font-weight: 850 !important;
        }

        .stButton > button {
            background:
                linear-gradient(
                    135deg,
                    #ff4f5e,
                    #e83f50
                ) !important;

            color: white !important;

            border: 1px solid #ff6875 !important;

            box-shadow:
                0 12px 30px rgba(255,60,80,.25) !important;
        }

        @media (max-width: 768px) {

            .block-container {
                padding-left: .7rem !important;
                padding-right: .7rem !important;
            }

            .hero {
                padding: 24px 18px !important;
            }

            .hero-title {
                font-size: 30px !important;
            }

            .kpi-value {
                font-size: 24px !important;
            }

            .probability {
                font-size: 38px !important;
            }

            .panel,
            .analysis-card,
            .ai-result {
                padding: 16px !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
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
   RecoverAI — Warm Wood + Minimal Gold Theme
   Responsive desktop + mobile
   ========================================================== */

:root {
    --wood-bg: #f5efe5;
    --wood-bg-2: #eee3d2;
    --card: #fffaf2;
    --card-2: #f7efe2;
    --border: #d9c7aa;
    --border-strong: #c7ad86;
    --text: #2f271f;
    --muted: #725f48;
    --muted-2: #8c775d;
    --gold: #c7922e;
    --gold-light: #e4bb62;
    --gold-dark: #a87418;
    --green: #668b45;
    --red: #bd5a4b;
    --shadow: rgba(83, 60, 32, 0.12);
}

/* Page */
.stApp {
    background:
        radial-gradient(circle at 8% 5%, rgba(228,187,98,0.18), transparent 28%),
        radial-gradient(circle at 92% 12%, rgba(199,173,134,0.18), transparent 30%),
        linear-gradient(135deg, var(--wood-bg), #fbf7f0 55%, var(--wood-bg-2));
    color: var(--text);
}

.block-container {
    max-width: 1450px;
    padding: 1.5rem 2rem 4rem;
}

#MainMenu, footer, header { visibility: hidden; }

/* General Streamlit text */
.stApp, .stApp p, .stApp label, .stApp span,
.stApp div, .stApp h1, .stApp h2, .stApp h3 {
    color: var(--text);
}

/* Hero */
.hero {
    padding: 42px 48px;
    border-radius: 26px;
    margin-bottom: 34px;
    background: linear-gradient(135deg, #fffaf2, #f1e5d2);
    border: 1px solid var(--border-strong);
    box-shadow: 0 18px 45px var(--shadow), inset 0 1px 0 rgba(255,255,255,.8);
}

.hero-title {
    font-size: 52px;
    font-weight: 850;
    letter-spacing: -1.8px;
    line-height: 1.1;
    margin-bottom: 10px;
}

.hero-title span {
    color: var(--gold-dark);
}

.hero-subtitle {
    font-size: 19px;
    color: var(--muted) !important;
    margin-bottom: 20px;
}

.status-pill {
    display: inline-block;
    padding: 8px 15px;
    border-radius: 999px;
    background: #f4e8c9;
    border: 1px solid #d8b45d;
    color: #7d5a18 !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
}

/* Titles */
.section-title {
    font-size: 25px;
    font-weight: 800;
    color: var(--text) !important;
    margin: 18px 0 18px;
    letter-spacing: -.35px;
}

/* KPI cards */
.kpi-card {
    min-height: 145px;
    padding: 24px;
    border-radius: 18px;
    background: linear-gradient(145deg, #fffdf8, #f5ecde);
    border: 1px solid var(--border);
    box-shadow: 0 10px 28px var(--shadow);
    transition: transform .2s ease, border-color .2s ease;
}
.kpi-card:hover {
    transform: translateY(-3px);
    border-color: #c9a45e;
}
.kpi-label, .action-label, .probability-label {
    color: var(--muted-2) !important;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.15px;
}
.kpi-value {
    color: var(--text) !important;
    font-size: 34px;
    font-weight: 850;
    margin-top: 9px;
}
.kpi-description {
    color: var(--muted) !important;
    font-size: 12px;
    margin-top: 6px;
}

/* Panels */
.panel, .analysis-card {
    padding: 26px;
    border-radius: 20px;
    background: linear-gradient(145deg, #fffaf2, #f4e9d9);
    border: 1px solid var(--border);
    box-shadow: 0 14px 38px var(--shadow);
}
.analysis-card { margin-top: 22px; }

/* Result */
.ai-result {
    padding: 30px;
    border-radius: 22px;
    background:
        radial-gradient(circle at top right, rgba(228,187,98,.22), transparent 42%),
        linear-gradient(145deg, #fffaf2, #efe1cc);
    border: 1px solid #cdb17e;
    box-shadow: 0 18px 48px var(--shadow);
}
.probability-label { color: #8a6a35 !important; }
.probability {
    color: #4b3822 !important;
    font-size: 54px;
    font-weight: 900;
    margin-top: 4px;
}
.recovery-level {
    color: #7d684d !important;
    font-size: 15px;
    font-weight: 800;
    margin: 8px 0 20px;
}

/* Action cards */
.action-card {
    padding: 16px 18px;
    margin-top: 10px;
    border-radius: 14px;
    background: rgba(255,255,255,.52);
    border: 1px solid #ddceb7;
    box-shadow: 0 5px 16px rgba(83,60,32,.06);
}
.action-value {
    color: #382c20 !important;
    font-size: 18px;
    font-weight: 800;
    margin-top: 6px;
}

/* Streamlit inputs */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label {
    color: #67543d !important;
    font-size: 12px !important;
    font-weight: 750 !important;
    margin-bottom: 5px !important;
}

div[data-testid="stNumberInput"] > div,
div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #fffaf2 !important;
    background-color: #fffaf2 !important;
    border: 1px solid #cfb996 !important;
    border-radius: 10px !important;
    color: #3a2e22 !important;
    min-height: 44px !important;
    box-shadow: inset 0 1px 2px rgba(83,60,32,.05);
}

div[data-testid="stNumberInput"] input {
    background: #fffaf2 !important;
    color: #3a2e22 !important;
    border: none !important;
    font-size: 14px !important;
    font-weight: 650 !important;
}

div[data-testid="stNumberInput"] button {
    background: #f1e2c7 !important;
    color: #654a23 !important;
    border: none !important;
}
div[data-testid="stNumberInput"] button:hover {
    background: #e7d2aa !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] {
    width: 100% !important;
}
div[data-testid="stSelectbox"] [data-baseweb="select"] [role="combobox"],
div[data-testid="stSelectbox"] [data-baseweb="select"] span {
    background: transparent !important;
    color: #3a2e22 !important;
}
div[data-testid="stSelectbox"] [data-baseweb="select"] svg {
    color: #a47a29 !important;
    fill: #a47a29 !important;
}

/* Dropdown */
div[data-baseweb="popover"],
div[data-baseweb="menu"] {
    background: #fffaf2 !important;
    border: 1px solid #cfb996 !important;
}
div[data-baseweb="menu"] li {
    background: #fffaf2 !important;
    color: #3a2e22 !important;
}
div[data-baseweb="menu"] li:hover {
    background: #f1e2c7 !important;
}

/* Slider */
div[data-testid="stSlider"] { padding-top: 4px !important; }
div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
    color: #a87518 !important;
    font-weight: 850 !important;
}

/* Analyze button */
.stButton > button {
    width: 100% !important;
    min-height: 50px !important;
    border-radius: 12px !important;
    background: linear-gradient(135deg, #d8a83d, #bd8520) !important;
    color: #fffdf8 !important;
    border: 1px solid #b77d17 !important;
    font-size: 14px !important;
    font-weight: 850 !important;
    box-shadow: 0 10px 24px rgba(174,125,32,.22);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #e0b34f, #c99128) !important;
    border-color: #a96f12 !important;
}

/* Native alerts */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: 1px solid #d6c3a2 !important;
}

/* Responsive */
@media (max-width: 900px) {
    .block-container {
        padding: 1rem .8rem 3rem !important;
    }
    .hero {
        padding: 28px 22px !important;
        border-radius: 20px !important;
        margin-bottom: 24px !important;
    }
    .hero-title { font-size: 36px !important; }
    .hero-subtitle { font-size: 15px !important; }
    .section-title { font-size: 20px !important; margin-top: 14px !important; }
    .kpi-card { min-height: 110px !important; padding: 17px !important; }
    .kpi-value { font-size: 26px !important; }
    .panel, .analysis-card, .ai-result { padding: 18px !important; border-radius: 16px !important; }
    .probability { font-size: 42px !important; }
    .action-card { padding: 14px !important; }
    .action-value { font-size: 16px !important; }
    .stButton > button { min-height: 52px !important; }
}

/* Very small phones */
@media (max-width: 600px) {
    .block-container {
        padding-left: .65rem !important;
        padding-right: .65rem !important;
    }
    .hero-title { font-size: 30px !important; }
    .hero-subtitle { font-size: 14px !important; }
    .status-pill { font-size: 10px !important; }
    .kpi-value { font-size: 23px !important; }
    .probability { font-size: 36px !important; }
    .action-label, .kpi-label, .probability-label { font-size: 9px !important; }
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] span { font-size: 13px !important; }
}
</style>


""",
    unsafe_allow_html=True

)



# ============================================================
# DARK BLUE THEME
# ============================================================

if st.session_state.dark_mode:

    st.markdown(
        """
        <style>

        /* PAGE */
        .stApp {
            background:
                radial-gradient(
                    circle at 10% 5%,
                    rgba(40, 90, 180, 0.25),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 90% 10%,
                    rgba(100, 50, 180, 0.18),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    #050914,
                    #091326,
                    #050914
                ) !important;

            color: #f5f7ff !important;
        }


        /* MAIN CONTAINER */
        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }


        /* ALL TEXT */
        .stApp p,
        .stApp span,
        .stApp label,
        .stApp h1,
        .stApp h2,
        .stApp h3 {
            color: #f5f7ff !important;
        }


        /* HERO */
        .hero {
            background:
                linear-gradient(
                    145deg,
                    #101d38,
                    #091326
                ) !important;

            border: 1px solid #315991 !important;

            box-shadow:
                0 20px 50px rgba(0,0,0,.45) !important;
        }

        .hero-title {
            color: #ffffff !important;
        }

        .hero-title span {
            color: #79a9ff !important;
        }

        .hero-subtitle {
            color: #9bbcff !important;
        }


        /* STATUS */
        .status-pill {
            background: rgba(20,150,110,.15) !important;
            border: 1px solid #1ca878 !important;
            color: #50e6ad !important;
        }


        /* SECTION TITLES */
        .section-title {
            color: #ffffff !important;
        }


        /* KPI CARDS */
        .kpi-card {
            background:
                linear-gradient(
                    145deg,
                    #101c33,
                    #0a1326
                ) !important;

            border: 1px solid #263f69 !important;

            box-shadow:
                0 12px 30px rgba(0,0,0,.40) !important;
        }

        .kpi-card:hover {
            border-color: #4c86e8 !important;
            transform: translateY(-3px);
        }

        .kpi-label {
            color: #7faeff !important;
        }

        .kpi-value {
            color: #ffffff !important;
        }

        .kpi-description {
            color: #8ca3c7 !important;
        }


        /* PANELS */
        .panel,
        .analysis-card,
        .ai-result {
            background:
                linear-gradient(
                    145deg,
                    #0c172c,
                    #080f20
                ) !important;

            border: 1px solid #29466f !important;

            box-shadow:
                0 15px 35px rgba(0,0,0,.42) !important;
        }


        /* ACTION CARDS */
        .action-card {
            background: #111c30 !important;
            border: 1px solid #29415f !important;
            box-shadow: 0 8px 20px rgba(0,0,0,.3) !important;
        }

        .action-label {
            color: #82a7dc !important;
        }

        .action-value {
            color: #ffffff !important;
        }


        /* AI PROBABILITY */
        .probability-label {
            color: #78a9ff !important;
        }

        .probability {
            color: #ffffff !important;
        }

        .recovery-level {
            color: #9ab8e5 !important;
        }


        /* NUMBER INPUT */
        div[data-testid="stNumberInput"] > div {
            background: #151e31 !important;
            background-color: #151e31 !important;
            border: 1px solid #385780 !important;
        }

        div[data-testid="stNumberInput"] input {
            background: transparent !important;
            color: #ffffff !important;
            font-weight: 700 !important;
        }


        /* PLUS / MINUS */
        div[data-testid="stNumberInput"] button {
            background: #1c2b45 !important;
            color: #dce9ff !important;
        }

        div[data-testid="stNumberInput"] button:hover {
            background: #2c4770 !important;
            color: #ffffff !important;
        }


        /* SELECT BOX */
        div[data-testid="stSelectbox"]
        [data-baseweb="select"] > div {
            background: #151e31 !important;
            background-color: #151e31 !important;
            border: 1px solid #385780 !important;
        }

        div[data-testid="stSelectbox"]
        [data-baseweb="select"]
        span {
            color: #ffffff !important;
        }

        div[data-testid="stSelectbox"]
        [data-baseweb="select"]
        svg {
            color: #8db7ff !important;
            fill: #8db7ff !important;
        }


        /* INPUT LABELS */
        div[data-testid="stNumberInput"] label,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSlider"] label {
            color: #91b8f0 !important;
            font-weight: 750 !important;
        }


        /* SLIDER */
        div[data-testid="stSlider"]
        [data-testid="stSliderThumbValue"] {
            color: #ff5260 !important;
            font-weight: 850 !important;
        }


        /* ANALYZE BUTTON */
        .stButton > button {
            background:
                linear-gradient(
                    135deg,
                    #ff4f5e,
                    #e83f50
                ) !important;

            color: white !important;

            border: 1px solid #ff6875 !important;

            box-shadow:
                0 12px 30px rgba(255,60,80,.25) !important;
        }

        .stButton > button:hover {
            background:
                linear-gradient(
                    135deg,
                    #ff6875,
                    #ed4051
                ) !important;

            transform: translateY(-2px);
        }


        /* MOBILE */
        @media (max-width: 768px) {

            .block-container {
                padding-left: .7rem !important;
                padding-right: .7rem !important;
            }

            .hero {
                padding: 24px 18px !important;
            }

            .hero-title {
                font-size: 30px !important;
            }

            .kpi-value {
                font-size: 24px !important;
            }

            .probability {
                font-size: 38px !important;
            }

            .panel,
            .analysis-card,
            .ai-result {
                padding: 16px !important;
            }
        }

        /* ======================================================
           FINAL DARK MODE READABILITY OVERRIDES
           Keep the dashboard dark blue and make content clear.
           These rules intentionally use !important so they also
           override the inline light-theme colors used in HTML.
           ====================================================== */

        /* All dashboard text */
        .stApp,
        .stApp p,
        .stApp span,
        .stApp label,
        .stApp div,
        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp strong {
            color: #f7faff !important;
        }

        /* KPI cards */
        .kpi-label,
        .action-label,
        .probability-label {
            color: #8fbaff !important;
        }

        .kpi-value,
        .kpi-description {
            color: #ffffff !important;
        }

        /* Main result */
        .probability {
            color: #ffffff !important;
        }

        .recovery-level {
            color: #b9d2f5 !important;
        }

        /* Action / information cards */
        .action-card,
        .action-card * {
            color: #ffffff !important;
        }

        .action-card .action-label {
            color: #8fbaff !important;
        }

        .action-card .action-value {
            color: #ffffff !important;
        }

        /* Override inline brown text inside generated HTML */
        .analysis-card [style*="color:#4b3d2f"],
        .analysis-card [style*="color:#3a2e22"],
        .analysis-card [style*="color:#7d684e"],
        .analysis-card [style*="color:#7d684e"],
        .analysis-card [style*="color:#8f7a5f"],
        .analysis-card [style*="color:#a9bbd8"] {
            color: #ffffff !important;
        }

        /* Inline progress scale text */
        .analysis-card [style*="font-size:12px"] span,
        .analysis-card [style*="font-size:13px"] {
            color: #dce9ff !important;
        }

        /* Decision pipeline */
        .analysis-card [style*="DECISION PIPELINE"] {
            color: #8fbaff !important;
        }

        /* Pipeline text and final decision */
        .analysis-card strong {
            color: #ffffff !important;
        }

        /* Progress-bar backgrounds */
        .analysis-card [style*="background:#eadcc8"] {
            background: #1b2c49 !important;
        }

        /* Recovery potential / summary panels */
        .analysis-card [style*="rgba(20,35,70,0.55)"],
        .analysis-card [style*="rgba(72,104,255,0.10)"] {
            color: #ffffff !important;
        }

        /* Streamlit alerts */
        div[data-testid="stAlert"],
        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] span {
            color: #ffffff !important;
        }

        /* Slider value */
        div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
            color: #ffffff !important;
        }

        /* Footer */
        .footer,
        .footer * {
            color: #9db8dc !important;
        }

        /* ======================================================
           END DARK MODE READABILITY OVERRIDES
           ====================================================== */

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
        color:#7d684e;
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
        background:#eadcc8;
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
                #d39b2d,
                #e4bb62,
                #7e9d57
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
        color:#8f7a5f;
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
                    color:#4b3d2f;
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
                    <span style="color:#b47d1c;"> → </span>
                    ML Prediction
                    <span style="color:#b47d1c;"> → </span>
                    Recovery Probability
                    <span style="color:#b47d1c;"> → </span>
                    Decision Engine
                    <span style="color:#b47d1c;"> → </span>
                    <strong style="color:#3a2e22;">
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
                        color:#7d684e;
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
                        color:#7d684e;
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
                        color:#7d684e;
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
                    background:#eadcc8;
                    border-radius:20px;
                    overflow:hidden;
                ">

                    <div style="
                        width:{max(2, min(probability * 100, 100)):.2f}%;
                        height:100%;
                        background:linear-gradient(
                            90deg,
                            #d39b2d,
                            #e4bb62,
                            #7e9d57
                        );
                        border-radius:20px;
                    ">
                    </div>

                </div>

                <div style="
                    display:flex;
                    justify-content:space-between;
                    margin-top:8px;
                    color:#8f7a5f;
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
                        color:#7d684e;
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
                        color:#7d684e;
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
                        color:#7d684e;
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
                        color:#3a2e22;
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
                    color:#3a2e22;
                ">
                    {action}
                </div>

                <div style="
                    margin-top:6px;
                    color:#7d684e;
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
                        background:#eadcc8;
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
                        color:#7d684e;
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
                        color:#7d684e;
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
                        color:#7d684e;
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
                        color:#7d684e;
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
                        color:#7d684e;
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
                    color:#4b3d2f;
                    font-size:16px;
                    line-height:1.6;
                ">
                    RecoverAI evaluated the transaction using its
                    historical payment behaviour, failure characteristics,
                    retry history and recovery probability before selecting
                    <strong style="color:#3a2e22;">
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
# ============================================================
# FINAL DARK MODE TEXT OVERRIDES
# ============================================================

if st.session_state.dark_mode:

    st.markdown(
        """
        <style>

        /* ==================================================
           RecoverAI Dark Mode - Final Text Readability
           ================================================== */

        /* Main analysis text */
        .analysis-card {
            color: #ffffff !important;
        }

        .analysis-card p,
        .analysis-card div,
        .analysis-card span,
        .analysis-card strong {
            color: #ffffff !important;
        }

        /* Keep section labels light blue */
        .analysis-card .section-title {
            color: #ffffff !important;
        }

        .analysis-card .action-label,
        .analysis-card .kpi-label,
        .analysis-card .probability-label {
            color: #82b5ff !important;
        }

        /* Main values */
        .analysis-card .action-value,
        .analysis-card .kpi-value,
        .analysis-card .probability {
            color: #ffffff !important;
        }

        /* Override old inline brown text */
        .analysis-card div[style*="#4b3d2f"],
        .analysis-card div[style*="#4b3822"],
        .analysis-card div[style*="#3a2e22"],
        .analysis-card div[style*="#7d684e"],
        .analysis-card div[style*="#7d684d"],
        .analysis-card div[style*="#725f48"] {
            color: #ffffff !important;
        }

        /* Override brown inline text on strong elements */
        .analysis-card strong[style*="#3a2e22"],
        .analysis-card strong[style*="#4b3d2f"] {
            color: #ffffff !important;
        }

        /* Decision pipeline */
        .analysis-card div[style*="color:#a9bbd8"] {
            color: #ffffff !important;
        }

        .analysis-card span[style*="#b47d1c"] {
            color: #8db7ff !important;
        }

        /* AI assessment */
        .analysis-card div[style*="rgba(72,104,255,0.10)"] {
            color: #ffffff !important;
        }

        /* Recovery analytics descriptions */
        .analysis-card div[style*="font-size:13px"] {
            color: #ffffff !important;
        }

        /* Current recovery decision */
        .analysis-card div[style*="font-size:22px"] {
            color: #ffffff !important;
        }

        /* Execution status */
        .analysis-card div[style*="font-size:14px"] {
            color: #ffffff !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
    # ============================================================
    # FINAL DARK MODE - FORCE ALL DASHBOARD TEXT TO WHITE
    # ============================================================

    if st.session_state.dark_mode:
        st.markdown(
            """
            <style>

            /* ================================================
               FORCE TEXT INSIDE ANALYSIS CARDS TO WHITE
               ================================================ */

            .analysis-card div,
            .analysis-card p,
            .analysis-card span,
            .analysis-card strong {
                color: #ffffff !important;
            }


            /* ================================================
               SECTION TITLES
               ================================================ */

            .analysis-card .section-title {
                color: #ffffff !important;
            }


            /* ================================================
               BLUE LABELS
               ================================================ */

            .analysis-card .action-label,
            .analysis-card .kpi-label,
            .analysis-card .probability-label {
                color: #82b5ff !important;
            }


            /* ================================================
               MAIN VALUES
               ================================================ */

            .analysis-card .action-value,
            .analysis-card .kpi-value,
            .analysis-card .probability {
                color: #ffffff !important;
            }


            /* ================================================
               AI REASONING TEXT
               ================================================ */

            .analysis-card .action-card > div:not(.action-label):not(.action-value) {
                color: #ffffff !important;
            }


            /* ================================================
               DECISION PIPELINE
               ================================================ */

            .analysis-card strong {
                color: #ffffff !important;
            }

            .analysis-card span {
                color: #ffffff !important;
            }


            /* Make pipeline arrows blue */
            .analysis-card span[style*="b47d1c"],
            .analysis-card span[style*="B47D1C"] {
                color: #79a9ff !important;
            }


            /* ================================================
               INLINE BROWN COLORS - OVERRIDE THEM
               ================================================ */

            .analysis-card [style*="color"] {
                color: #ffffff !important;
            }


            /* Restore blue labels AFTER inline override */
            .analysis-card .action-label {
                color: #82b5ff !important;
            }

            .analysis-card .section-title {
                color: #ffffff !important;
            }

            .analysis-card .action-value {
                color: #ffffff !important;
            }


            /* ================================================
               AI ASSESSMENT / EXPLANATION
               ================================================ */

            .analysis-card div[style*="font-size:16px"],
            .analysis-card div[style*="font-size:18px"],
            .analysis-card div[style*="font-size:14px"],
            .analysis-card div[style*="font-size:15px"] {
                color: #ffffff !important;
            }


            /* ================================================
               PIPELINE TEXT
               ================================================ */

            .analysis-card div[style*="margin-top:12px"] {
                color: #ffffff !important;
            }


            /* ================================================
               KEEP PROGRESS BAR COLORS
               ================================================ */

            .analysis-card div[style*="background:#eadcc8"] {
                color: transparent !important;
            }

            </style>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FINAL DARK-BLUE THEME + INPUT READABILITY FIX
# ============================================================

if st.session_state.dark_mode:

    st.markdown(
        """
        <style>

        /* ---------- DARK BLUE PAGE ---------- */
        .stApp {
            background:
                radial-gradient(
                    circle at 10% 5%,
                    rgba(40, 90, 180, 0.25),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 90% 10%,
                    rgba(100, 50, 180, 0.18),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    #050914,
                    #091326,
                    #050914
                ) !important;
            color: #f7faff !important;
        }

        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background: transparent !important;
        }

        /* ---------- NUMBER INPUTS ----------
           Keep the input box light, but make the typed value BLACK.
           This fixes:
           Transaction Amount (₹)
           Retry Attempts
           Previous Successful Payments
           Previous Failed Payments
        */
        div[data-testid="stNumberInput"] > div {
            background: #f1f3f7 !important;
            background-color: #f1f3f7 !important;
            border: 1px solid #8fa6c7 !important;
            border-radius: 10px !important;
        }

        div[data-testid="stNumberInput"] input,
        div[data-testid="stNumberInput"] input[type="number"] {
            background: #f1f3f7 !important;
            background-color: #f1f3f7 !important;
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            caret-color: #111827 !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }

        div[data-testid="stNumberInput"] input::placeholder {
            color: #374151 !important;
            -webkit-text-fill-color: #374151 !important;
            opacity: 1 !important;
        }

        div[data-testid="stNumberInput"] button {
            background: #1b2b46 !important;
            color: #e7efff !important;
            border-color: #385780 !important;
        }

        div[data-testid="stNumberInput"] button:hover {
            background: #29466f !important;
            color: #ffffff !important;
        }

        /* ---------- SELECT BOXES ---------- */
        div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
            background: #f1f3f7 !important;
            background-color: #f1f3f7 !important;
            border: 1px solid #8fa6c7 !important;
            color: #111827 !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] span,
        div[data-testid="stSelectbox"] [data-baseweb="select"] [role="combobox"] {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] svg {
            color: #243b5a !important;
            fill: #243b5a !important;
        }

        /* Dropdown menu */
        div[data-baseweb="popover"],
        div[data-baseweb="menu"] {
            background: #f1f3f7 !important;
            border: 1px solid #8fa6c7 !important;
        }

        div[data-baseweb="menu"] li {
            background: #f1f3f7 !important;
            color: #111827 !important;
        }

        div[data-baseweb="menu"] li:hover {
            background: #dce7f6 !important;
            color: #111827 !important;
        }

        /* ---------- INPUT LABELS ---------- */
        div[data-testid="stNumberInput"] label,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSlider"] label {
            color: #dbe8ff !important;
            font-weight: 750 !important;
        }

        /* ---------- REMOVE BROWN FROM RESULT CARDS ---------- */
        .analysis-card [style*="color:#4b3d2f"],
        .analysis-card [style*="color:#4b3822"],
        .analysis-card [style*="color:#3a2e22"],
        .analysis-card [style*="color:#7d684e"],
        .analysis-card [style*="color:#7d684d"],
        .analysis-card [style*="color:#725f48"],
        .analysis-card [style*="color:#8f7a5f"] {
            color: #ffffff !important;
        }

        /* Any remaining inline color in analysis text */
        .analysis-card [style*="color:"] {
            color: #ffffff !important;
        }

        /* Restore intentional blue labels */
        .analysis-card .action-label,
        .analysis-card .kpi-label,
        .analysis-card .probability-label {
            color: #82b5ff !important;
        }

        /* Pipeline arrows */
        .analysis-card span[style*="b47d1c"],
        .analysis-card span[style*="B47D1C"] {
            color: #79a9ff !important;
        }

        /* Main result values */
        .analysis-card .action-value,
        .analysis-card .kpi-value,
        .analysis-card .probability,
        .analysis-card .section-title,
        .analysis-card strong {
            color: #ffffff !important;
        }

        /* Recovery progress background */
        .analysis-card [style*="background:#eadcc8"] {
            background: #1b2c49 !important;
        }

        /* Footer */
        .footer,
        .footer * {
            color: #9db8dc !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )



# ============================================================
# FINAL DARK BLUE UI THEME
# White text + dark inputs across the complete dashboard
# ============================================================

if st.session_state.dark_mode:
    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL DARK BLUE PAGE
           ===================================================== */

        .stApp {
            background:
                radial-gradient(circle at 8% 5%, rgba(45,105,210,.20), transparent 28%),
                radial-gradient(circle at 92% 10%, rgba(90,70,190,.16), transparent 30%),
                linear-gradient(135deg, #050914 0%, #091326 55%, #050914 100%) !important;
            color: #ffffff !important;
        }

        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stHeader"] {
            background: transparent !important;
        }

        /* Main Streamlit text */
        .stApp p,
        .stApp label,
        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6 {
            color: #ffffff !important;
        }

        /* =====================================================
           CUSTOM DASHBOARD CARDS
           ===================================================== */

        .hero,
        .panel,
        .analysis-card,
        .ai-result {
            background: linear-gradient(145deg, #0d1930, #080f20) !important;
            border: 1px solid #29466f !important;
            box-shadow: 0 15px 35px rgba(0,0,0,.42) !important;
        }

        .hero-title,
        .section-title {
            color: #ffffff !important;
        }

        .hero-title span {
            color: #79a9ff !important;
        }

        .hero-subtitle {
            color: #dbe8ff !important;
        }

        .kpi-card,
        .action-card {
            background: #111c30 !important;
            border: 1px solid #29415f !important;
            color: #ffffff !important;
        }

        .kpi-label,
        .action-label,
        .probability-label {
            color: #82b5ff !important;
        }

        .kpi-value,
        .kpi-description,
        .action-value,
        .probability,
        .recovery-level {
            color: #ffffff !important;
        }

        .kpi-description {
            color: #ffffff !important;
        }

        /* =====================================================
           FORCE INLINE BROWN TEXT TO WHITE
           This catches the HTML result cards generated below.
           ===================================================== */

        .analysis-card [style*="color"],
        .analysis-card [style*="COLOR"] {
            color: #ffffff !important;
        }

        .analysis-card .action-label,
        .analysis-card .kpi-label,
        .analysis-card .probability-label {
            color: #82b5ff !important;
        }

        .analysis-card .action-value,
        .analysis-card .kpi-value,
        .analysis-card .probability,
        .analysis-card .section-title,
        .analysis-card strong {
            color: #ffffff !important;
        }

        /* Decision pipeline arrows */
        .analysis-card span[style*="b47d1c"],
        .analysis-card span[style*="B47D1C"] {
            color: #79a9ff !important;
        }

        /* =====================================================
           NUMBER INPUTS — DARK BOX + WHITE TEXT
           Applies to all four:
           Transaction Amount
           Retry Attempts
           Previous Successful Payments
           Previous Failed Payments
           ===================================================== */

        div[data-testid="stNumberInput"] {
            color: #ffffff !important;
        }

        div[data-testid="stNumberInput"] > div {
            background: #111c30 !important;
            background-color: #111c30 !important;
            border: 1px solid #5277a8 !important;
            border-radius: 10px !important;
        }

        div[data-testid="stNumberInput"] input,
        div[data-testid="stNumberInput"] input[type="number"],
        div[data-testid="stNumberInput"] input[type="text"] {
            background: #111c30 !important;
            background-color: #111c30 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            caret-color: #ffffff !important;
            opacity: 1 !important;
            font-weight: 700 !important;
        }

        div[data-testid="stNumberInput"] input::placeholder {
            color: #dbe8ff !important;
            -webkit-text-fill-color: #dbe8ff !important;
            opacity: 1 !important;
        }

        div[data-testid="stNumberInput"] button {
            background: #1c2f4f !important;
            color: #ffffff !important;
            border-color: #385780 !important;
        }

        div[data-testid="stNumberInput"] button svg {
            color: #ffffff !important;
            fill: #ffffff !important;
        }

        div[data-testid="stNumberInput"] button:hover {
            background: #2b4771 !important;
            color: #ffffff !important;
        }

        /* =====================================================
           SELECT BOXES — DARK BOX + WHITE TEXT
           ===================================================== */

        div[data-testid="stSelectbox"] {
            color: #ffffff !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
            background: #111c30 !important;
            background-color: #111c30 !important;
            border: 1px solid #5277a8 !important;
            color: #ffffff !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"],
        div[data-testid="stSelectbox"] [data-baseweb="select"] [role="combobox"],
        div[data-testid="stSelectbox"] [data-baseweb="select"] span {
            background: transparent !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] svg {
            color: #9ec5ff !important;
            fill: #9ec5ff !important;
        }

        /* Dropdown */
        div[data-baseweb="popover"],
        div[data-baseweb="menu"] {
            background: #111c30 !important;
            border: 1px solid #5277a8 !important;
        }

        div[data-baseweb="menu"] li {
            background: #111c30 !important;
            color: #ffffff !important;
        }

        div[data-baseweb="menu"] li:hover {
            background: #203a60 !important;
            color: #ffffff !important;
        }

        /* =====================================================
           INPUT LABELS
           ===================================================== */

        div[data-testid="stNumberInput"] label,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSlider"] label {
            color: #ffffff !important;
            font-weight: 750 !important;
        }

        /* =====================================================
           SLIDER
           ===================================================== */

        div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
            color: #ffffff !important;
            font-weight: 850 !important;
        }

        /* =====================================================
           BUTTON
           ===================================================== */

        .stButton > button {
            background: linear-gradient(135deg, #ff4f5e, #e83f50) !important;
            color: #ffffff !important;
            border: 1px solid #ff6875 !important;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #ff6875, #ed4051) !important;
            color: #ffffff !important;
        }

        /* =====================================================
           PROGRESS BAR
           ===================================================== */

        .analysis-card [style*="background:#eadcc8"] {
            background: #1b2c49 !important;
        }

        /* =====================================================
           ALERTS
           ===================================================== */

        div[data-testid="stAlert"],
        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] span {
            color: #ffffff !important;
        }

        /* =====================================================
           FOOTER
           ===================================================== */

        .footer,
        .footer * {
            color: #dbe8ff !important;
        }

        /* =====================================================
           MOBILE
           ===================================================== */

        @media (max-width: 768px) {
            .block-container {
                padding-left: .7rem !important;
                padding-right: .7rem !important;
            }

            .hero {
                padding: 24px 18px !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )
