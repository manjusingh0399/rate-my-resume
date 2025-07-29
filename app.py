import streamlit as st
import pandas as pd
import plotly.express as px

# Updated Color Palette
BG_COLOR = "#fefaf6"
PINK = "#ff5c8a"
ORANGE = "#ffb347"
TEXT = "#2c2c2c"
WHITE = "#ffffff"

# Streamlit Page Config
st.set_page_config(page_title="Resume vs Reality", page_icon="💼", layout="wide")

# Custom CSS Styling
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {BG_COLOR};
    }}
    h1, h2, h3 {{
        color: {PINK};
    }}
    .section-header {{
        font-size: 1.8em; font-weight: bold; color: {ORANGE};
        margin-top: 1.2em; margin-bottom: 0.4em;
    }}
    .description-box {{
        background-color: {WHITE};
        color: {TEXT};
        padding: 1em;
        border-left: 6px solid {PINK};
        border-radius: 10px;
        margin-bottom: 1em;
        box-shadow: 0 4px 12px #00000010;
    }}
    </style>
""", unsafe_allow_html=True)

# Load example dataset
@st.cache_data
def load_data():
    return pd.DataFrame({
        "Skill": ["Excel", "SQL", "Python", "Communication", "Teamwork", "Power BI", "Market Research"],
        "Job Ads": [92, 76, 68, 45, 41, 32, 29],
        "Resumes": [88, 49, 37, 93, 88, 27, 30],
        "Hires": [64, 54, 55, 37, 31, 18, 15]
    })

skills = load_data()

# --- Header ---
st.markdown(f"<h1 style='text-align:center;'>💡 Resume vs Reality</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:17px; color:{TEXT};'>Friendly data-backed advice on which skills actually get you hired — not just what sounds good on paper.</p>", unsafe_allow_html=True)

# --- Section 1: Skills Overview ---
st.markdown("<div class='section-header'>📊 Skill Frequency Overview</div>", unsafe_allow_html=True)
st.markdown("<div class='description-box'>This chart compares how often certain skills appear in job listings, resumes, and actual hired candidates. Let’s find the overhyped and the underrated!</div>", unsafe_allow_html=True)

fig = px.bar(skills, x="Skill", y=["Job Ads", "Resumes", "Hires"], barmode="group",
             color_discrete_sequence=[PINK, ORANGE, "#9be7ff"],
             title="📊 Skill Frequency: Job Listings vs Resumes vs Hires")
fig.update_layout(
    plot_bgcolor=BG_COLOR, paper_bgcolor=BG_COLOR,
    font_color=TEXT, legend=dict(font=dict(color=TEXT)),
    xaxis=dict(color=TEXT), yaxis=dict(color=TEXT)
)
st.plotly_chart(fig, use_container_width=True)

# --- Section 2: Resume Fit Score ---
st.markdown("<div class='section-header'>🎯 Your Resume Fit Score</div>", unsafe_allow_html=True)
st.markdown("<div class='description-box'>Enter your skills and pick a job role to see how aligned you are — plus some sweet advice on what to improve.</div>", unsafe_allow_html=True)

skills_role = {
    "Analyst": ["SQL", "Python", "Excel"],
    "Marketing": ["Canva", "SEO", "Market Research"],
    "HR": ["Communication", "Recruitment"],
    "Sales": ["Negotiation", "CRM"]
}

col1, col2 = st.columns(2)
with col1:
    user_skills = st.text_input("🎒 Your Skills (comma-separated)", "Excel, Python, Communication")
with col2:
    role = st.selectbox("🎯 Target Role", list(skills_role.keys()))

user_set = set([s.strip().capitalize() for s in user_skills.split(",") if s.strip()])
target_set = set(skills_role.get(role, []))
score = int(100 * len(user_set & target_set) / len(target_set)) if target_set else 0

st.metric("📈 Resume Match Score", f"{score}/100")

missing = target_set - user_set
if score == 100:
    st.success("🌟 You're nailing it! Your skills are perfectly aligned for this role.")
elif score >= 60:
    st.info(f"🛠 You're doing well! Still room for polish: {', '.join(missing)}")
else:
    st.warning(f"📉 Looks like some key skills are missing: {', '.join(missing)}")

# --- Section 3: Friendly Career Advice ---
advice_map = {
    "Python": "Python is the language of data. Learning it opens doors!",
    "SQL": "SQL = 'Speak to the database'. It's essential for Analysts.",
    "Excel": "Master Excel — it's the Swiss Army knife of tools.",
    "Canva": "For marketers, Canva = quick design wins.",
    "SEO": "Want clicks? Learn SEO.",
    "Market Research": "Understand customers and trends — win hearts and markets.",
    "Recruitment": "Talent-finding is core to any HR role.",
    "Communication": "No one hires silence. Communication is gold.",
    "Negotiation": "In sales, closing depends on negotiation.",
    "CRM": "CRM tools help manage leads, deals, and relationships."
}

if missing:
    for skill in missing:
        st.markdown(f"<div class='description-box'>💡 {advice_map.get(skill, 'Consider learning ' + skill.title())}</div>", unsafe_allow_html=True)

# Footer
st.markdown("<hr>")
st.markdown(f"<p style='text-align:center; color:{TEXT}; font-size:14px;'>👩‍💻 Built with data, heart, and just the right amount of sass ✨</p>", unsafe_allow_html=True)
