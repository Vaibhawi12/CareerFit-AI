import streamlit as st 
import fitz 
import google.generativeai as genai 
import re

genai.configure(api_key=st.secrets["GCP_API_KEY"])

def extract_text_from_pdf(uploaded_file):
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc :
        text += page.get_text()
    return text

def analyze_resume(resume_text, job_description):
    prompt = f"""
    You are an AI-powered Resume and Job Description Analyzer. Your task is to perform the following:

    1. **Skill Extraction & Matching**
    - Extract relevant skills, tools, technologies, and keywords from both the resume and job description.
    - Identify matching skills and missing skills (gap analysis).

    2. **ATS-Optimized Resume Rewrite**
    - Rewrite the resume content to be more ATS-friendly.
    - Naturally insert missing skills from the job description into appropriate sections without keyword stuffing.
    - Maintain a professional and concise tone.

    3. **Interview Question Generation**
    - Generate 8–10 potential interview questions based on the job description, focusing on required skills, experience, and industry knowledge.

    4. **Match Score**
    - Based on semantic similarity between the resume and job description, calculate a match score out of 100.
    - Briefly explain why you assigned that score.

    **Format your output as follows:**
    ### 1. Extracted Skills from Resume
    [List of skills]

    ### 2. Extracted Skills from Job Description
    [List of skills]

    ### 3. Matching Skills
    [List of skills]

    ### 4. Missing Skills (Gap Analysis)
    [List of skills]

    ### 5. ATS-Optimized Resume Rewrite
    [Rewritten resume text]

    ### 6. Suggested Interview Questions
    [List of 8–10 questions]

    ### 7. Match Score
    Score: XX/100
    Reasoning: [Brief explanation]
    
    resume:
    {resume_text}
    job description
    {job_description}
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def highlight_skills(section_title, skills_list, color):
    st.markdown(f"#### {section_title}")
    for skill in skills_list:
        st.markdown(f"<span style='color:{color}; font-weight:bold;'>{skill}</span>", unsafe_allow_html=True)
    
st.set_page_config(page_title="CareerFit AI", page_icon="🤖" , layout="centered")

with open(".streamlit/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 class='title-gradient'>CareerFit AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Resume Optimizer & Job Match Assistant</p>", unsafe_allow_html=True)

uploaded_resume = st.file_uploader("Upload Your Resume PDF File", type=["pdf"])
job_desc = st.text_area("Paste Job Description Here")

if st.button("Analyze Resume"):
    if uploaded_resume and job_desc.strip():
        with st.spinner("Analyzing resume... Grab A coffee!"):
            resume_text = extract_text_from_pdf(uploaded_resume)
            analysis = analyze_resume(resume_text, job_desc)
            
        sections = re.split(r"### ", analysis)
        for section in sections:
            if section.strip():
                st.markdown(f"### {section}", unsafe_allow_html=True)    
        
    else:
        st.error(" Please upload valid resume file and job description.")
        
