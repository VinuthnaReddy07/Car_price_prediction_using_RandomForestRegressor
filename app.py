
import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
from html import escape

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="AutoValue | Car Price Prediction",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #10233f;
    --blue: #3474f7;
    --text: #18345e;
    --muted: #61728d;
    --line: #e2eaf5;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f5f8ff;
    color: var(--text);
}

[data-testid="stAppViewContainer"] {
    background: #f5f8ff;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    right: 1rem;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.4rem;
    padding-bottom: 2rem !important;
}

/* Hide Streamlit branding */
#MainMenu, footer {
    visibility: hidden;
}

/* Navigation */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0 18px;
    border-bottom: 1px solid var(--line);
    margin-bottom: 14px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 24px;
    font-weight: 800;
    color: #173b6c;
    letter-spacing: -0.8px;
}

.brand-mark {
    display: grid;
    place-items: center;
    width: 38px;
    height: 38px;
    border-radius: 12px;
    color: #ffffff;
    background: linear-gradient(145deg, #4a87ff, #245bd6);
    box-shadow: 0 5px 12px rgba(47, 109, 246, 0.22);
    font-size: 15px;
    letter-spacing: -0.5px;
}

.brand-name span {
    color: #3978f6;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #526b8b;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.25px;
}

.nav-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #39b980;
    box-shadow: 0 0 0 4px #e3f7ef;
}

/* Hero section */
.hero {
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    border-radius: 22px;
    margin: 0;
    padding: 48px 52px;
    min-height: 290px;
    color: white;
    background:
        linear-gradient(90deg,
            rgba(12, 25, 44, 0.96) 0%,
            rgba(12, 25, 44, 0.84) 45%,
            rgba(12, 25, 44, 0.28) 100%),
        url("https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1800&q=85")
        center 55% / cover no-repeat;
}

.hero-copy {
    max-width: 590px;
}

.hero-tag {
    display: inline-block;
    background: rgba(68, 128, 255, 0.2);
    border: 1px solid rgba(164, 196, 255, 0.3);
    padding: 8px 13px;
    border-radius: 30px;
    color: #e4efff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
    margin-bottom: 16px;
}

.hero h1 {
    color: white !important;
    font-size: clamp(34px, 4.2vw, 52px) !important;
    line-height: 1.14 !important;
    font-weight: 800 !important;
    letter-spacing: -1.6px;
    margin: 0 0 17px !important;
}

.hero h1 span {
    color: #95c7ff;
}

.hero p {
    color: #e1e9f6;
    font-size: 15px;
    line-height: 1.7;
    max-width: 490px;
    margin: 0;
}

/* Main content */
.content-area {
    height: 0;
    margin-top: 0;
    position: relative;
    z-index: 2;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 20px;
    box-shadow: 0 14px 36px rgba(29, 58, 103, 0.07);
    padding: 24px;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 18px 42px rgba(29, 58, 103, 0.1);
}

.form-heading {
    display: flex;
    align-items: flex-start;
    gap: 13px;
    margin-bottom: 24px;
}

.form-heading-icon {
    display: grid;
    place-items: center;
    flex: 0 0 44px;
    height: 44px;
    border-radius: 13px;
    background: #edf3ff;
    font-size: 21px;
}

.form-heading h2 {
    color: #183b6b;
    font-size: 21px;
    font-weight: 800;
    letter-spacing: -0.5px;
    line-height: 1.3;
    margin: 0;
}

.form-heading p {
    color: #61728d;
    font-size: 13px;
    line-height: 1.5;
    margin: 4px 0 0;
}

.section-title {
    color: #183b6b;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0 0 5px;
}

.section-subtitle {
    color: #587092;
    font-size: 13px;
    margin-bottom: 24px;
}

.mini-heading {
    color: #183b6b;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: -0.3px;
    margin: 2px 0 8px;
}

.mini-description {
    color: #71819a;
    font-size: 12px;
    line-height: 1.6;
    margin: 0 0 25px;
}

.step {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin: 21px 0;
}

.step-icon {
    flex: 0 0 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-size: 22px;
    background: #e5edff;
}

.step h4 {
    color: #1a3b67;
    font-size: 13px;
    font-weight: 700;
    margin: 3px 0 6px;
}

.step p {
    color: #5b7192;
    font-size: 11px;
    line-height: 1.6;
    margin: 0;
}

