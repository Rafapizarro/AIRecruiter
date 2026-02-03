import streamlit as st
import requests

API_URL = "https://ai-recruiter-api-301926925569.europe-west1.run.app/ask"

st.set_page_config(
    page_title="AIRecruiter",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 AIRecruiter")

st.markdown(
    """
**AIRecruiter** evaluates Rafa’s professional profile using verified background information.

Select an evaluation mode and provide your input below.
"""
)

# --- Mode selection ---
mode = st.radio(
    "Select evaluation mode",
    ["Ask a question", "Evaluate job fit"]
)

# --- Mode-specific placeholder ---
if mode == "Ask a question":
    placeholder = """Ask anything about Rafa’s professional background, for example:
• Has Rafa worked in X or a similar environment?
• How strong is his experience with Y?
• What kind of teammate would he be in a fast-moving team?
• Where might he need support or ramp-up time?
"""
else:
    placeholder = """Paste the full job description here.

AIRecruiter will evaluate Rafa’s fit based on verified background information,
highlighting strengths, gaps, and overall alignment with the role.
"""

question = st.text_area(
    "Your input",
    placeholder=placeholder,
    height=180
)

# --- Action button ---
if st.button("Analyze"):
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

            # --- Main answer ---
            st.subheader("Answer")
            st.write(result.get("answer", "No answer returned."))

            # --- Confidence ---
            st.subheader("Level of confidence in this answer")
            st.write(result.get("confidence", "unknown").capitalize())

            with st.expander("What does this confidence level mean?"):
                st.markdown(
                    """
- **High**: Strong, consistent evidence across multiple parts of Rafa’s background.
- **Medium**: Relevant experience exists, but with some assumptions or gaps.
- **Low**: Limited direct evidence; conclusions are more inferential.
- **Very low**: The available information does not strongly support a reliable answer.
"""
                )

            # --- Fit score (job-fit mode only) ---
            if mode == "Evaluate job fit":
                if "fit_score" in result:
                    st.markdown("## 🎯 Fit score")
                    st.markdown(
                        f"<h1 style='text-align: center;'>{result['fit_score']} / 10</h1>",
                        unsafe_allow_html=True
                    )

                    if "fit_score_reason" in result:
                        st.caption(result["fit_score_reason"])
                else:
                    st.info("A numerical fit score could not be reliably estimated for this role.")
