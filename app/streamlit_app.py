import streamlit as st
import requests
import re

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

Select an **evaluation mode** and provide your input below.
"""
)

# -----------------------------
# Helper functions (UX guards)
# -----------------------------

def is_link_only(text: str) -> bool:
    text = text.strip()
    url_pattern = r"https?://\S+"
    urls = re.findall(url_pattern, text)
    return len(urls) == 1 and len(text) < 200

def looks_like_job_description(text: str) -> bool:
    text_lower = text.lower()

    # Strong signal: long, structured input
    if len(text) > 800:
        return True

    # Weak signals (only matter if several are present)
    jd_keywords = [
        "responsibilities",
        "requirements",
        "what you bring",
        "what you’ll do",
        "about the role",
        "we are looking for"
    ]

    keyword_hits = sum(1 for k in jd_keywords if k in text_lower)

    # Require multiple weak signals + some length
    return len(text) > 500 and keyword_hits >= 3

# --- Mode selection ---
mode = st.radio(
    "Evaluation mode",
    ["Ask a question", "Evaluate job fit"]
)

# --- Mode-specific placeholder ---
if mode == "Ask a question":
    placeholder = """Ask anything about Rafa’s professional background, for example:

•  Has Rafa worked in X or a similar environment?
•  How strong is his experience with Y?
•  What kind of teammate would he be in a fast-moving team?
•  Where might he need support or ramp-up time?
"""
else:
    placeholder = """Paste the full text job description here.

AIRecruiter will evaluate Rafa’s fit based on his verified background information,
highlighting strengths, possible gaps, and overall alignment with the role.
"""

question = st.text_area(
    "Your input",
    placeholder=placeholder,
    height=180
)

# --- Action button ---
analyze_clicked = st.button("Analyze")

# --- Spinner container (above fit score) ---
spinner_container = st.container()

# --- Fit score container ---
fit_score_container = st.container()

# -----------------------------
# Main action
# -----------------------------
if analyze_clicked:
    user_input = question.strip()

    # 1. Too short input
    if len(user_input) < 10:
        st.warning("Please enter a more detailed input.")
        st.stop()

    # 2. Link-only input (not supported)
    if is_link_only(user_input):
        st.warning(
            "It looks like you pasted a job description link. "
            "Please paste the full job description text instead — links are not supported."
        )
        st.stop()

    # 3. Job description pasted in QA mode
    if mode == "Ask a question" and looks_like_job_description(user_input):
        st.warning(
            "It looks like you pasted a job description while in **Ask a question** mode.\n\n"
            "To evaluate how well Rafa fits this role, please switch to **Evaluate job fit** mode."
        )
        st.stop()

    # --- Valid input → proceed ---
    payload = {
        "question": user_input,
        "mode": "job_fit" if mode == "Evaluate job fit" else "qa"
    }

    with spinner_container:
        with st.spinner("Analyzing profile..."):
            response = requests.post(API_URL, json=payload)

    if response.status_code != 200:
        st.error(f"Error {response.status_code}")
        st.code(response.text)
        st.stop()

    result = response.json()
    answer_text = result.get("answer", "")

    # Remove fit score lines from the main answer (already shown above)
    answer_text = re.sub(r"Fit score:\s*.*", "", answer_text)
    answer_text = re.sub(r"Fit score reason:\s*.*", "", answer_text)
    answer_text = answer_text.strip()

    # --- Extract fit score from answer text ---
    score_match = re.search(r"Fit score:\s*([0-9]+(?:\.5)?)", answer_text)
    reason_match = re.search(r"Fit score reason:\s*(.+)", answer_text)

    fit_score = score_match.group(1) if score_match else None
    fit_reason = reason_match.group(1) if reason_match else None

    # --- Render Fit score (job-fit mode only) ---
    if mode == "Evaluate job fit" and fit_score:
        with fit_score_container:
            st.markdown("### 🎯 Fit score")
            st.markdown(
                f"<h1 style='text-align: center; margin-bottom: 0;'>{fit_score} / 10</h1>",
                unsafe_allow_html=True
            )
            if fit_reason:
                st.markdown(
                    f"""
                    <p style="
                        text-align: center;
                        font-size: 1.05rem;
                        margin-top: 0.5rem;
                    ">
                        {fit_reason}
                    </p>
                    """,
                    unsafe_allow_html=True
                )

    # --- Main answer ---
    st.subheader("Answer")
    st.write(answer_text if answer_text else "No answer returned.")

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

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
