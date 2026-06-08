import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("data/StudentsPerformance.csv")

df = load_data()

# ---------------- TITLE ----------------
st.title("📊 Student Performance Dashboard")
st.markdown("Analyze student performance using interactive charts and filters.")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Gender",
    df["gender"].unique(),
    default=df["gender"].unique()
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

math_range = st.sidebar.slider(
    "Math Score Range",
    int(df["math score"].min()),
    int(df["math score"].max()),
    (
        int(df["math score"].min()),
        int(df["math score"].max())
    )
)

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df["gender"].isin(gender))
    & (df["lunch"].isin(lunch))
    & (df["test preparation course"].isin(prep))
    & (df["math score"].between(math_range[0], math_range[1]))
]

# ---------------- KPI CARDS ----------------
st.subheader("📌 KPI Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", len(filtered_df))
col2.metric("Avg Math", round(filtered_df["math score"].mean(), 2))
col3.metric("Avg Reading", round(filtered_df["reading score"].mean(), 2))
col4.metric("Avg Writing", round(filtered_df["writing score"].mean(), 2))

st.divider()

# ---------------- ROW 1 ----------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Bar Chart")

    fig, ax = plt.subplots()

    sns.barplot(
        data=filtered_df,
        x="gender",
        y="math score",
        estimator="mean",
        ax=ax
    )

    ax.set_title("Average Math Score by Gender")

    st.pyplot(fig)

with c2:
    st.subheader("Pie Chart")

    fig, ax = plt.subplots()

    counts = filtered_df["gender"].value_counts()

    ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%"
    )

    ax.set_title("Gender Distribution")

    st.pyplot(fig)

# ---------------- ROW 2 ----------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Histogram")

    fig, ax = plt.subplots()

    sns.histplot(
        filtered_df["math score"],
        kde=True,
        ax=ax
    )

    st.pyplot(fig)

with c2:
    st.subheader("Count Plot")

    fig, ax = plt.subplots()

    sns.countplot(
        data=filtered_df,
        x="test preparation course",
        ax=ax
    )

    plt.xticks(rotation=15)

    st.pyplot(fig)

# ---------------- ROW 3 ----------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Scatter Plot")

    fig, ax = plt.subplots()

    sns.scatterplot(
        data=filtered_df,
        x="math score",
        y="reading score",
        hue="gender",
        ax=ax
    )

    st.pyplot(fig)

with c2:
    st.subheader("Box Plot")

    fig, ax = plt.subplots()

    sns.boxplot(
        data=filtered_df,
        x="gender",
        y="writing score",
        ax=ax
    )

    st.pyplot(fig)

# ---------------- HEATMAP ----------------
st.subheader("Heatmap")

corr = filtered_df[
    ["math score", "reading score", "writing score"]
].corr()

fig, ax = plt.subplots(figsize=(8,5))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig)

# ---------------- AREA CHART ----------------
st.subheader("Area Chart")

st.area_chart(
    filtered_df[
        ["math score", "reading score", "writing score"]
    ]
)

# ---------------- VIOLIN PLOT ----------------
st.subheader("Violin Plot")

fig, ax = plt.subplots()

sns.violinplot(
    data=filtered_df,
    x="gender",
    y="math score",
    ax=ax
)

st.pyplot(fig)

# ---------------- DATA TABLE ----------------
st.subheader("Dataset Preview")

st.dataframe(filtered_df)
