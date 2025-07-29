import streamlit as st
import pandas as pd
import plotly.express as px

# --- Theme Colors ---
BLACK = "#18181b"
PINK = "#ff4da6"
WHITE = "#f9fafb"
GRAY = "#232329"
ORANGE = "#ffa07a"

# --- Streamlit Page Settings ---
st.set_page_config(
    page_title="Resume vs Reality",
    page_icon="✨",
    layout="wide"
)

# --- Custom Styling ---
st.markdown(
    f"""
    <style>
    body {{background: {BLACK}; color: {WHITE};}}
    .css-10trblm {{color: {PINK}!important;}}
    .insight-card {{
        border-radius:13px; background:{WHITE}; color:{BLACK};
        font-size:1.1rem; margin:1.5em 0 .8em 0; padding:1.2em;
        border-left:7px solid {PINK}; box-shadow:0 2px 8px #0002;
    }}
    .big-header {{
        font-size:2.4em; font-weight:bold; color:{PINK};
        text-shadow:0 2px 18px #0007;
        margin-top:.7em; margin-bottom:.2em;
    }}
    </style>
    """, unsafe_allow_html=True
)

# --- Sidebar Navigation ---
st.sidebar.image("https://img.icons8.com/emoji/96/fairy.png", width=70)
st.sidebar.title("✨ Navigation")
menu = st.sidebar.radio("Jump to", [
    "🏠 Welcome",
    "📊 Insights",
    "📈 Role Explorer",
    "🎯 Score & Feedback",
    "ℹ️ About"
])

# --- Dummy Dataset (Replace with your real data) ---
@st.cache_data
def load_data():
    skills = pd.DataFrame({
        "Skill": ["Excel", "SQL", "Python", "Communication", "Teamwork", "Power BI", "Market Research"],
        "Job Ads": [92, 76, 68, 45, 41, 32, 29],
        "Resumes": [88, 49, 37, 93, 88, 27, 30],
        "Hires": [64, 54, 55, 37, 31, 18, 15]
    })
    return skills

skills = load_data()

# --- Core Role Skills (Dummy) ---
skills_role = {
    "Analyst": ["SQL", "Python", "Excel"],
    "Marketing": ["Canva", "SEO", "Market Research"],
    "HR": ["Communication", "Recruitment"],
    "Sales": ["Negotiation", "CRM"]
}

# --- Content Sections ---
if menu == "🏠 Welcome":
    st.markdown(f'<div class="big-header">✨ Resume vs Reality</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="insight-card">Welcome! Think of this as your stylish, brutally honest older sister telling you what *actually* lands the job. Data doesn’t lie—but it can sparkle! 💅</div>',
        unsafe_allow_html=True)
    st.markdown("Use the sidebar to explore skills, roles, and your hiring potential. Let’s glow up your resume! 💖")

elif menu == "📊 Insights":
    st.markdown("<h2 style='color:#ff4da6;'>Key Skill Insights</h2>", unsafe_allow_html=True)
    
    # Bar Chart
    fig = px.bar(
        skills, x="Skill", y=["Job Ads", "Resumes", "Hires"],
        barmode="group", color_discrete_sequence=[PINK, WHITE, "#65fcda"]
    )
    fig.update_layout(
        plot_bgcolor=BLACK, paper_bgcolor=BLACK, font_color=WHITE,
        legend=dict(font=dict(color=WHITE)), xaxis=dict(color=WHITE), yaxis=dict(color=WHITE)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="insight-card">💡 <b>Insight:</b> Resumes love soft skills like "Teamwork", but hiring favors actual tools—Python, SQL, and Excel. So yes, be nice—but also know your way around a database. 😉</div>',
        unsafe_allow_html=True
    )

elif menu == "📈 Role Explorer":
    st.markdown("<h2 style='color:#ff4da6;'>Explore By Role</h2>", unsafe_allow_html=True)
    role = st.selectbox("Choose a target job role", list(skills_role.keys()))
    core_skills = skills_role.get(role, [])
    core = ", ".join(core_skills)
    st.markdown(f'<div class="insight-card"><b>{role} roles:</b> Most-wanted skills are {core}.</div>', unsafe_allow_html=True)

    # Pie Chart
    role_data = pd.DataFrame({
        "Skill": core_skills,
        "Importance": [100 - i * 20 for i in range(len(core_skills))]
    })
    fig = px.pie(role_data, names="Skill", values="Importance",
                 title=f"Top Skills for {role}",
                 color_discrete_sequence=[PINK, ORANGE, WHITE])
    st.plotly_chart(fig, use_container_width=True)

elif menu == "🎯 Score & Feedback":
    st.markdown("<h2 style='color:#ff4da6;'>Your Score & Advice</h2>", unsafe_allow_html=True)
    myskills = st.text_input("Enter your skills (comma-separated)", "Excel, Python, Communication")
    role = st.selectbox("Target role?", list(skills_role.keys()), key="scorerole")
    pick = set([x.strip().capitalize() for x in myskills.split(",") if x.strip()])
    target = set(skills_role.get(role, []))
    score = int(100 * len(pick & target) / len(target)) if target else 0

    st.progress(score)
    st.metric("Resume Fit Score", f"{score}/100")

    missing = target - pick
    advice = {
        "Python": "Learning Python can launch your Analyst career.",
        "SQL": "SQL is crucial for data roles.",
        "Excel": "Excel is essential everywhere.",
        "Canva": "Canva helps tell visual stories for Marketers.",
        "SEO": "SEO skills boost digital marketing jobs.",
        "Market Research": "Strengthen your market research side.",
        "Recruitment": "HR jobs always value recruitment skills.",
        "Communication": "Communication matters in every field.",
        "Negotiation": "Negotiation sets Sales pros apart.",
        "CRM": "Salesforce/HubSpot experience is valued!"
    }

    if score == 100:
        st.balloons()
        st.markdown('<div class="insight-card" style="border-left:8px solid #65fc65;">🌟 Amazing! You’ve nailed the perfect match. Add a little sparkle and hit submit!</div>', unsafe_allow_html=True)
    elif score >= 60:
        st.snow()
        st.markdown(f'<div class="insight-card">You’re almost there! You might want to brush up on: {", ".join(missing)}</div>', unsafe_allow_html=True)
    else:
        st.markdown("<div class='insight-card' style='border-left:8px solid #ffae42;'>Let’s glow up your skill set. Here’s what to work on:</div>", unsafe_allow_html=True)
        for skill in missing:
            st.markdown(f'<div class="insight-card" style="border-left:7px solid #ffc400;">{advice.get(skill, "Add " + skill.title())}</div>', unsafe_allow_html=True)

elif menu == "ℹ️ About":
    st.markdown("<h2 style='color:#ff4da6;'>About This Project</h2>", unsafe_allow_html=True)
    st.markdown("<div class='insight-card'>This app was lovingly crafted to expose the real hiring truth. It’s stylish, sassy, and straight from the data. No fluff—just facts and fun. Share it, learn from it, and glow up your career. 💖</div>", unsafe_allow_html=True)
