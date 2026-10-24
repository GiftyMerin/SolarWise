import streamlit as st
import pandas as pd
import joblib
from datetime import date, time

st.set_page_config(
    page_title="SolarWise | Predictive Green Energy",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root {
    --bg:#FBFCF9; --surface:rgba(255,255,255,.90); --sage:#E6EEE2;
    --green:#66896A; --forest:#304D39; --olive:#89996D;
    --text:#26382B; --muted:#778277; --line:#E6EBE2;
}
.stApp {background:linear-gradient(rgba(245,249,242,.78),rgba(245,249,242,.82)), url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRWnDw2VdbzqcZD-t3FEXuwFcHGVU8qKeK0S9Pb-FdmRA&s=10') center center / cover fixed no-repeat; color:var(--text); font-family:'DM Sans',sans-serif;}
[data-testid="stAppViewContainer"] {background:transparent;}
[data-testid="stMain"] {background:transparent;}
[data-testid="stMainBlockContainer"] {background:transparent;}
[data-testid="stVerticalBlockBorderWrapper"] {background:rgba(255,255,255,.84) !important; backdrop-filter:blur(8px);}
[data-testid="stMetric"], .metric-card {background:rgba(255,255,255,.90) !important; backdrop-filter:blur(8px);}
[data-testid="stHeader"] {background: linear-gradient(160deg,  rgba(163, 59, 43, 0.22), rgba(163, 59, 43, 0.10)  ) !important;}
.block-container {max-width:1320px; padding-top:1.6rem; padding-bottom:3.5rem;}
h1,h2,h3 {font-family:'Manrope',sans-serif !important; color:var(--forest) !important; letter-spacing:-.8px;}
h2 {font-size:clamp(1.5rem,2.4vw,2rem) !important;}
[data-testid="stSidebar"] {
    background: linear-gradient(
        160deg,
        rgba(163, 59, 43, 0.22),
        rgba(163, 59, 43, 0.10)
    ) !important;
    border-right: 1px solid rgba(163, 59, 43, 0.20);
    box-shadow: 8px 0 28px rgba(38, 56, 43, 0.06);
}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 {color:var(--forest)!important;}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stRadio"] label {color:#71876A !important;}
[data-testid="stSidebar"] [data-testid="stRadio"] > label {font-size:10px!important;font-weight:800!important;letter-spacing:1.8px!important;color:#A33B2B!important;}
[data-testid="stSidebar"] [role="radiogroup"] label {background:rgba(255,255,255,.52);border:1px solid rgba(255,255,255,.8);border-radius:10px;padding:11px 13px;margin:5px 0;transition:all .22s ease;}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {background:#304D39!important;border-color:#304D39!important;transform:translateX(4px);}
[data-testid="stSidebar"] [role="radiogroup"] label:hover * {color:#fff!important;}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {background:#304D39!important;border-color:#304D39!important;box-shadow:0 5px 14px rgba(48,77,57,.18);}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) * {color:#fff!important;}
.sidebar-hero {background:linear-gradient(145deg,rgba(48,77,57,.96),rgba(102,137,106,.93));color:#fff;padding:22px 18px;border-radius:16px;margin:6px 0 18px;box-shadow:0 12px 28px rgba(48,77,57,.16);}
.sidebar-hero .brand {font-family:'Manrope',sans-serif;font-weight:800;font-size:25px;letter-spacing:-.8px;color:#fff;}
.sidebar-hero .tagline {font-size:11px;line-height:1.65;color:rgba(255,255,255,.85);margin-top:10px;}
.sidebar-hero .sun-icon {font-size:30px;margin-bottom:8px;}

.page-hero {background:rgba(245,249,242,.9);backdrop-filter:blur(10px);border:1px solid #E0E9DC;border-radius:14px;padding:24px 28px;margin:0 0 24px;box-shadow:0 10px 30px rgba(38,56,43,.05);}
.page-hero .eyebrow {color:#A33B2B;text-transform:uppercase;letter-spacing:2px;font-size:10px;font-weight:800;}
.page-hero h1 {margin:8px 0 8px;font-size:clamp(26px,3vw,38px);line-height:1.12;}
.page-hero p {margin:0;color:#596B5A;line-height:1.7;font-size:14px;}
.hero {background:rgba(245,249,242,.88);backdrop-filter:blur(8px);padding:clamp(28px,4vw,54px);border-radius:8px;border:1px solid #E0E9DC;margin-bottom:30px;position:relative;overflow:hidden;}
.hero .eyebrow {text-transform:uppercase;letter-spacing:2.4px;font-size:10px;font-weight:800;color:var(--green);}
.hero h1 {font-size:clamp(36px,4.5vw,62px);line-height:1.06;margin:16px 0 18px;max-width:700px;}
.hero p {max-width:610px;font-size:15px;line-height:1.85;color:#596B5A;}
.hero-art {min-height:265px;height:100%;border-radius:8px;background:radial-gradient(ellipse at 52% 48%,rgba(255,255,255,.96) 0%,rgba(255,255,255,.65) 27%,rgba(214,229,207,.85) 58%,rgba(191,214,184,.8) 100%);display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative;}
.image-caption {color:var(--muted);font-size:12px;line-height:1.6;margin-top:5px;margin-bottom:14px;}
.carousel-frame {background:rgba(255,255,255,.86);padding:14px;border:1px solid rgba(230,235,226,.9);border-radius:12px;backdrop-filter:blur(8px);}
.carousel-title {font-family:'Manrope',sans-serif;font-size:20px;font-weight:800;color:var(--forest);margin:4px 0 8px;}
.carousel-description {font-size:13px;line-height:1.7;color:#596B5A;}
[data-testid="stImage"] img {border-radius:8px;object-fit:cover;}
.sun-disc {width:170px;height:170px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#F9FCF4 0%,#D5E5CE 42%,#9DBB94 76%,#7E9F77 100%);box-shadow:0 20px 60px rgba(65,101,65,.14);display:flex;align-items:center;justify-content:center;font-size:64px;color:#547653;position:relative;}
.sun-disc:before,.sun-disc:after {content:"";position:absolute;border:1px solid rgba(89,128,82,.28);border-radius:50%;width:230px;height:230px;transform:rotate(-25deg);}
.sun-disc:after {width:275px;height:130px;transform:rotate(42deg);}
.pill {display:inline-block;background:rgba(255,255,255,.78);color:var(--forest);padding:8px 12px;border:1px solid #D8E2D3;border-radius:3px;font-size:10px;font-weight:800;letter-spacing:1px;}
.metric-card {background:white;border:1px solid var(--line);border-radius:8px;padding:22px;min-height:145px;box-shadow:none;}
.metric-label {color:var(--muted);font-size:12px;font-weight:600;letter-spacing:.2px;}
.metric-value {font-family:'Manrope',sans-serif;color:var(--forest);font-size:28px;font-weight:800;margin:12px 0 6px;overflow-wrap:anywhere;}
.metric-note,.small-muted {color:var(--muted);font-size:12px;line-height:1.7;}
div.stButton>button[kind="primary"] {background:var(--forest);color:white;border:1px solid var(--forest);border-radius:5px;min-height:47px;font-weight:700;letter-spacing:.1px;}
div.stButton>button[kind="primary"]:hover {background:var(--green);color:white;border-color:var(--green);}
/* Brick-red input labels requested: date, time, irradiation and temperatures */
div[data-testid="stNumberInput"] label, div[data-testid="stDateInput"] label, div[data-testid="stTimeInput"] label {color:#A33B2B!important;font-weight:700!important;}
.brick-subheading {font-family:'Manrope',sans-serif;font-size:1.25rem;font-weight:800;color:#A33B2B!important;letter-spacing:-.4px;margin:.35rem 0 1rem;}
/* Smooth, continuously looping image carousel */
.carousel-motion-window {width:100%;overflow:hidden;border-radius:8px;}
.carousel-motion-track {display:flex;width:max-content;animation:solarwise-scroll 32s linear infinite;will-change:transform;}
.carousel-motion-track:hover {animation-play-state:paused;}
.carousel-motion-track img {display:block;width:clamp(240px, 30vw, 380px);height:240px;object-fit:cover;object-position:center;flex:0 0 auto;margin-right:14px;border-radius:8px;}
@keyframes solarwise-scroll {0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
@media(max-width:800px){.carousel-motion-track img{width:78vw;height:190px;margin-right:10px}}
div[data-testid="stNumberInput"] input,div[data-testid="stDateInput"] input,div[data-testid="stTimeInput"] input {border-radius:5px;}
[data-testid="stVerticalBlockBorderWrapper"] {border-color:var(--line) !important;border-radius:8px !important;background:rgba(255,255,255,.65);}
[data-testid="stMetric"] {background:#fff;border:1px solid var(--line);border-radius:8px;padding:16px;}
[data-testid="stMetricLabel"] {color:var(--muted);}
[data-testid="stMetricValue"] {color:var(--forest);}
hr {border-color:var(--line);}
footer {visibility:hidden;}

@media(max-width:800px){.hero{padding:25px 20px}.hero-art{min-height:180px}.sun-disc{width:125px;height:125px;font-size:48px}.metric-value{font-size:22px}}

/* Container to handle drop shadows for clip-path shapes */
.star-card-wrapper {
    position: relative;
    margin: 35px auto;
    width: 100%;
    max-width: 440px;
    filter: drop-shadow(0px 10px 22px rgba(184, 134, 11, 0.22)) 
            drop-shadow(0px 0px 2px #E0BA6E); /* Warm golden border outline */
    transition: transform 0.35s ease;
    animation: floatStar 6s ease-in-out infinite alternate;
}

.star-card-wrapper:hover {
    transform: translateY(-8px) scale(1.02);
}

/* 8-Point Star Card Shape with Gold Gradient */
.cloud-card {
    position: relative;
    /* Radiant Solar Gold Gradient */
    background: linear-gradient(135deg, #FFFDF9 0%, #FFF4D9 45%, #FCE09B 100%);
    
    /* Precise 16-coordinate polygon for an 8-point star */
    clip-path: polygon(
        50% 0%, 
        63% 20%, 
        88% 12%, 
        80% 37%, 
        100% 50%, 
        80% 63%, 
        88% 88%, 
        63% 80%, 
        50% 100%, 
        37% 80%, 
        12% 88%, 
        20% 63%, 
        0% 50%, 
        20% 37%, 
        12% 12%, 
        37% 20%
    );
    
    /* Generous padding so text sits comfortably within the core */
    padding: 105px 75px 100px 75px;
    min-height: 410px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}

/* Remove old cloud puff pseudo-elements */
.cloud-card::before,
.cloud-card::after {
    content: none !important;
}

.cloud-card h3 {
    color: #304D39 !important;
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    font-size: 21px;
    line-height: 1.3;
    margin-bottom: 12px;
    position: relative;
    z-index: 2;
}

.cloud-card p {
    color: #4A5C4B;
    font-size: 14px;
    line-height: 1.7;
    max-width: 250px;
    margin: 0 auto;
    position: relative;
    z-index: 2;
}

/* Gentle Floating Motion */
@keyframes floatStar {
    0% {
        transform: translateY(0px);
    }
    100% {
        transform: translateY(-6px);
    }
}

/* Responsive Mobile Adjustments */
@media (max-width: 800px) {
    .star-card-wrapper {
        max-width: 350px;
    }

    .cloud-card {
        padding: 85px 55px 80px 55px;
        min-height: 340px;
    }

    .cloud-card h3 {
        font-size: 18px;
    }

    .cloud-card p {
        font-size: 13px;
        max-width: 190px;
    }
}

</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load("data/solar_power_model.joblib")

with st.sidebar:
    st.markdown("""
    <div class="sidebar-hero">
      <div class="sun-icon">☀️</div>
      <div class="brand">SolarWise</div>
      <div class="tagline">HOUSEHOLD ENERGY INSIGHTS<br>Learn · Estimate · Save energy</div>
    </div>
    """, unsafe_allow_html=True)
    page = st.radio("EXPLORE SOLARWISE", ["Solar estimator", "Energy offset", "About this project"], key="solarwise_navigation")
    st.divider()
    st.markdown("### 🌿 Our goal")
    st.write("Explore solar power output and understand how clean energy could support your home.")
    st.caption("Machine-learning prototype · Not a utility meter")

page_hero_content = {
    "Solar estimator": ("SOLAR ENERGY · MADE CLEAR", "A brighter future, powered by the sun.", "Explore weather conditions and measurement time to estimate solar plant AC power."),
    "Energy offset": ("HOUSEHOLD ENERGY · MADE CLEAR", "Understand your solar energy offset.", "Explore how solar energy used at home could reduce grid electricity imports and illustrative costs."),
    "About this project": ("THE PROJECT · PREDICTIVE GREEN ENERGY", "Technology for a greener tomorrow.", "Learn how the machine-learning prototype estimates solar power and how to interpret its results."),
}
hero_eyebrow, hero_title, hero_description = page_hero_content[page]
st.markdown(f'<div class="page-hero"><span class="eyebrow">{hero_eyebrow}</span><h1>{hero_title}</h1><p>{hero_description}</p></div>', unsafe_allow_html=True)

# Continuously moving image carousel. It loops automatically and pauses on hover.
carousel_images = [
    {"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlI0-1-h2sbpRECHzRZY1je0K88YE7Q72XEzOpmAT8bg&s=10", "title": "Clean energy in action", "description": "Solar power turns sunlight into useful electricity for homes and communities."},
    {"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQsyGzdsHBmae_1tRdY1tlBGc_Vqj4VTQTxH75Mw_oxNQ&s=10", "title": "A greener tomorrow", "description": "Thoughtful energy choices can support a cleaner, more sustainable future."},
    {"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRclc970cOg1ibfpFuuN6ulMrPnAsqerpdet7TqFCjZiA&s=10", "title": "Nature and sustainability", "description": "Protecting natural ecosystems is an important part of a greener future."},
    {"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQiGaUz39unMr4f7CU8prZzWmgxGS7kNiraiWsVAu_w4g&s=10", "title": "Powering everyday life", "description": "Explore how renewable energy can help reduce reliance on grid electricity."},
    {"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQimzVzsJ8FkpE6vOjq6k7cpLWUbpDpYjdi9o2Lxl7D6g&s=10", "title": "A brighter future", "description": "Small steps toward efficient energy use can add up over time."},
]

st.markdown("### Explore the greener future")
track_images = "".join(f'<img src="{item["url"]}" alt="{item["title"]}">' for item in carousel_images)
# Duplicate the complete image set so the carousel loops seamlessly.
st.markdown(
    '<div class="carousel-frame"><div class="carousel-motion-window"><div class="carousel-motion-track">'
    + track_images + track_images
    + '</div></div></div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="carousel-title">Clean energy, nature, and a brighter future</div>', unsafe_allow_html=True)
#st.markdown('<div class="carousel-description">The images move continuously in a seamless loop. Hover over the carousel to pause it.</div>', unsafe_allow_html=True)

if page == "Solar estimator":
    st.markdown("## Solar power estimator")
    st.markdown('<p class="small-muted">Enter weather conditions and measurement time to estimate AC power with your trained model.</p>', unsafe_allow_html=True)
    try:
        model = load_model()
    except Exception as exc:
        st.error("The trained model could not be loaded. Check that data/solar_power_model.joblib exists.")
        st.code(str(exc))
        st.stop()

    with st.container(border=True):
        st.markdown('<h3 class="brick-subheading"> Weather conditions</h3>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            irradiation = st.number_input("Solar irradiation", min_value=0.0, max_value=2.0, value=0.5, step=0.05, help="Use the same units and range as your training data.")
        with c2:
            ambient_temperature = st.number_input("Ambient temperature (°C)", min_value=-10.0, max_value=60.0, value=25.0, step=1.0)
        with c3:
            module_temperature = st.number_input("Solar module temperature (°C)", min_value=-10.0, max_value=90.0, value=30.0, step=1.0)
        st.markdown('<h3 class="brick-subheading"> Measurement time</h3>', unsafe_allow_html=True)
        c4, c5 = st.columns(2)
        with c4:
            measurement_date = st.date_input("Date", value=date.today())
        with c5:
            measurement_time = st.time_input("Time", value=time(12, 0), step=300)
        predict_clicked = st.button("🔆 Estimate solar power", type="primary", use_container_width=True)

    if predict_clicked:
        input_data = pd.DataFrame([{
            "IRRADIATION": irradiation,
            "AMBIENT_TEMPERATURE": ambient_temperature,
            "MODULE_TEMPERATURE": module_temperature,
            "HOUR": measurement_time.hour,
            "MINUTE": measurement_time.minute,
            "DAY_OF_WEEK": measurement_date.weekday(),
        }])
        try:
            prediction = max(0.0, float(model.predict(input_data)[0]))
            st.session_state["solar_prediction_w"] = prediction
            st.session_state["solar_prediction_time"] = f"{measurement_date:%d %b %Y} · {measurement_time.strftime('%I:%M %p')}"
            st.session_state["solar_prediction_irradiation"] = irradiation
        except Exception as exc:
            st.error("Prediction failed. Check the model and its expected input features.")
            st.code(str(exc))

    if "solar_prediction_w" in st.session_state:
        prediction_w = st.session_state["solar_prediction_w"]
        prediction_kw = prediction_w / 1000
        st.markdown("### Your estimate")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Estimated AC power</div><div class="metric-value">{prediction_w:,.0f} W</div><div class="metric-note">Model output at selected time</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Equivalent power</div><div class="metric-value">{prediction_kw:,.3f} kW</div><div class="metric-note">Watts converted to kilowatts</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Measurement</div><div class="metric-value" style="font-size:18px">{st.session_state["solar_prediction_time"]}</div><div class="metric-note">Selected date and time</div></div>', unsafe_allow_html=True)
        st.success("Prediction completed.")
        if st.session_state.get("solar_prediction_irradiation", 0) == 0:
            st.warning("Irradiation is zero. Actual solar output would normally be zero or close to zero; treat this model output cautiously.")
        st.info("This is plant-level AC power at one measurement time, not household energy produced over a day. Daily energy in kWh requires measurements over time, and household output may differ from the training plant.")
    else:
        st.markdown('<div class="metric-card"><h3>🌱 Ready when you are</h3><p class="small-muted">Enter the weather conditions above and select “Estimate solar power” to view your model result.</p></div>', unsafe_allow_html=True)

elif page == "Energy offset":
    st.markdown("## Household energy offset")
    st.markdown('<p class="small-muted">Explore how solar energy used directly in the home could reduce grid electricity imports.</p>', unsafe_allow_html=True)
    st.info("Enter a daily solar energy value measured or estimated separately. The current ML model predicts power at one time and cannot calculate a full day’s kWh by itself.")
    with st.container(border=True):
        st.markdown("### ⚡ Daily energy inputs")
        c1, c2 = st.columns(2)
        with c1:
            solar_kwh = st.number_input("Solar energy available today (kWh)", min_value=0.0, value=8.0, step=0.5)
            electricity_rate = st.number_input("Grid electricity rate (₹ per kWh)", min_value=0.0, value=6.0, step=0.5)
        with c2:
            usage_kwh = st.number_input("Household electricity usage today (kWh)", min_value=0.0, value=12.0, step=0.5)
            self_use_fraction = st.slider("Share of solar energy used directly at home", 0, 100, 80) / 100
        calculate = st.button("Calculate energy offset", type="primary", use_container_width=True)

    if calculate:
        solar_self_used = solar_kwh * self_use_fraction
        avoided_grid = min(usage_kwh, solar_self_used)
        grid_needed = max(0.0, usage_kwh - avoided_grid)
        surplus = max(0.0, solar_kwh - solar_self_used)
        savings = avoided_grid * electricity_rate
        offset_pct = avoided_grid / usage_kwh * 100 if usage_kwh > 0 else 0.0
        m1, m2, m3 = st.columns(3)
        m1.metric("Grid electricity avoided", f"{avoided_grid:.2f} kWh")
        m2.metric("Estimated grid import", f"{grid_needed:.2f} kWh")
        m3.metric("Illustrative usage-based savings", f"₹{savings:.2f}")
        st.progress(min(1.0, offset_pct / 100))
        st.caption(f"Estimated usage offset: {offset_pct:.1f}%")
        st.bar_chart(pd.DataFrame({"Energy": ["Household usage", "Solar used at home", "Grid needed"], "kWh": [usage_kwh, solar_self_used, grid_needed]}), x="Energy", y="kWh")
        if surplus > 0:
            st.caption(f"{surplus:.2f} kWh of entered solar energy is not used directly under this assumption. It may be exported, stored, or curtailed depending on the system.")
        st.warning("Simplified estimate only. It excludes fixed charges, taxes, export credits, battery losses, time-of-use rates, and utility-specific net-metering rules. Real offset depends on when solar generation and usage occur.")

else:
    st.markdown("## About Predictive Green Energy")

    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown("""
        <div class="cloud-card">
            <h3>Project overview</h3>
            <p>
                This project explores machine learning to estimate solar
                plant AC power using irradiation, ambient temperature,
                module temperature, and measurement time.
            </p>
        </div> <br> 
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="cloud-card">
            <h3> The Difference</h3>
            <p>
                Power (kW) describes the rate of energy production at a
                moment. Energy (kWh) accumulates over time. Daily
                generation requires a time series or a validated
                daily-energy model.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="cloud-card">
            <h3> Machine learning</h3>
            <p>
                The dashboard loads a trained model and sends it the
                features it expects. The output estimates power at
                one measurement time.
            </p>
        </div> <br>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="cloud-card">
            <h3> Household relevance</h3>
            <p>
                The offset calculator uses user-provided daily generation
                and consumption values. It does not read a utility meter
                or predict an official bill.
            </p>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.markdown('<p class="small-muted" style="text-align:center">SOLARWISE · Predictive Green Energy · A machine-learning prototype for learning and exploration</p>', unsafe_allow_html=True)
