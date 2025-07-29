import streamlit as st
import pandas as pd
import plotly.express as px

# Theme Colors
BLACK = "#18181b"
PINK = "#ff4da6"
WHITE = "#f9fafb"
ORANGE = "#ffa07a"

# Streamlit Page Config
st.set_page_config(page_title="Resume vs Reality", page_icon="✨", layout="wide")

# Styling
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {BLACK};
    }}
    h1, h2, h3, h4 {{
        color: {PINK};
    }}
    .section-header {{
        font-size: 1.8em; font-weight: bold; color: {ORANGE};
        margin-top: 1.2em; margin-bottom: 0.3em;
    }}
    .description-box {{
        background-color: {WHITE}; color: {BLACK};
        padding: 1em; border-radius: 8px;
        margin-bottom: 1em; box-shadow: 0 2px 10px #0003;
    }}
    </style>
""", unsafe_allow_html=True)

# Load example dataset (replace with actual processed data)
@st.cache_data
def load_data():
    return pd.DataFrame({
        "Skill": ["Excel", "SQL", "Python", "Communication", "Teamwork", "Power BI", "Market Research"],
        "Job Ads": [92, 76, 68, 45, 41, 32, 29],
        "Resumes": [88, 49, 37, 93, 88, 27, 30],
        "Hires": [64, 54, 55, 37, 31, 18, 15]
    })

skills = load_data()

# Page Header
st.markdown("<h1 style='text-align:center;'>✨ Resume vs Reality</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Let’s cut through the fluff — here’s what actually gets you hired 👀</p>", unsafe_allow_html=True)

# Section 1: Overview of Skills
st.markdown("<div class='section-header'>📊 Skill Landscape</div>", unsafe_allow_html=True)
st.markdown("<div class='description-box'>This chart shows how often key skills appear in job ads, resumes, and among hires. Spot what’s hot, what’s not, and what’s oversold.</div>", unsafe_allow_html=True)

fig = px.bar(skills, x="Skill", y=["Job Ads", "Resumes", "Hires"], barmode="group",
             color_discrete_sequence=[PINK, WHITE, "#65fcda"],
             title="Skill Frequency: Job Listings vs Resumes vs Hires")
fig.update_layout(
    plot_bgcolor=BLACK, paper_bgcolor=BLACK, font_color=WHITE,
    legend=dict(font=dict(color=WHITE)), xaxis=dict(color=WHITE), yaxis=dict(color=WHITE)
)
st.plotly_chart(fig, use_container_width=True)

# Section 2: Personalized Fit Checker
st.markdown("<div class='section-header'>🎯 Resume Fit Score</div>", unsafe_allow_html=True)
st.markdown("<div class='description-box'>Drop in your skills and select your target job. We’ll give you your fit score, point out missing areas, and coach you on what to learn next.</div>", unsafe_allow_html=True)

skills_role = {
    "Analyst": ["SQL", "Python", "Excel"],
    "Marketing": ["Canva", "SEO", "Market Research"],
    "HR": ["Communication", "Recruitment"],
    "Sales": ["Negotiation", "CRM"]
}

col1, col2 = st.columns(2)
with col1:
    user_skills = st.text_input("Your Skills (comma-separated)", "Excel, Python, Communication")
with col2:
    role = st.selectbox("Target Role", list(skills_role.keys()))

user_set = set([s.strip().capitalize() for s in user_skills.split(",") if s.strip()])
target_set = set(skills_role.get(role, []))
score = int(100 * len(user_set & target_set) / len(target_set)) if target_set else 0

st.metric("📈 Resume Match Score", f"{score}/100")

missing = target_set - user_set
if score == 100:
    st.success("💥 Perfect Match! You're resume-ready for this role!")
elif score >= 60:
    st.info(f"⚡ Pretty good! You might still want to pick up: {', '.join(missing)}")
else:
    st.warning(f"📉 Hmm… time to level up with: {', '.join(missing)}")

# Section 3: Tailored Advice
advice_map = {
    "Python": "Python is the real MVP for data roles — get comfy with it.",
    "SQL": "Without SQL, you're skipping the language of databases.",
    "Excel": "Spreadsheets aren't sexy, but Excel is essential.",
    "Canva": "For marketing? Canva is your creative BFF.",
    "SEO": "SEO = Visibility. It’s your digital megaphone.",
    "Market Research": "Know the market. Own the strategy.",
    "Recruitment": "No HR game without sourcing like a pro.",
    "Communication": "Talk the talk — soft skills close the deal.",
    "Negotiation": "Sales 101: Win hearts, close deals.",
    "CRM": "CRM tools = Organized selling + Better pipelines."
}

for skill in missing:
    st.markdown(f"<div class='description-box'>💡 {advice_map.get(skill, 'Add ' + skill.title())}</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; font-size:14px;'>🚀 Built with love to demystify hiring. No gatekeeping, just glow-ups.</p>", unsafe_allow_html=True)
