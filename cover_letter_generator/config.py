# Configuration settings for the Cover Letter Generator

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found! Please check your .env file.\n"
        "Make sure you have a .env file in the same directory with:\n"
        "OPENAI_API_KEY=your_api_key_here"
    )

MODEL = "gpt-4o-mini"

# System Messages
SYSTEM_MESSAGE = """You are an expert career counselor and professional writer specializing in creating compelling, personalized cover letters. 

Your role is to:
1. Analyze resumes to extract key skills, experiences, and achievements
2. Analyze job descriptions to identify requirements and company culture
3. Create tailored cover letters that bridge the gap between candidate and position
4. Use professional, engaging language that demonstrates value proposition
5. Structure cover letters with proper formatting in markdown

Always maintain a professional tone while being authentic and specific to the candidate's background and the job requirements."""

RESUME_ANALYSIS_PROMPT = """You are a resume analysis expert. Extract information and return only valid JSON."""

JOB_ANALYSIS_PROMPT = """You are a job market analyst. Extract information and return only valid JSON."""

# Resume Structure Template
RESUME_TEMPLATE = {
    "name": "Full name",
    "email": "Email address",
    "phone": "Phone number",
    "location": "City, State/Country",
    "summary": "Professional summary or objective",
    "skills": ["skill1", "skill2", "skill3"],
    "experience": [
        {
            "title": "Job title",
            "company": "Company name",
            "duration": "Start date - End date",
            "description": "Key responsibilities and achievements"
        }
    ],
    "education": [
        {
            "degree": "Degree name",
            "institution": "School/University name",
            "year": "Graduation year"
        }
    ],
    "certifications": ["cert1", "cert2"],
    "achievements": ["achievement1", "achievement2"]
}

# Job Analysis Template
JOB_TEMPLATE = {
    "company_name": "Company name",
    "job_title": "Job title",
    "required_skills": ["skill1", "skill2", "skill3"],
    "preferred_skills": ["skill1", "skill2"],
    "experience_requirements": "Years of experience and level",
    "education_requirements": "Education level required",
    "key_responsibilities": ["responsibility1", "responsibility2"],
    "company_culture": "Company values and culture indicators",
    "benefits": ["benefit1", "benefit2"],
    "location": "Job location",
    "employment_type": "Full-time, Part-time, etc."
}

# Fallback Data Structures
FALLBACK_RESUME_DATA = {
    "name": "Unknown",
    "email": "unknown@email.com",
    "phone": "Unknown",
    "location": "Unknown",
    "summary": "Professional with relevant experience",
    "skills": ["Various skills"],
    "experience": [{"title": "Professional", "company": "Various", "duration": "Recent", "description": "Relevant experience"}],
    "education": [{"degree": "Relevant Degree", "institution": "University", "year": "Recent"}],
    "certifications": [],
    "achievements": []
}

FALLBACK_JOB_DATA = {
    "company_name": "Target Company",
    "job_title": "Position",
    "required_skills": ["Relevant skills"],
    "preferred_skills": [],
    "experience_requirements": "Relevant experience",
    "education_requirements": "Relevant education",
    "key_responsibilities": ["Key responsibilities"],
    "company_culture": "Professional environment",
    "benefits": [],
    "location": "Location",
    "employment_type": "Full-time"
}
