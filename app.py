import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Resume vs Reality", page_icon="🎯", layout="wide")

# --- Styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', sans-serif;
    }
    .big-title {
        color: #5a189a;
        font-size: 2.5em;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.2em;
    }
    .tagline {
        color: #9d4edd;
        font-size: 1.2em;
        text-align: center;
        margin-bottom: 1.5em;
    }
    .box {
        background-color: white;
        border-left: 6px solid #9d4edd;
        padding: 1.2em;
        margin-bottom: 1em;
        border-radius: 10px;
        box-shadow: 0px 3px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- Data (can be replaced with real CSVs) ---
def load_data():
    return pd.DataFrame({
        "Skill": ["Excel", "SQL", "Python", "Communication", "Teamwork", "Power BI", "Market Research"],
        "Category": ["Tool", "Tool", "Tool", "Soft Skill", "Soft Skill", "Tool", "Domain Knowledge"],
        "Job Ads": [92, 76, 68, 45, 41, 32, 29],
        "Resumes": [88, 49, 37, 93, 88, 27, 30],
        "Hires": [64, 54, 55, 37, 31, 18, 15]
    })

df = load_data()

# --- Title and Intro ---
st.markdown("<div class='big-title'>🎯 Resume vs Reality</div>", unsafe_allow_html=True)
st.markdown("<div class='tagline'>✨ Discover which skills are just buzzwords—and which truly get you hired</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='box'>Ever wonder if the skills you're adding to your resume actually matter to recruiters? This tool helps you compare what's written on resumes, what companies ask for in job ads, and what hired candidates actually have. ✍️</div>",
    unsafe_allow_html=True)

# --- Filters ---
cols = st.columns(3)
with cols[0]:
    category_filter = st.selectbox("🔍 Filter by Skill Type", ["All"] + sorted(df["Category"].unique()))
with cols[1]:
    top_n = st.slider("🎯 Top N Skills to Show", 3, len(df), 7)
with cols[2]:
    metric_choice = st.selectbox("📊 Sort By", ["Job Ads", "Resumes", "Hires"])

# --- Filter Logic ---
if category_filter != "All":
    df_filtered = df[df["Category"] == category_filter]
else:
    df_filtered = df.copy()

df_top = df_filtered.sort_values(by=metric_choice, ascending=False).head(top_n)

# --- Plot ---
st.subheader("📈 Skill Frequency Across Sources")
fig = px.bar(df_top, x="Skill", y=["Job Ads", "Resumes", "Hires"],
             barmode="group",
             color_discrete_sequence=["#9d4edd", "#f72585", "#3a86ff"])
fig.update_layout(xaxis_title=None, yaxis_title="Frequency")
st.plotly_chart(fig, use_container_width=True)

# --- Advanced Insight ---
st.subheader("📉 Predictability & Real Value")
df["Resume Inflation"] = (df["Resumes"] + 1) / (df["Job Ads"] + 1)
df["Hiring Edge"] = (df["Hires"] + 1) / (df["Resumes"] + 1)

fig2 = px.scatter(df, x="Resume Inflation", y="Hiring Edge", text="Skill",
                  color="Category", size="Hires", hover_data=["Job Ads", "Resumes"],
                  title="🧠 Skill Positioning Matrix")
fig2.update_traces(textposition="top center")
fig2.update_layout(height=550)
st.plotly_chart(fig2, use_container_width=True)

# --- Skill-by-Skill Insight ---
st.subheader("🔍 Deep Dive: Select Skills to Explore")
selected_skills = st.multiselect("Pick skills to explore:", df["Skill"].tolist(), default=["Python", "Communication"])

if selected_skills:
    insight_df = df[df["Skill"].isin(selected_skills)].copy()
    insight_df["Inflation"] = (insight_df["Resumes"] + 1) / (insight_df["Job Ads"] + 1)
    insight_df["Edge"] = (insight_df["Hires"] + 1) / (insight_df["Resumes"] + 1)
    
    st.write(insight_df[["Skill", "Job Ads", "Resumes", "Hires", "Inflation", "Edge"]].reset_index(drop=True))

    for _, row in insight_df.iterrows():
        st.markdown(f"<div class='box'><b>{row['Skill']}</b>: <br>📌 <i>Appears {row['Resumes']} times in resumes</i>, <br>📋 <i>{row['Job Ads']} times in job ads</i>, <br>🎯 <i>Actually helped {row['Hires']} people get hired</i>.<br><br>🧠 Resume Inflation: <b>{row['Inflation']:.2f}</b><br>🌟 Hiring Edge: <b>{row['Edge']:.2f}</b></div>", unsafe_allow_html=True)

# --- Closing Note ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#5a189a;'>Built with ❤️ by Manju Singh | MBA | Data & Insight Enthusiast</p>",
    unsafe_allow_html=True
)
