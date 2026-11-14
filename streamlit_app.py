import html

import streamlit as st

st.set_page_config(page_title="Smart Plant Watering", page_icon="🌱", layout="centered")

# Visual style: deep forest background, warm wheat and sage accents,
# and a serif display face for headings and the moisture reading.
STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Inter:wght@400;500;600&display=swap');

:root {
  --bg: #0E1813;
  --card: #17241D;
  --line: #2C3F34;
  --text: #EDE7D9;
  --muted: #A9B5AA;
  --wheat: #E2B65A;
  --sage: #8FB996;
  --clay: #D9826A;
  --water: #7FB8C4;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
  background: var(--bg) !important;
  font-family: Inter, system-ui, sans-serif;
  color: var(--text);
}
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 720px; padding-top: 3rem; padding-bottom: 4rem; }

h1 {
  font-family: Fraunces, Georgia, serif !important;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.5px;
  margin-bottom: 0.2rem;
}
.subtitle { color: var(--muted); font-size: 1.05rem; margin: 0 0 2rem 0; }

label, [data-testid="stWidgetLabel"] p { color: var(--muted) !important; font-weight: 500; }

div[data-testid="stTextInput"] input {
  background: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--line) !important;
  border-radius: 12px !important;
}
div[data-testid="stTextInput"] input:focus {
  border-color: var(--water) !important;
  box-shadow: 0 0 0 2px rgba(127, 184, 196, 0.25) !important;
}

div[data-testid="stSlider"] [role="slider"] {
  background: var(--wheat) !important;
  border: 2px solid var(--bg) !important;
}

.stButton > button {
  background: var(--sage);
  color: #0E1813;
  border: none;
  border-radius: 999px;
  padding: 0.6rem 2.2rem;
  font-weight: 600;
  margin-top: 0.5rem;
}
.stButton > button:hover { background: #a6cca9; color: #0E1813; border: none; }
.stButton > button:focus:not(:active) { box-shadow: 0 0 0 3px var(--water); }

.result {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 28px;
  margin-top: 28px;
}
.result .plant { color: var(--muted); font-size: 0.95rem; margin: 0; }
.reading {
  font-family: Fraunces, Georgia, serif;
  font-size: 2.6rem;
  color: var(--wheat);
  margin: 2px 0 10px 0;
  line-height: 1.1;
}
.branches { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 18px 0; }
.branch {
  border-radius: 14px;
  padding: 14px 8px;
  text-align: center;
  border: 2px solid transparent;
  opacity: 0.3;
  color: #0E1813;
}
.branch.active { opacity: 1; border-color: var(--text); }
.b-dry { background: var(--clay); }
.b-mod { background: var(--wheat); }
.b-wet { background: var(--water); }
.branch strong { display: block; font-size: 0.95rem; }
.branch span { display: block; font-size: 0.85rem; margin-top: 4px; }
.rec { color: var(--text); font-weight: 600; margin: 6px 0; font-size: 1.05rem; }
.advice { color: var(--muted); margin: 6px 0 0 0; line-height: 1.6; }
</style>
"""


def decide(moisture):
    """Return the flowchart branch for a moisture percentage."""
    if moisture < 30:
        return {
            "key": "dry",
            "status": "Dry",
            "action": "Water the plant now.",
            "advice": "The soil is too dry. Give the plant a full watering and check again later.",
        }
    if moisture < 60:
        return {
            "key": "mod",
            "status": "Moderate",
            "action": "Give only a little water.",
            "advice": "The soil has enough moisture. A small amount of water is enough for now.",
        }
    return {
        "key": "wet",
        "status": "Wet",
        "action": "Do not water.",
        "advice": "The soil is already wet. Watering now could cause root rot, so skip it.",
    }


def branch_class(active_key, key, base):
    return f"branch {base}{' active' if active_key == key else ''}"


st.markdown(STYLE, unsafe_allow_html=True)

st.title("🌱 Smart Plant Watering")
st.markdown(
    '<p class="subtitle">Check your plant\'s soil moisture and get a watering recommendation.</p>',
    unsafe_allow_html=True,
)

plant_name = st.text_input("Enter plant name", placeholder="For example: Money plant")
moisture = st.slider("Soil moisture (%)", min_value=0, max_value=100, value=40)

if st.button("Analyse"):
    if not plant_name.strip():
        st.warning("Please enter a plant name.")
    else:
        decision = decide(moisture)
        safe_name = html.escape(plant_name.strip())

        st.markdown(
            f"""
<div class="result">
  <p class="plant">Report for {safe_name}</p>
  <div class="reading">{moisture}% {decision["status"]}</div>
  <div class="branches">
    <div class="{branch_class(decision["key"], "dry", "b-dry")}">
      <strong>Below 30%</strong><span>Dry</span><span>Water plant</span>
    </div>
    <div class="{branch_class(decision["key"], "mod", "b-mod")}">
      <strong>30 to 59%</strong><span>Moderate</span><span>Little water</span>
    </div>
    <div class="{branch_class(decision["key"], "wet", "b-wet")}">
      <strong>60 to 100%</strong><span>Wet</span><span>No watering</span>
    </div>
  </div>
  <p class="rec">Recommendation: {decision["action"]}</p>
  <p class="advice">{decision["advice"]}</p>
</div>
""",
            unsafe_allow_html=True,
        )
