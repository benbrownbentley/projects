"""
Type definitions for the Cover Letter Generator application.

This module contains all type hints and data structures used throughout the application.
This makes the code more readable and helps with IDE support and learning.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass


@dataclass
class ResumeData:
    """Structured resume data extracted from uploaded files."""
    name: str
    email: str
    phone: str
    location: str
    summary: str
    skills: List[str]
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    certifications: List[str]
    achievements: List[str]


@dataclass
class JobData:
    """Structured job description data extracted from text."""
    company_name: str
    job_title: str
    required_skills: List[str]
    preferred_skills: List[str]
    experience_requirements: str
    education_requirements: str
    key_responsibilities: List[str]
    company_culture: str
    benefits: List[str]
    location: str
    employment_type: str


@dataclass
class ProcessingResult:
    """Result of cover letter generation process."""
    success: bool
    content: Optional[str] = None
    error_message: Optional[str] = None


# Type aliases for better readability
FileType = str  # "pdf", "docx", or "text"
ProgressCallback = Any  # Gradio Progress object
ResumeFile = Any  # Gradio File object

