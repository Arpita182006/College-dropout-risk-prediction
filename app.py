import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go
from pathlib import Path

# -------------------- Page configuration --------------------
st.set_page_config(
    page_title="StudentPulse | Dropout Risk AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- Load model --------------------
MODEL_PATH = Path(__file__).parent / "dropout_risk.pkl"

@st.cache_resource
def load_model(path):
    with open(path, "rb") as file:
        return pickle.load(file)

# -------------------- Styling --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root { --ink:#ffffff; --muted:#d1e0e8; --panel:#102633; --line:#365765; --teal:#62f5d4; }
.stApp {
    background: radial-gradient(circle at 85% 0%, #123f49 0, #0b202d 35%, #081721 75%);
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: #0b1c27; border-right: 1px solid #25414e; }
[data-testid="stSidebar"] * { color: #eaf3f7; }
h1,h2,h3 { font-family: 'Manrope', sans-serif !important; color: #ffffff !important; }
p, li, label, span, div, small { }
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li { color: #f1f7fa; }
.stCaption, [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {
    color: #c4d6df !important;
}
label, [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label {
    color: #f4fbff !important; font-weight: 600 !important;
}
input, textarea, [data-baseweb="select"] *, [data-baseweb="input"] input {
    color: #ffffff !important;
}
[data-testid="stNumberInput"] button { color: #ffffff !important; background:#25414e !important; }
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] { color:#e4eef3 !important; }
[data-testid="stAlert"] p, [data-testid="stAlert"] div { color:#ffffff !important; }
.stApp a { color:#70f3dc !important; }
.hero {
    padding: 28px 30px; border: 1px solid #28505b; border-radius: 24px;
    background: linear-gradient(115deg, rgba(20,63,74,.95), rgba(12,36,49,.95));
    margin-bottom: 22px; box-shadow: 0 18px 55px rgba(0,0,0,.16);
}
.eyebrow { color: #48dfc1; text-transform: uppercase; letter-spacing: 2px; font-size: .75rem; font-weight: 800; }
.hero-title { font-family: 'Manrope',sans-serif; font-size: clamp(2rem,4vw,3.2rem); line-height:1.12; font-weight:800; margin: 9px 0 12px; }
.hero-copy { color:#e1edf2 !important; max-width:760px; font-size:1rem; line-height:1.7; }
.pill { display:inline-block; padding:6px 11px; border-radius:99px; border:1px solid #5b8995; background:#143b44; color:#d8fff6 !important; font-size:.78rem; margin-right:6px; margin-top:14px; }
.panel {
    background: rgba(16,38,51,.88); border:1px solid #25414e; border-radius:20px;
    padding:20px 22px; margin-bottom:16px;
}
.panel-label { color:#d2e2e9 !important; font-size:.82rem; font-weight:700; letter-spacing:.7px; text-transform:uppercase; }
.metric { font-family:'Manrope',sans-serif; font-size:1.85rem; font-weight:800; color:#ffffff !important; margin-top:6px; }
.small-copy { color:#c9dbe3 !important; font-size:.88rem; line-height:1.55; }
.section-title { font-family:'Manrope',sans-serif; font-size:1.15rem; font-weight:800; margin:4px 0 3px; }
div.stButton > button[kind="primary"] {
    background: linear-gradient(100deg,#39d9bb,#64e8ce); color:#08222a; border:0;
    border-radius:12px; min-height:3.1rem; font-weight:800; width:100%;
}
div.stButton > button[kind="primary"]:hover { background:#8af3df; color:#08222a; }
div[data-testid="stNumberInput"] input, div[data-testid="stSelectbox"] div,
div[data-testid="stSlider"] { border-radius:10px; }
hr { border-color:#25414e; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("## 🎓 StudentPulse")
    st.caption("AI-assisted student success insights")
    st.divider()
    st.markdown("### About this tool")
    st.write("Estimate a student's dropout-risk output from academic, wellbeing, and support indicators.")
    st.info("Use this as a screening aid—not as a final decision about any student.")
    st.markdown("**Model file**")
    st.code("dropout_risk.pkl", language="text")
    st.caption("Keep this file in the same folder as app.py.")

# -------------------- Header --------------------
st.markdown("""
<div class="hero">
  <div class="eyebrow">Student success • Predictive insights</div>
  <div class="hero-title">Understand risk.<br>Support potential.</div>
  <div class="hero-copy">A student-first dashboard that brings academic progress, wellbeing, and support indicators together to help identify where extra support may be useful.</div>
  <span class="pill">✦ Machine learning</span><span class="pill">◈ Student wellness</span><span class="pill">↗ Actionable insights</span>
</div>
""", unsafe_allow_html=True)

# -------------------- Inputs --------------------
st.markdown("## Build a student profile")
st.markdown('<p class="small-copy">Enter the available details below, then run the model to see its output.</p>', unsafe_allow_html=True)

with st.form("student_profile"):
    left, right = st.columns(2, gap="large")

    with left:
        st.markdown('<div class="section-title">📘 Academic performance</div>', unsafe_allow_html=True)
        st.markdown('<p class="small-copy">Learning progress and study habits</p>', unsafe_allow_html=True)
        current_gpa = st.number_input("Current GPA (0.0–4.0)", min_value=0.0, max_value=4.0, step=0.1, value=2.5)
        attendance_rate = st.number_input("Attendance rate (%)", min_value=0.0, max_value=100.0, step=1.0, value=75.0)
        study_hours = st.number_input("Study hours per week", min_value=0.0, max_value=80.0, step=1.0, value=15.0)

    with right:
        st.markdown('<div class="section-title">🌿 Wellbeing & support</div>', unsafe_allow_html=True)
        st.markdown('<p class="small-copy">Context that may affect a student’s experience</p>', unsafe_allow_html=True)
        financial_stress = st.slider("Financial stress (1 = low, 10 = high)", 1, 10, 5)
        mental_health_score = st.slider("Mental health score (1–10)", 1, 10, 6, help="Use the same scale and meaning used when training your model.")
        part_time_job_label = st.selectbox("Has a part-time job?", ["No", "Yes"])
        parental_support = st.select_slider("Parental support level", options=["low", "medium", "high"], value="medium")

    submitted = st.form_submit_button("✨  Predict dropout risk", type="primary", use_container_width=True)

# -------------------- Live profile overview --------------------
st.markdown("---")
st.markdown("### Profile snapshot")
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="panel"><div class="panel-label">GPA</div><div class="metric">{current_gpa:.1f}<span style="font-size:1rem;color:#9fb4c2"> / 4.0</span></div><div class="small-copy">Academic progress</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="panel"><div class="panel-label">Attendance</div><div class="metric">{attendance_rate:.0f}%</div><div class="small-copy">Class participation</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="panel"><div class="panel-label">Study time</div><div class="metric">{study_hours:.0f}<span style="font-size:1rem;color:#9fb4c2"> hrs/wk</span></div><div class="small-copy">Weekly study hours</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="panel"><div class="panel-label">Support</div><div class="metric" style="text-transform:capitalize">{parental_support}</div><div class="small-copy">Parental support level</div></div>', unsafe_allow_html=True)

# -------------------- Prediction --------------------
if submitted:
    try:
        pipe = load_model(MODEL_PATH)
        input_data = pd.DataFrame([{
            "current_gpa": current_gpa,
            "attendance_rate": attendance_rate,
            "study_hours_per_week": study_hours,
            "financial_stress": financial_stress,
            "mental_health_score": mental_health_score,
            "part_time_job": 1 if part_time_job_label == "Yes" else 0,
            "parental_support": parental_support.lower(),
        }])

        result = float(pipe.predict(input_data)[0])
        # This display assumes the model returns a value between 0 and 1.
        if 0 <= result <= 1:
            risk_pct = result * 100
            if result < 0.3:
                level, color, emoji = "Low risk", "#48df9a", "🟢"
                message = "The model output is in the lower range. Continue reinforcing positive study habits and support."
                actions = ["Recognize current effort and progress.", "Keep regular check-ins with the student.", "Maintain access to academic and wellbeing resources."]
            elif result < 0.7:
                level, color, emoji = "Moderate risk", "#ffc766", "🟡"
                message = "The model output is in the middle range. A supportive check-in may help identify barriers early."
                actions = ["Discuss attendance, workload, and study routines.", "Ask whether financial or personal support is needed.", "Agree on one or two achievable next steps."]
            else:
                level, color, emoji = "High risk", "#ff7d89", "🔴"
                message = "The model output is in the higher range. Consider a timely, non-judgmental conversation and offer appropriate support."
                actions = ["Connect the student with an academic advisor.", "Offer information about financial aid and student services.", "Make a follow-up plan with the student's consent."]

            st.markdown("---")
            st.markdown("## Your prediction")
            result_col, detail_col = st.columns([1, 1.35], gap="large")
            with result_col:
                st.markdown(f"""
                <div class="panel" style="text-align:center;border-color:{color}66">
                  <div class="panel-label">Model output</div>
                  <div style="font-size:3rem;margin:10px 0 0">{emoji}</div>
                  <div class="metric" style="font-size:2.6rem;color:{color}">{risk_pct:.1f}%</div>
                  <div style="font-size:1.2rem;font-weight:800;color:{color}">{level}</div>
                  <div class="small-copy" style="margin-top:10px">Displayed as output × 100</div>
                </div>
                """, unsafe_allow_html=True)
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=risk_pct,
                    number={"suffix": "%", "font": {"size": 26, "color": "#eaf3f7"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "#9fb4c2"},
                        "bar": {"color": color},
                        "bgcolor": "#102633",
                        "bordercolor": "#25414e",
                        "steps": [
                            {"range": [0, 30], "color": "#163f3a"},
                            {"range": [30, 70], "color": "#4b3d28"},
                            {"range": [70, 100], "color": "#4a2b35"},
                        ],
                        "threshold": {"line": {"color": "#ffffff", "width": 3}, "thickness": 0.8, "value": risk_pct},
                    },
                ))
                fig.update_layout(height=230, margin=dict(l=15, r=15, t=15, b=10), paper_bgcolor="rgba(0,0,0,0)", font_color="#eaf3f7")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            with detail_col:
                st.markdown(f'<div class="panel"><div class="section-title">What this may mean</div><p class="small-copy">{message}</p></div>', unsafe_allow_html=True)
                st.markdown('<div class="panel"><div class="section-title">Suggested supportive next steps</div>', unsafe_allow_html=True)
                for action in actions:
                    st.markdown(f"- {action}")
                st.markdown("</div>", unsafe_allow_html=True)
                st.caption("Important: These bands are illustrative thresholds. Validate them against your model's training target and evaluation before using them in real settings.")
        else:
            st.warning(f"The model returned {result:.4f}, which is outside the expected 0–1 range. Your model may be predicting a class label or a different score. Check the model's target and output before converting it to a percentage.")
    except FileNotFoundError:
        st.error("Could not find dropout_risk.pkl. Put the model file in the same folder as this Python file.")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.info("Check that the input column names and data types match the model's training pipeline.")

st.markdown("---")
st.markdown('<p class="small-copy" style="text-align:center">StudentPulse • Built to encourage early support, not label students.</p>', unsafe_allow_html=True)
