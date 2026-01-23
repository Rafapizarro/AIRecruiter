import streamlit as st
from src.rag.pipeline import rag_pipeline

st.set_page_config(
    page_title="AIRecruiter",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 AIRecruiter")

st.markdown(
    """
**AIRecruiter** helps you evaluate Rafa’s fit for a role using verified background information.

You can ask questions like:
- *Is Rafa experienced in leading complex projects?*
- *What kind of teams does Rafa perform best in?*
- *Does Rafa have experience with data science and deployment?*
"""
)

mode = st.radio(
    "Select evaluation mode",
    ["Ask a question", "Evaluate job fit"]
)

question = st.text_area(
    "Recruiter question",
    placeholder="Paste a question or a job-related query here…",
    height=120
)

if st.button("Ask"):
    if len(question.strip()) < 5:
        st.warning("Please enter a more specific question.")
    else:
        with st.spinner("Analyzing profile..."):
            result = rag_pipeline(
                        question,
                        mode="job_fit" if mode == "Evaluate job fit" else "qa"
                    )

        st.subheader("Answer")
        st.write(result["answer"])

        # Confidence display
        confidence = result["confidence"]

        st.subheader("Confidence")
        if confidence == "high":
            st.success("High confidence")
        elif confidence == "medium":
            st.warning("Medium confidence")
        elif confidence == "low":
            st.error("Low confidence")
        else:
            st.info("Insufficient information")

        if "fit_score" in result:
            st.subheader("Estimated Fit Score")
            st.metric(
                label="Fit score (0-10)",
                value=f"{result['fit_score']} / 10"
            )

        # Sources
        if result["sources"]:
            with st.expander("Sources used"):
                for src in result["sources"]:
                    st.write(f"- {src}")
