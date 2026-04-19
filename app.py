import streamlit as st
from pdf_utils import extract_text_from_pdf
from analyzer import extract_cv_data, extract_job_requirements, analyze_match, generate_feedback

st.set_page_config(page_title="CV Analyzer", layout="wide")
st.title("CV Analyzer")

col1, col2 = st.columns(2)
with col1:
    cv_file = st.file_uploader("Upload CV/Resume (PDF)", type=["pdf"])
with col2:
    jd_text = st.text_area("Paste Job Description", height=300)

if st.button("Analyze", disabled = not (cv_file and jd_text)):
    with st.spinner("Extracting cv data ..."):
        cv_text = extract_text_from_pdf(cv_file)
        cv_data = extract_cv_data(cv_text)

    with st.spinner("Extracting job requirements ..."):
        job = extract_job_requirements(jd_text)

    with st.spinner("Analyzing match ..."):
        analysis = analyze_match(cv_data, job)

    # show more prominently
    st.metric(label="Overall Match Score", value=f"{analysis.overall_score}/100")
    c1, c2, c3 = st.columns(3)
    c1.metric("Skills", f"{analysis.skills_score}/100")
    c2.metric("Experience", f"{analysis.experience_score}/100")
    c3.metric("Seniority", analysis.seniority_fit)

    st.subheader("Tailored feedback")
    st.write_stream(generate_feedback(cv_data, job, analysis))