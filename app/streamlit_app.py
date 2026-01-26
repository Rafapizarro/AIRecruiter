import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="AIRecruiter",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 AIRecruiter")

st.markdown(
    """
**AIRecruiter** helps evaluate Rafa’s fit using verified background information.

Choose a mode and paste your question or job description.
"""
)

mode = st.radio(
    "Select evaluation mode",
    ["Ask a question", "Evaluate job fit"]
)

question = st.text_area(
    "Your input",
    placeholder="Paste a recruiter question or a job description here…",
    height=160
)

if st.button("Ask"):
    if len(question.strip()) < 10:
        st.warning("Please enter a more detailed input.")
    else:
        payload = {
            "question": question,
            "mode": "job_fit" if mode == "Evaluate job fit" else "qa"
        }

        with st.spinner("Analyzing profile..."):
            response = requests.post(API_URL, json=payload)

        if response.status_code != 200:
            st.error(f"Error {response.status_code}")
            st.code(response.text)

        else:
            result = response.json()

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Confidence")
            st.write(result["confidence"].capitalize())

            if "fit_score" in result:
                st.subheader("Estimated Fit Score")
                st.metric(
                    label="Fit score (0–10)",
                    value=f"{result['fit_score']} / 10"
                )

            if result.get("sources"):
                with st.expander("Sources used"):
                    for src in result["sources"]:
                        st.write(f"- {src}")
