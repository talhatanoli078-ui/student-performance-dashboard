import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.metric-container {
    background: linear-gradient(135deg,#4F46E5,#06B6D4);
    padding:15px;
    border-radius:15px;
    text-align:center;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    pd.read_csv("studentsperformance.csv")

df = load_data()

# ---------------- FEATURE ENGINEERING ----------------
df["average_score"] = (
    df["math score"] +
    df["reading score"] +
    df["writing score"]
) / 3

df["performance"] = pd.cut(
    df["average_score"],
    bins=[0, 60, 80, 100],
    labels=["Poor", "Good", "Excellent"]
)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center'>
🎓 Student Performance Analytics Dashboard
</h1>
<p style='text-align:center'>
Interactive Educational Analytics Platform
</p>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 Filters")

gender = st.sidebar.multiselect(
    "Gender",
    df["gender"].unique(),
    default=df["gender"].unique()
)

race = st.sidebar.multiselect(
    "Race / Ethnicity",
    df["race/ethnicity"].unique(),
    default=df["race/ethnicity"].unique()
)

lunch = st.sidebar.multiselect(
    "Lunch Type",
    df["lunch"].unique(),
    default=df["lunch"].unique()
)

prep = st.sidebar.multiselect(
    "Test Preparation",
    df["test preparation course"].unique(),
    default=df["test preparation course"].unique()
)

parent = st.sidebar.multiselect(
    "Parental Education",
    df["parental level of education"].unique(),
    default=df["parental level of education"].unique()
)

score_range = st.sidebar.slider(
    "Average Score Range",
    0,
    100,
    (0, 100)
)

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df["gender"].isin(gender)) &
    (df["race/ethnicity"].isin(race)) &
    (df["lunch"].isin(lunch)) &
    (df["test preparation course"].isin(prep)) &
    (df["parental level of education"].isin(parent)) &
    (df["average_score"].between(score_range[0], score_range[1]))
]

# ---------------- KPI CARDS ----------------
st.subheader("📊 KPI Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Students", len(filtered_df))
c2.metric("Math Avg", round(filtered_df["math score"].mean(), 1))
c3.metric("Reading Avg", round(filtered_df["reading score"].mean(), 1))
c4.metric("Writing Avg", round(filtered_df["writing score"].mean(), 1))

st.divider()

# ---------------- CHARTS ROW 1 ----------------
col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        filtered_df,
        x="gender",
        y="math score",
        color="gender",
        title="Average Math Score by Gender"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(
        filtered_df,
        names="gender",
        title="Gender Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- CHARTS ROW 2 ----------------
col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(
        filtered_df,
        x="average_score",
        color="performance",
        nbins=20,
        title="Performance Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.scatter(
        filtered_df,
        x="math score",
        y="reading score",
        color="performance",
        size="writing score",
        hover_data=["gender"],
        title="Math vs Reading"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- HEATMAP ----------------
st.subheader("🔥 Correlation Heatmap")

corr = filtered_df[
    ["math score", "reading score", "writing score"]
].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- RADAR CHART ----------------
st.subheader("🎯 Performance Radar")

avg_math = filtered_df["math score"].mean()
avg_read = filtered_df["reading score"].mean()
avg_write = filtered_df["writing score"].mean()

radar = go.Figure()

radar.add_trace(go.Scatterpolar(
    r=[avg_math, avg_read, avg_write],
    theta=["Math", "Reading", "Writing"],
    fill='toself'
))

radar.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=False
)

st.plotly_chart(radar, use_container_width=True)

# ---------------- TREEMAP ----------------
st.subheader("🌳 Treemap")

fig = px.treemap(
    filtered_df,
    path=["gender", "performance"],
    values="average_score"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- SUNBURST ----------------
st.subheader("☀️ Sunburst Analysis")

fig = px.sunburst(
    filtered_df,
    path=[
        "gender",
        "lunch",
        "test preparation course"
    ]
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- TOP STUDENTS ----------------
st.subheader("🏆 Top 10 Students")

top_students = filtered_df.sort_values(
    "average_score",
    ascending=False
).head(10)

st.dataframe(top_students, use_container_width=True)

# ---------------- AI INSIGHTS ----------------
st.subheader("🤖 AI Insights")

best_subject = max(
    {
        "Math": filtered_df["math score"].mean(),
        "Reading": filtered_df["reading score"].mean(),
        "Writing": filtered_df["writing score"].mean()
    },
    key=lambda x: {
        "Math": filtered_df["math score"].mean(),
        "Reading": filtered_df["reading score"].mean(),
        "Writing": filtered_df["writing score"].mean()
    }[x]
)

st.success(
    f"Students perform best in {best_subject}. "
    f"Average overall score is "
    f"{round(filtered_df['average_score'].mean(),2)}."
)

# ---------------- DATA PREVIEW ----------------
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df, use_container_width=True)

# ---------------- DOWNLOAD ----------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "student_performance.csv",
    "text/csv"
)
