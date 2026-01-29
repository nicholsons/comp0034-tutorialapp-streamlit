from pathlib import Path

import streamlit as st
from streamlit_plotly_mapbox_events import plotly_mapbox_events

from paralympics.charts import bar_chart, line_chart, scatter_map

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

st.set_page_config(page_title="Paralympics", layout="wide")


# Callback
def clear_other_state():
    """Clear irrelevant widget state whenever the chart choice changes."""
    for key in ["trend_feature", "bar_pills"]:
        st.session_state.pop(key, None)


# Layout
# Header (simple navbar-like container with logo and title)
nav_container = st.container(horizontal=True, horizontal_alignment="center")
with nav_container:
    logo = STATIC_DIR / "colour-logo.webp"
    st.image(logo, width=40)
    st.markdown("**Paralympics research app**")

st.markdown("Use the charts to explore the data and then answer the questions below.")

left_col, right_col = st.columns([1, 3])

with left_col:
    # 1. Choose chart
    st.selectbox(
        "Choose a chart:",
        ["Trends", "Participants by gender", "Paralympics locations"],
        key="chart_choice",
        index=None,
        placeholder="Select chart to view...",
        on_change=clear_other_state
    )

    # 2. Line chart → show second selectbox
    if st.session_state.get("chart_choice") == "Trends":
        st.selectbox(
            "Choose feature:",
            ["Sports", "Events", "Countries", "Participants"],
            key="trend_feature"
        )

    # 4. Bar chart → show pills
    elif st.session_state.get("chart_choice") == "Participants by gender":
        st.pills(
            "Choose the type of Paralympics:",
            ["Winter", "Summer"],
            key="bar_pills",
            selection_mode="multi"
        )

with right_col:
    # 3. Draw a line chart after the feature is selected
    if st.session_state.get("chart_choice") == "Trends" and st.session_state.get("trend_feature"):
        feature = str.lower(st.session_state.trend_feature)
        fig = line_chart(feature)
        st.plotly_chart(fig, width="content")

    # 5. Draw one or more bar charts depending on pill selection
    if st.session_state.get("chart_choice") == "Participants by gender" and st.session_state.get(
            "bar_pills"):
        for pill in st.session_state.bar_pills:
            event_type = str.lower(pill)
            fig = bar_chart(event_type)
            st.plotly_chart(fig, width="content")

    # 6. Map chart displays once chosen
    if st.session_state.get("chart_choice") == "Paralympics locations":
        fig = scatter_map()
        st.plotly_chart(fig, width="content")

# Full-width section
st.divider()

# Questions form
question_container = st.container()
with question_container:
    st.write("Answer the questions using the charts to help you.")
    with st.form("questions"):
        col1, col2 = st.columns(2)
        with col1:
            question_one = st.text_input("Question one?", "")
            question_three = st.text_input("Question three?", "")
            name = st.text_input("Your name", "")
            st.form_submit_button("Submit your answers")
        with col2:
            question_two = st.text_input("Question two?", "")
            question_four = st.text_input("Question four?", "")
