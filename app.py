import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Unemployment Analysis in India",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df1 = pd.read_csv("Unemployment_in_India.csv")
df2 = pd.read_csv("Unemployment_Rate_upto_11_2020.csv")

# Remove extra spaces from column names
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Convert dates
df1["Date"] = pd.to_datetime(df1["Date"], errors="coerce")
df2["Date"] = pd.to_datetime(df2["Date"], errors="coerce")

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📊 Unemployment Analysis in India")

st.markdown("""
### Overview

This dashboard analyzes unemployment data in India using Python,
Pandas, Matplotlib, Seaborn and Streamlit.

The analysis focuses on:

- Unemployment trends over time
- Rural vs Urban unemployment
- State-wise unemployment
- COVID-19 period
- Employment and labour participation
- Correlation between employment indicators
""")

st.divider()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("📌 Dashboard Menu")

page = st.sidebar.radio(
    "Select Analysis",
    [
        "Overview",
        "Unemployment Trend",
        "Rural vs Urban",
        "State-wise Analysis",
        "COVID-19 Analysis",
        "Correlation Analysis"
    ]
)

# ---------------------------------------------------
# OVERVIEW
# ---------------------------------------------------

if page == "Overview":

    st.header("📌 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Dataset 1 Rows",
            df1.shape[0]
        )

    with col2:
        st.metric(
            "Dataset 1 Columns",
            df1.shape[1]
        )

    with col3:
        st.metric(
            "Dataset 2 Rows",
            df2.shape[0]
        )

    with col4:
        st.metric(
            "Dataset 2 Columns",
            df2.shape[1]
        )

    st.subheader("Dataset 1")

    st.dataframe(
        df1.head(10),
        use_container_width=True
    )

    st.subheader("Dataset 2")

    st.dataframe(
        df2.head(10),
        use_container_width=True
    )

    st.subheader("Missing Values")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Dataset 1")
        st.dataframe(
            df1.isnull().sum()
        )

    with col2:
        st.write("Dataset 2")
        st.dataframe(
            df2.isnull().sum()
        )

# ---------------------------------------------------
# UNEMPLOYMENT TREND
# ---------------------------------------------------

elif page == "Unemployment Trend":

    st.header("📈 Unemployment Trend Over Time")

    monthly_unemployment = (
        df1.groupby("Date")[
            "Estimated Unemployment Rate (%)"
        ]
        .mean()
        .sort_index()
    )

    st.line_chart(
        monthly_unemployment
    )

    st.subheader("Average Unemployment Rate")

    average_rate = df1[
        "Estimated Unemployment Rate (%)"
    ].mean()

    st.metric(
        "Average Unemployment Rate",
        f"{average_rate:.2f}%"
    )

    st.markdown("""
    **Observation:** The unemployment rate remained relatively stable
    during much of 2019 and early 2020, followed by a sharp increase
    during the COVID-19 period.
    """)

# ---------------------------------------------------
# RURAL VS URBAN
# ---------------------------------------------------

elif page == "Rural vs Urban":

    st.header("🏙️ Rural vs Urban Unemployment")

    rural_urban = (
        df1.groupby("Area")[
            "Estimated Unemployment Rate (%)"
        ]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(rural_urban)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Rural Average",
            f"{rural_urban.get('Rural', 0):.2f}%"
        )

    with col2:
        st.metric(
            "Urban Average",
            f"{rural_urban.get('Urban', 0):.2f}%"
        )

    st.markdown("""
    **Observation:** The dataset shows a higher average unemployment
    rate in urban areas than rural areas during the period analyzed.
    """)

# ---------------------------------------------------
# STATE-WISE ANALYSIS
# ---------------------------------------------------

elif page == "State-wise Analysis":

    st.header("🗺️ State-wise Unemployment Analysis")

    state_unemployment = (
        df2.groupby("Region")[
            "Estimated Unemployment Rate (%)"
        ]
        .mean()
        .sort_values(ascending=False)
    )

    # Number of states to display
    number_of_states = st.slider(
        "Number of states to display",
        min_value=5,
        max_value=len(state_unemployment),
        value=min(15, len(state_unemployment))
    )

    selected_states = state_unemployment.head(
        number_of_states
    )

    st.bar_chart(selected_states)

    st.subheader("State-wise Values")

    st.dataframe(
        selected_states.reset_index(
            name="Average Unemployment Rate (%)"
        ),
        use_container_width=True
    )

    st.markdown("""
    **Observation:** Unemployment rates vary considerably across the
    states represented in the dataset.
    """)

# ---------------------------------------------------
# COVID-19 ANALYSIS
# ---------------------------------------------------

elif page == "COVID-19 Analysis":

    st.header("🦠 COVID-19 and Unemployment")

    covid_data = df2[
        (df2["Date"].dt.year == 2020)
    ]

    covid_monthly = (
        covid_data.groupby("Date")[
            "Estimated Unemployment Rate (%)"
        ]
        .mean()
        .sort_index()
    )

    st.line_chart(
        covid_monthly
    )

    if len(covid_monthly) > 0:

        highest_date = covid_monthly.idxmax()
        highest_rate = covid_monthly.max()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Highest Recorded Rate",
                f"{highest_rate:.2f}%"
            )

        with col2:
            st.metric(
                "Peak Date",
                highest_date.strftime("%B %Y")
            )

    st.markdown("""
    **Observation:** The unemployment rate increased sharply during
    May and June 2020 and then declined substantially during the
    following months.

    The dataset shows a major change in unemployment during this period,
    although the analysis alone cannot establish COVID-19 as the sole
    cause of the change.
    """)

# ---------------------------------------------------
# CORRELATION ANALYSIS
# ---------------------------------------------------

elif page == "Correlation Analysis":

    st.header("🔗 Employment Indicators Correlation")

    correlation = df2[
        [
            "Estimated Unemployment Rate (%)",
            "Estimated Employed",
            "Estimated Labour Participation Rate (%)"
        ]
    ].corr()

    # Display correlation table
    st.subheader("Correlation Matrix")

    st.dataframe(
        correlation.style.format("{:.2f}"),
        use_container_width=True
    )

    # Heatmap
    fig, ax = plt.subplots(figsize=(8, 5))

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        ax=ax
    )

    ax.set_title(
        "Correlation Between Employment Indicators"
    )

    st.pyplot(fig)

    st.subheader("Key Relationships")

    unemployment_employment = correlation.loc[
        "Estimated Unemployment Rate (%)",
        "Estimated Employed"
    ]

    unemployment_participation = correlation.loc[
        "Estimated Unemployment Rate (%)",
        "Estimated Labour Participation Rate (%)"
    ]

    st.write(
        f"**Unemployment vs Employment:** "
        f"{unemployment_employment:.2f}"
    )

    st.write(
        f"**Unemployment vs Labour Participation:** "
        f"{unemployment_participation:.2f}"
    )

    st.markdown("""
    **Interpretation:** The correlation between unemployment and
    estimated employment is weakly negative, while the correlation
    between unemployment and labour participation is very weakly
    negative.

    Correlation measures association and does not establish causation.
    """)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "Unemployment Analysis in India | Python & Streamlit Project"
)