label, [data-testid="stWidgetLabel"] p {
    color: #294668 !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    margin-bottom: 6px !important;
}

[data-testid="stWidgetLabel"] {
    margin-bottom: 5px !important;
}

div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-color: #c8d8f0 !important;
    border-radius: 11px !important;
    min-height: 45px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

div[data-baseweb="select"] > div:hover {
    border-color: #8eafe9 !important;
}

div[data-baseweb="select"] input,
div[data-baseweb="select"] div[role="combobox"] {
    color: #173b6c !important;
    -webkit-text-fill-color: #173b6c !important;
    font-weight: 600;
}

div[data-testid="stNumberInput"] input {
    background-color: #ffffff !important;
    border: 1px solid #c8d8f0 !important;
    border-radius: 11px 0 0 11px;
    min-height: 44px;
    color: #173b6c !important;
    -webkit-text-fill-color: #173b6c !important;
    font-weight: 600;
}

div[data-testid="stNumberInput"] [data-baseweb="input"] {
    background-color: #ffffff !important;
    border-radius: 11px 0 0 11px;
}

div[data-testid="stNumberInput"] button {
    background-color: #edf3ff !important;
    color: #2865ed !important;
    border: 1px solid #c8d8f0 !important;
    transition: background-color 0.2s ease, color 0.2s ease;
}

div[data-testid="stNumberInput"] button:hover {
    background-color: #dce8ff !important;
    color: #174cae !important;
}

div[data-testid="stNumberInput"] button svg {
    fill: currentColor;
}

div[data-testid="stNumberInput"] input:focus {
    border-color: #3474f7 !important;
    box-shadow: 0 0 0 3px rgba(52, 116, 247, 0.15);
}

[data-baseweb="popover"] {
    border: 1px solid #dce6f4 !important;
    border-radius: 12px !important;
    box-shadow: 0 14px 34px rgba(22, 46, 83, 0.14) !important;
}

[role="option"][aria-selected="true"] {
    background-color: #edf3ff !important;
    color: #1c4fa8 !important;
}

.stButton > button:focus-visible {
    outline: 3px solid rgba(52, 116, 247, 0.35);
    outline-offset: 3px;
}

