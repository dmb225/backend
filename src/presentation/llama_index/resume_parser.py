"""
Tip: Improve reliability in structured extraction

While using LLMs for structured extraction is powerful, it’s not always reliable.
Here are a few practical ways to improve robustness:
    - Test your schema on multiple resume formats to ensure it works across document variations.
    - Add fallback handling in production environments—for example,
      retrying extraction or prompting the model again if parsing fails.
    - Wrap sllm.complete() in a try/except block to catch and gracefully handle rare parsing errors.
For critical use cases, consider combining LLM-based extraction with traditional NLP techniques
(like regex checks or form validators).
This hybrid approach can significantly improve accuracy and reliability.

"""

import json
import os

import streamlit as st
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
from llama_index.readers.file import PDFReader

# Structured data extraction from resume using LlamaIndex
from pydantic import BaseModel, Field

from src.logging_config import setup_logging


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
    graduation_year: str | None = Field(description="The year the candidate completed their degree")


class ResumeData(BaseModel):
    name: str = Field(description="The full name of the candidate")
    email: str = Field(description="The candidate's email address")
    phone: str = Field(description="The candidate's phone number")
    education: list[EducationItem] = Field(description="The candidate's education history")
    experience: list[ExperienceItem] = Field(description="The candidate's work experiences")
    skills: list[str] = Field(description="The candidate's technical or professional skills")


def main() -> None:
    setup_logging()
    load_dotenv()

    st.title("📄 Resume Structured Data Extraction")

    uploaded_file = st.file_uploader("Upload your resume PDF", type="pdf")

    if uploaded_file:
        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        pdf_reader = PDFReader()
        documents = pdf_reader.load_data("temp_resume.pdf")
        text = documents[0].text

        llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"))

        sllm = llm.as_structured_llm(ResumeData, strict=False)
        response = sllm.complete(text)

        resume_json = json.loads(response.text)
        st.json(resume_json)


if __name__ == "__main__":
    main()
