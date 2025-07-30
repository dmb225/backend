import json
import os

import llama_index.core
import streamlit as st
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
from llama_index.readers.file import PDFReader
from pydantic import BaseModel, Field

llama_index.core.set_global_handler("simple")

st.set_page_config(page_title="Job Application Optimizer")
st.title("🎯 Job Application Optimizer")
st.markdown("Upload your resume and paste a job description to get personalized feedback.")

uploaded_resume = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])
job_description = st.text_area("📝 Paste the job description")
analyze_clicked = st.button("Analyze Resume")


# Define schema for structured extraction
class ExperienceItem(BaseModel):
    company_name: str | None = Field(
        description="The name of the company where the candidate worked"
    )
    job_title: str | None = Field(description="The candidate's job title at the company")
    start_date: str | None = Field(description="The start date of the job")
    end_date: str | None = Field(description="The end date of the job")


class EducationItem(BaseModel):
    degree: str | None = Field(description="The name of the degree or certification")
    institution: str | None = Field(description="The name of the university or school")
    graduation_year: int | None = Field(description="The year the candidate completed their degree")


# Final resume schema
class ResumeData(BaseModel):
    name: str = Field(description="The full name of the candidate")
    email: str = Field(description="The candidate's email address")
    phone: str = Field(description="The candidate's phone number")
    education: list[EducationItem] = Field(description="The candidate's education history")
    experience: list[ExperienceItem] = Field(description="The candidate's work experiences")
    skills: list[str] = Field(description="The candidate's technical or professional skills")


# Initialize the LLM
load_dotenv()
llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"))

# Run on click
if uploaded_resume and job_description and analyze_clicked:
    with st.spinner("Processing resume..."):
        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_resume.getbuffer())

        # Load resume text from PDF
        reader = PDFReader()
        documents = reader.load_data("temp_resume.pdf")
        resume_text = documents[0].text

        # Extract structured data
        sllm = llm.as_structured_llm(ResumeData, strict=False)
        response = sllm.complete(resume_text)
        extracted_data = json.loads(response.text)

        # Build prompt
        prompt = f"""
        You are a resume optimization assistant.

        Here is a job description the candidate is interested in:

        {job_description}

        Here is the candidate's resume in structured form:
        {json.dumps(extracted_data, indent=2)}

        Based on this information, provide helpful, actionable suggestions to improve the resume and tailor it more closely to the job. Focus on relevance, missing keywords, skills alignment, and formatting tips.
        """  # noqa: E501

        # Generate feedback
        feedback = llm.complete(prompt)

        # Display result
        st.subheader("📋 Suggestions to Improve Your Resume")
        st.write(feedback.text)