/* Primary button */
.stButton > button {
    width: 100%;
    min-height: 50px;
    border: none;
    border-radius: 12px;
    color: white;
    background: linear-gradient(100deg, #3474f7, #2865ed);
    font-size: 14px;
    font-weight: 700;
    box-shadow: 0 6px 15px rgba(47, 109, 246, 0.22);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    color: white;
    border: none;
    transform: translateY(-2px);
    box-shadow: 0 9px 20px rgba(47, 109, 246, 0.3);
}

/* Price result */
.price-card {
    display: flex;
    align-items: center;
    gap: 22px;
    background: linear-gradient(115deg, #ffffff 0%, #edf4ff 100%);
    border: 1px solid #dbe7f8;
    border-radius: 20px;
    padding: 26px 30px;
    margin: 24px 0 30px;
    box-shadow: 0 12px 30px rgba(29, 58, 103, 0.06);
}

.price-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 64px;
    height: 64px;
    background: linear-gradient(145deg, #e0ebff, #cbdcff);
    border-radius: 19px;
    color: #2e6df4;
    font-size: 32px;
    font-weight: 800;
}

.price-content {
    min-width: 0;
}

.price-label {
    color: #42618e;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 6px;
}

.price-status {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #28664d;
    background: #e7f7ef;
    border: 1px solid #d2efdf;
    border-radius: 30px;
    padding: 6px 10px;
    margin-bottom: 10px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.45px;
    text-transform: uppercase;
}

.price-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #31a971;
}

.price-card.is-empty .price-status {
    color: #536a8b;
    background: #f0f4fa;
    border-color: #e2eaf5;
}

.price-card.is-empty .price-status-dot {
    background: #8498b5;
}

.price-value {
    color: #173c70;
    font-size: clamp(27px, 3.5vw, 40px);
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.2;
    overflow-wrap: anywhere;
}

.price-card.is-empty .price-value {
    color: #8092ad;
    font-size: clamp(22px, 3vw, 30px);
    letter-spacing: -0.5px;
}

.price-note {
    color: #5877a5;
    font-size: 12px;
    margin-top: 8px;
}

.price-car {
    margin-left: auto;
    font-size: 54px;
    opacity: 0.85;
}

/* Footer */
.footer {
    background: #111f34;
    color: #c8d5e9;
    padding: 22px 26px;
    border-radius: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    font-size: 12px;
    margin: 0;
}

.footer-brand {
    color: white;
    font-weight: 800;
    font-size: 19px;
}

.footer-brand span {
    color: #8fc7ff;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

@media (max-width: 700px) {
    .hero {
        min-height: 260px;
        padding: 38px 25px;
        border-radius: 18px;
        background-position: 60% center;
    }

    .hero p {
        max-width: 100%;
    }

    .brand {
        font-size: 21px;
    }

    .nav-right {
        display: none;
    }

    .price-card {
        padding: 20px 17px;
        gap: 13px;
    }

    .price-icon {
        flex-basis: 50px;
        height: 50px;
        border-radius: 15px;
        font-size: 25px;
    }

    .price-car {
        display: none;
    }

    .footer {
        flex-direction: column;
        text-align: center;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 19px;
        border-radius: 17px;
    }
}

/* High-contrast showroom palette */
:root {
    --navy: #14243b;
    --blue: #ef8b38;
    --text: #1c304b;
    --muted: #64748b;
    --line: #e5e9f0;
}

.navbar {
    border-bottom-color: #e5e9f0;
    margin-bottom: 20px;
}

.brand-mark {
    background: linear-gradient(145deg, #ffad58, #e87922);
    box-shadow: 0 7px 16px rgba(232, 121, 34, 0.25);
}

.brand-name span,
.footer-brand span {
    color: #e87922;
}

.nav-indicator {
    background: #e98a3b;
    box-shadow: 0 0 0 4px #fff0e2;
}

.hero {
    min-height: 340px;
    border-radius: 26px;
    padding: 52px 58px;
    background:
        linear-gradient(90deg,
            rgba(13, 27, 46, 0.98) 0%,
            rgba(13, 27, 46, 0.88) 48%,
            rgba(13, 27, 46, 0.38) 100%),
        url("https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1800&q=85")
        center 55% / cover no-repeat;
    box-shadow: 0 22px 45px rgba(17, 34, 58, 0.18);
}

.hero-tag {
    color: #ffe3c7;
    background: rgba(232, 121, 34, 0.19);
    border-color: rgba(255, 183, 117, 0.42);
}

.hero h1 span {
    color: #ffb267;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #e4e9f1;
    border-radius: 22px;
    box-shadow: 0 16px 38px rgba(22, 39, 62, 0.075);
}

.form-heading-icon {
    color: #c7651e;
    background: #fff0e2;
}

.form-heading h2,
.mini-heading {
    color: #172a43;
}

.form-heading {
    padding-bottom: 18px;
    border-bottom: 1px solid #edf0f5;
    margin-bottom: 20px;
}

.field-group-label {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #e87922;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.15px;
    text-transform: uppercase;
    margin: 8px 0 13px;
}

.field-group-label::after {
    height: 1px;
    flex: 1;
    background: #edf0f5;
    content: "";
}

label, [data-testid="stWidgetLabel"] p {
    color: #30425b !important;
}

div[data-baseweb="select"] > div {
    border-color: #d7dee8 !important;
    border-radius: 12px !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: #e99a5c !important;
}

div[data-baseweb="select"] input,
div[data-baseweb="select"] div[role="combobox"] {
    color: #253954 !important;
    -webkit-text-fill-color: #253954 !important;
}

div[data-testid="stNumberInput"] input {
    color: #253954 !important;
    -webkit-text-fill-color: #253954 !important;
    border-color: #d7dee8 !important;
}

div[data-testid="stNumberInput"] button {
    color: #d66e23 !important;
    background-color: #fff3e8 !important;
    border-color: #ead9c9 !important;
}

div[data-testid="stNumberInput"] button:hover {
    color: #a64e12 !important;
    background-color: #ffe4cd !important;
}

div[data-testid="stNumberInput"] input:focus {
    border-color: #e98a3b !important;
    box-shadow: 0 0 0 3px rgba(233, 138, 59, 0.17);
}

.stButton > button {
    min-height: 56px;
    border-radius: 13px;
    background: linear-gradient(105deg, #f29a4b, #e57625);
    box-shadow: 0 9px 20px rgba(218, 112, 33, 0.22);
    letter-spacing: 0.1px;
}

.stButton > button:hover {
    background: linear-gradient(105deg, #f5a65f, #d96a1c);
    box-shadow: 0 12px 25px rgba(218, 112, 33, 0.3);
}

.how-it-works-card {
    display: flow-root;
    background: linear-gradient(155deg, #1a2e49, #102139);
    color: #eef4fc;
    border: 1px solid #263d5a;
    border-radius: 22px;
    padding: 28px 26px;
    box-shadow: 0 16px 36px rgba(16, 33, 57, 0.16);
}

.how-it-works-card .mini-heading {
    color: #ffffff !important;
    font-size: 19px;
    line-height: 1.4;
}

.how-it-works-card .mini-description,
.how-it-works-card .step p {
    color: #d3deec !important;
}

.how-it-works-card .step h4 {
    color: #ffffff !important;
}

.how-it-works-card .step-icon {
    color: #ffb267 !important;
    background: rgba(255, 157, 73, 0.15);
}

.how-it-works-card .step {
    padding-bottom: 17px;
    border-bottom: 1px solid rgba(202, 219, 240, 0.13);
}

.how-it-works-card .step:last-child {
    padding-bottom: 0;
    border-bottom: 0;
}

.price-card {
    color: #ffffff;
    background:
        radial-gradient(ellipse at 92% 10%, rgba(245, 153, 72, 0.2), transparent 35%),
        linear-gradient(115deg, #172b46, #102039);
    border: 1px solid #263d5b;
    border-radius: 23px;
    padding: 30px 34px;
    box-shadow: 0 18px 38px rgba(16, 33, 57, 0.16);
}

.price-icon {
    color: #ffd2a5;
    background: rgba(255, 171, 97, 0.16);
    border: 1px solid rgba(255, 190, 133, 0.18);
}

.price-label {
    color: #c4d2e4;
}

.price-value {
    color: #ffffff;
}

.price-note {
    color: #bdcbe0;
}

.price-status {
    color: #ffe5cc;
    background: rgba(232, 121, 34, 0.16);
    border-color: rgba(255, 183, 117, 0.24);
}

.price-status-dot {
    background: #ffab61;
}

.price-card.is-empty .price-status {
    color: #dbe5f1;
    background: rgba(220, 232, 247, 0.09);
    border-color: rgba(220, 232, 247, 0.16);
}

.price-card.is-empty .price-status-dot {
    background: #a9bad0;
}

.price-card.is-empty .price-value {
    color: #d6e0ed;
}

.price-car {
    opacity: 1;
    filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.2));
}

.footer {
    color: #bdc9d8;
    background: #0e1c30;
    border-radius: 18px;
}

.footer-brand {
    color: #ffffff;
}

@media (max-width: 700px) {
    .hero {
        min-height: 280px;
        padding: 38px 25px;
    }

    .price-card {
        padding: 22px 18px;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------------- NAVIGATION ----------------
st.markdown("""
<div class="navbar">
    <div class="brand">
        <span class="brand-mark">AV</span>
        <span class="brand-name">Auto<span>Value</span></span>
    </div>
    <div class="nav-right"><span class="nav-indicator"></span> USED CAR VALUATION</div>
</div>
""", unsafe_allow_html=True)


# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <div class="hero-copy">
        <div class="hero-tag">SMARTER VALUATION · POWERED BY DATA</div>
        <h1>Know what your car<br>
        <span>could be worth.</span></h1>
        <p>
            Get a data-informed estimate in seconds. Tell us about the car
            and we’ll do the number crunching.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- LOAD MODEL ----------------
try:
    model_data = joblib.load("car_price_model.pkl")
except FileNotFoundError:
    st.error(
        "Model file not found. Run Car_price_prediction.py "
        "to train the model and create car_price_model.pkl."
    )
    st.stop()

if not isinstance(model_data, dict) or model_data.get("version") != 2:
    st.error(
        "The saved model uses an older input format. Run "
        "Car_price_prediction.py again to train the updated model."
    )
    st.stop()

model = model_data["model"]


# ---------------- CAR INPUTS + HOW IT WORKS ----------------
st.markdown('<div class="content-area"></div>', unsafe_allow_html=True)

left, right = st.columns([1.8, 1], gap="large")

with left:
    with st.container(border=True):
        st.markdown("""
        <div class="form-heading">
            <div class="form-heading-icon">🚘</div>
            <div>
                <h2>Vehicle details</h2>
                <p>Enter the information below for your price estimate.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        current_year = datetime.now().year
        st.markdown('<div class="field-group-label">Vehicle identity</div>', unsafe_allow_html=True)
        brand_column, model_column = st.columns(2)
        with brand_column:
            brand = st.selectbox("Brand", list(model_data["brand_models"]))
        with model_column:
            car_model = st.selectbox(
                "Model",
                model_data["brand_models"][brand],
            )

        year_column, km_column = st.columns(2)
        with year_column:
            year = st.number_input(
                "Manufacturing year",
                min_value=1980,
                max_value=current_year,
                value=min(2020, current_year),
                step=1,
            )
        with km_column:
            km_driven = st.number_input(
                "Kilometers driven",
                min_value=0,
                max_value=1_000_000,
                value=30000,
                step=1000,
            )

        st.markdown('<div class="field-group-label">Specifications</div>', unsafe_allow_html=True)
        fuel_column, transmission_column = st.columns(2)
        with fuel_column:
            fuel = st.selectbox("Fuel type", model_data["fuel_options"])
        with transmission_column:
            transmission = st.selectbox(
                "Transmission",
                model_data["transmission_options"],
            )

        owner_column, mileage_column = st.columns(2)
        with owner_column:
            owner = st.selectbox("Previous owners", model_data["owner_options"])
        with mileage_column:
            mileage = st.number_input(
                "Mileage (km/l or km/kg)",
                min_value=0.0,
                max_value=float(model_data["mileage_max"]),
                value=float(model_data["mileage_default"]),
                step=0.1,
                format="%.1f",
            )

        st.write("")

        predict = st.button("Get my price estimate  →", type="primary")

with right:
    st.markdown("""
        <div class="how-it-works-card">
        <div class="mini-heading">A clear estimate, in three steps</div>
        <p class="mini-description">
            A quick guide to how AutoValue turns vehicle details into a price estimate.
        </p>

        <div class="step">
            <div class="step-icon">📝</div>
            <div>
                <h4>01 &nbsp; Add vehicle details</h4>
                <p>Choose the make, model, age, usage and key specifications.</p>
            </div>
        </div>

        <div class="step">
            <div class="step-icon">🧠</div>
            <div>
                <h4>02 &nbsp; Analyze the data</h4>
                <p>Our trained model compares your details with car listings.</p>
            </div>
        </div>

        <div class="step">
            <div class="step-icon">₹</div>
            <div>
                <h4>03 &nbsp; View your estimate</h4>
                <p>Get an instant guide to your car’s estimated selling price.</p>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)


# ---------------- PREDICTION ----------------
if "predicted_price" not in st.session_state:
    st.session_state.predicted_price = None

if predict:
    new_car = pd.DataFrame({
        "brand": [brand],
        "model": [car_model],
        "fuel": [fuel],
        "transmission": [transmission],
        "owner": [owner],
        "year": [year],
        "km_driven": [km_driven],
        "mileage": [mileage],
    })

    st.session_state.predicted_price = float(
        model.predict(new_car)[0]
    )

# ---------------- PRICE RESULT ----------------
if st.session_state.predicted_price is None:
    price_text = "Your estimate is on its way"
    note = "Complete the vehicle details and select “Get my price estimate”."
    price_card_class = "price-card is-empty"
    price_status = "Ready when you are"
else:
    price_text = f"₹ {st.session_state.predicted_price:,.0f}"
    note = (
        f"Estimate for a {year} {brand} {car_model}, "
        f"driven {km_driven:,} km."
    )
    price_card_class = "price-card"
    price_status = "Model estimate"
note = escape(note)

st.markdown(f"""
<div class="{price_card_class}">
    <div class="price-icon">₹</div>
    <div class="price-content">
        <div class="price-status"><span class="price-status-dot"></span> {price_status}</div>
        <div class="price-label">Estimated selling price</div>
        <div class="price-value">{price_text}</div>
        <div class="price-note">{note}</div>
    </div>
    <div class="price-car">🚘</div>
</div>
""", unsafe_allow_html=True)


# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    <div class="footer-brand">Auto<span>Value</span></div>
    <div>Helping you make a more informed decision.</div>
    <div>Model-generated estimate · For guidance only</div>
</div>
""", unsafe_allow_html=True)
