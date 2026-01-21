import streamlit as st

st.set_page_config(page_title="Paralympics", layout="wide")

# Two columns. Use [1,1] for equal widths or e.g. [1,3] for 1:3
left_col, right_col = st.columns([1, 3])

with left_col:
    select_chart = st.selectbox("Choose a chart:",
                                ("Trends in number of sports, events, counties, participants",
                                 "Participants by gender",
                                 "Paralympics locations"),
                                index=None,
                                placeholder="Select chart to view...")

    # Conditional rendering based on the option chosen in select_chart
    if select_chart == "Trends in number of sports, events, countries, participants":
        select_trend_type = st.selectbox("Choose the feature to display:",
                                         ["Sports", "Events", "Countries", "Participants"])
    elif select_chart == "Participants by gender":
        options = ["Winter", "Summer"]
        selection = st.pills("Choose the type of Paralympics:",
                             options,
                             selection_mode="multi")

    with right_col:
        st.subheader("Charts")

# Full-width
st.divider()

question_container = st.container()

with question_container:
    st.write("Answer the questions using the charts to help you.")
    with st.form("questions"):
        col1, col2 = st.columns(2)
        with col1:
            question_one = st.text_input("Question one?", "Enter your answer here")
            question_three = st.text_input("Question three?", "Enter your answer here")
            name = st.text_input("Your name", "Enter your name here")
            st.form_submit_button("Submit your answers")
        with col2:
            question_two = st.text_input("Question two?", "Enter your answer here")
            question_four = st.text_input("Question four?", "Enter your answer here")
