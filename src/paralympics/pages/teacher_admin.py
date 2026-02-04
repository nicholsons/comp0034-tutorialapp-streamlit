import requests
import streamlit as st

from paralympics.paralympics_dashboard import API_BASE

st.set_page_config(page_title="Teacher Admin", layout="wide")


def process_form() -> None:
    """ Process the form when the user presses submit button.

    Called when the user presses Submit.
    Reads all values from st.session_state, validates them,
    and sends them to the REST API if valid.
    """
    # Extract the values from the session_state as JSON, JSON attributes match the database
    # column name
    question = {"question_text": st.session_state.question_text}
    responses = [
        {"response_text": st.session_state.response_text_1,
         "is_correct": st.session_state.is_correct_1},
        {"response_text": st.session_state.response_text_2,
         "is_correct": st.session_state.is_correct_2},
        {"response_text": st.session_state.response_text_3,
         "is_correct": st.session_state.is_correct_3},
        {"response_text": st.session_state.response_text_4,
         "is_correct": st.session_state.is_correct_4},
    ]

    # Validation
    errors = []

    if not question["question_text"] or not question["question_text"].strip():
        errors.append("Question text is required.")

    for idx, r in enumerate(responses, start=1):
        if not r["response_text"] or not r["response_text"].strip():
            errors.append(f"Option {idx} must have text.")

    correct_count = sum(1 for r in responses if r["is_correct"])
    if correct_count == 0:
        errors.append("Please select exactly one correct response (none selected).")
    elif correct_count > 1:
        errors.append("Please select exactly one correct response (multiple selected).")

    # Render validation errors
    if errors:
        for e in errors:
            st.error(e)
        return

    # Send to the API using the JSON data
    payload = question
    try:
        response = requests.post(f"{API_BASE}/question", json=payload)
        response.raise_for_status()

        # Get the id of the newly saved question from the response
        question_id = response.json()["id"]

        for idx, r in enumerate(responses, start=1):
            r["question_id"] = question_id
            resp = requests.post(f"{API_BASE}/response", json=r)
            resp.raise_for_status()
        st.success("Question saved successfully.")

        # Clear the caches as the data has now been updated
        # You can clear a function's cache with func.clear() or clear the entire cache with st.cache_data.clear().
        st.cache_data.clear()

    except Exception as exc:
        st.error(f"Error saving question: {exc}")


# Form UI
with st.form("question_form"):
    st.header("Create Question")

    # Create input for the question text
    st.text_input("Enter the question", key="question_text")

    st.write("Enter the multiple choice options and mark the correct answer.")

    # Create inputs for the 4 options
    for i in range(1, 5):
        col_text, col_check = st.columns([4, 1])
        col_text.text_input("Text for option", key=f"response_text_{i}")
        col_check.checkbox("Correct?", key=f"is_correct_{i}")

    # Create submit button — calls the process_form() function on submit
    st.form_submit_button("Save Question", on_click=process_form)
