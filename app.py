import streamlit as st
import pandas as pd
import plotly.express as px

# Color Palette
BG_COLOR = "#fefaf6"
PINK = "#ff5c8a"
ORANGE = "#ffb347"
TEXT = "#2c2c2c"
BLUE = "#82cfff"

st.set_page_config(page_title="Resume vs Reality", page_icon="💼", layout="wide")

# Custom CSS
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {BG_COLOR};
    }}
    h1, h2, h3 {{
        color: {PINK};
    }}
    .section-header {{
        font-size: 1.8em;
        font-weight: bold;
        color: {ORANGE};
        margin-top: 1.2em;
        margin-bottom: 0.4em;
    }}
    .description-box {{
        background-color: white;
        color: {TEXT};
        padding: 1em;
        border-left: 6px solid {PINK};
        border-radius: 10px;
        margin-bottom: 1em;
        box-shadow: 0 4px 12px #00000010;
    }}
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.DataFrame({
        "Skill": ["Excel", "SQL", "Python", "Communication", "Teamwork", "Power BI", "Market Research"],
        "Job Ads": [92, 76, 68, 45, 41, 32, 29],
        "Resumes": [88, 49, 37, 93, 88, 27, 30],
        "Hires": [64, 54, 55, 37, 31, 18, 15]
    })

skills_data = load_data()
skills_role = {
    "Analyst": ["SQL", "Python", "Excel"],
    "Marketing": ["Canva", "SEO", "Market Research"],
    "HR": ["Communication", "Recruitment"],
    "Sales": ["Negotiation", "CRM"]
}
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

st.markdown("""<h1 style='text-align:center;'>💡 Resume vs Reality</h1>""", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:17px; color:{TEXT};'>Discover how your skills compare to real hiring trends, and get tailored suggestions to grow your edge. 📈</p>", unsafe_allow_html=True)

# Tabs layout
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 Fit Score", "💡 Suggestions", "ℹ️ About"])

# === Overview Tab ===
with tab1:
    st.markdown("<div class='section-header'>📊 Skills Across Sources</div>", unsafe_allow_html=True)
    st.markdown("<div class='description-box'>This chart shows how frequently certain skills appear in job descriptions, resumes, and among hired profiles. 👀 Spot the underrated gems and the resume fluff!</div>", unsafe_allow_html=True)

    fig = px.bar(skills_data, x="Skill", y=["Job Ads", "Resumes", "Hires"], barmode="group",
                 color_discrete_sequence=[PINK, ORANGE, BLUE])
    fig.update_layout(
        plot_bgcolor=BG_COLOR, paper_bgcolor=BG_COLOR,
        font_color=TEXT, legend=dict(font=dict(color=TEXT)),
        xaxis=dict(color=TEXT), yaxis=dict(color=TEXT)
    )
    st.plotly_chart(fig, use_container_width=True)

# === Fit Score Tab ===
with tab2:
    st.markdown("<div class='section-header'>🎯 Check Your Resume Fit</div>", unsafe_allow_html=True)
    st.markdown("<div class='description-box'>Enter your skills and choose a role to see how aligned you are with real job expectations.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        input_skills = st.text_input("Your Skills (comma-separated)", "Excel, Python, Communication")
    with col2:
        role = st.selectbox("Choose Target Role", list(skills_role.keys()))

    user_set = set([x.strip().capitalize() for x in input_skills.split(",") if x.strip()])
    target_set = set(skills_role.get(role, []))
    match_score = int(100 * len(user_set & target_set) / len(target_set)) if target_set else 0

    st.metric("Resume Fit Score", f"{match_score}/100")
    st.progress(match_score)

    missing = target_set - user_set
    if missing:
        st.warning(f"You're missing these key skills: {', '.join(missing)}")

# === Suggestions Tab ===
with tab3:
    st.markdown("<div class='section-header'>💡 Skill Advice</div>", unsafe_allow_html=True)
    st.markdown("<div class='description-box'>Here’s what you can learn to become a stronger fit. These suggestions are tailored to your missing skills.</div>", unsafe_allow_html=True)

    if missing:
        for skill in missing:
            st.markdown(f"<div class='description-box'>🌱 <b>{skill}</b>: {advice_map.get(skill, 'Try learning ' + skill.title())}</div>", unsafe_allow_html=True)
    else:
        st.success("You're doing great! You match all key skills for this role 🎉")

# === About Tab ===
with tab4:
    st.markdown("<div class='section-header'>ℹ️ About</div>", unsafe_allow_html=True)
    st.markdown("<div class='description-box'>This app compares resume data, job listings, and hiring records to help you build a smarter skill strategy. Designed to guide, not overwhelm — like a career-savvy older sister with data skills 😉</div>", unsafe_allow_html=True)
    st.write("Built with ❤️ using Streamlit + Plotly + Pandas")
