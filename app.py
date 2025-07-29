import streamlit as st
import pandas as pd
import plotly.express as px

# Theme colors
BG_COLOR = "#fffdf9"
PINK = "#ff5c8a"
ORANGE = "#ffb347"
TEXT = "#2c2c2c"
BLUE = "#82cfff"

st.set_page_config(page_title="Resume vs Reality", page_icon="📄", layout="wide")

# Custom CSS
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {BG_COLOR};
        color: {TEXT};
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

# Dummy data (replace with your own in production)
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

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Welcome", "📊 Skill Insights", "🎯 Fit Score", "💡 Suggestions", "ℹ️ About"])

# --- Tab 1: Welcome ---
with tab1:
    st.markdown("<h1 style='text-align:center;'>✨ Welcome to Resume vs Reality</h1>", unsafe_allow_html=True)

    st.markdown(f"""
        <div class='description-box'>
            <h3 style="color:{PINK};">Why this App Exists</h3>
            <p>You're here because you're ready to stop guessing and start growing. This app helps you bridge the gap between what you put on your resume and what actually gets people hired.</p>
            <ul>
                <li>📌 Discover which skills matter across resumes, job ads, and real hires</li>
                <li>📈 Check how well your skills match a role</li>
                <li>💡 Get suggestions on how to improve</li>
            </ul>
            <p>Each tab walks you through a real, supportive journey — from insight to action. Built for job seekers, by one of them.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class='description-box'>
            <h3 style="color:{ORANGE};">👋 A Word from the Developer</h3>
            <p>Hi! I'm Manju – an MBA student, a data enthusiast, and just like you — someone who's chasing opportunities and feeling all the uncertainties that come with it.</p>
            <p>I created this app out of my own job-search anxiety. I wanted to transform that anxiety into something empowering — into a light in the dark for anyone who’s struggling with where to begin or how to improve.</p>
            <p>So take a breath, dig in, and let the data show you where you shine and where you can grow. Let’s build something together.</p>
            <p style="color:{PINK};"><i>“You’re not behind. You’re building. Let’s make those skills count.”</i></p>
        </div>
    """, unsafe_allow_html=True)

# --- Tab 2: Skill Insights ---
with tab2:
    st.markdown("<div class='section-header'>📊 What Skills Appear Where?</div>", unsafe_allow_html=True)
    st.markdown("<div class='description-box'>Compare how often each skill appears in job ads, resumes, and among people who actually got hired.</div>", unsafe_allow_html=True)

    fig = px.bar(skills_data, x="Skill", y=["Job Ads", "Resumes", "Hires"], barmode="group",
                 color_discrete_sequence=[PINK, ORANGE, BLUE])
    fig.update_layout(
        plot_bgcolor=BG_COLOR, paper_bgcolor=BG_COLOR,
        font_color=TEXT, legend=dict(font=dict(color=TEXT)),
        xaxis=dict(color=TEXT), yaxis=dict(color=TEXT)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 3: Fit Score ---
with tab3:
    st.markdown("<div class='section-header'>🎯 How Well Do You Fit?</div>", unsafe_allow_html=True)
    st.markdown("<div class='description-box'>Enter your skills and role to see your resume's relevance score and how close you are to nailing the job!</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        input_skills = st.text_input("🧾 Your Skills (comma-separated)", "Excel, Python, Communication")
    with col2:
        role = st.selectbox("🎯 Target Role", list(skills_role.keys()))

    user_set = set([x.strip().capitalize() for x in input_skills.split(",") if x.strip()])
    target_set = set(skills_role.get(role, []))
    match_score = int(100 * len(user_set & target_set) / len(target_set)) if target_set else 0

    st.metric("Resume Fit Score", f"{match_score}/100")
    st.progress(match_score)

    missing = target_set - user_set
    if missing:
        st.warning(f"🧩 You're missing: {', '.join(missing)}")
    else:
        st.success("✅ Perfect match! You’re ready for this role!")

# --- Tab 4: Suggestions ---
with tab4:
    st.markdown("<div class='section-header'>💡 Where You Can Grow</div>", unsafe_allow_html=True)
    st.markdown("<div class='description-box'>Based on your match, here’s what you can improve to get closer to that dream role.</div>", unsafe_allow_html=True)

    if missing:
        for skill in missing:
            st.markdown(f"<div class='description-box'>🌱 <b>{skill}</b>: {advice_map.get(skill, 'Try learning ' + skill.title())}</div>", unsafe_allow_html=True)
    else:
        st.success("🎉 You're already rocking the skills this role needs!")

# --- Tab 5: About ---
with tab5:
    st.markdown("<div class='section-header'>ℹ️ About Resume vs Reality</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class='description-box'>
            This app is designed to demystify the job hunt. It’s based on comparing skill sets across resumes, job ads, and actual hires.
            <br><br>
            Rather than throwing buzzwords on a page, you’ll learn what really gives people an edge — and how to build your own edge.
            <br><br>
            Created with ❤️ by Manju Singh — aspiring analyst, MBA student, and fellow job seeker.
        </div>
    """, unsafe_allow_html=True)
