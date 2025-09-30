"""
Input validation functions for the Cover Letter Generator.

This module contains all validation logic, making it easy to test and reuse.
"""

from typing import Optional, Tuple
from data_types import ResumeFile, FileType


def validate_inputs(resume_file: Optional[ResumeFile], job_description: str) -> Tuple[bool, Optional[str]]:
    """
    Validate user inputs before processing.
    
    Args:
        resume_file: The uploaded resume file (can be None)
        job_description: The job description text
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if inputs are valid, False otherwise
        - error_message: Error message if invalid, None if valid
        
    Examples:
        >>> validate_inputs(None, "Software Engineer position")
        (False, "❌ Please upload a resume file.")
        
        >>> validate_inputs(file_object, "")
        (False, "❌ Please provide a job description.")
        
        >>> validate_inputs(file_object, "Software Engineer position")
        (True, None)
    """
    if resume_file is None:
        return False, "❌ Please upload a resume file."
    
    if not job_description or not job_description.strip():
        return False, "❌ Please provide a job description."
    
    return True, None


def detect_file_type(file_path: str, user_specified_type: FileType = "auto") -> FileType:
    """
    Detect the file type of an uploaded resume.
    
    Args:
        file_path: Path to the uploaded file
        user_specified_type: Type specified by user ("auto", "pdf", "docx", "text")
        
    Returns:
        Detected file type as string
        
    Examples:
        >>> detect_file_type("resume.pdf", "auto")
        "pdf"
        
        >>> detect_file_type("resume.docx", "auto")
        "docx"
        
        >>> detect_file_type("resume.txt", "auto")
        "text"
    """
    if user_specified_type != "auto":
        return user_specified_type
    
    file_path_lower = file_path.lower()
    
    if file_path_lower.endswith('.pdf'):
        return "pdf"
    elif file_path_lower.endswith(('.docx', '.doc')):
        return "docx"
    else:
        return "text"


def validate_file_size(file_path: str, max_size_mb: int = 2) -> Tuple[bool, Optional[str]]:
    """
    Validate that the uploaded file is not too large.
    
    Args:
        file_path: Path to the file to validate
        max_size_mb: Maximum allowed file size in MB
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    import os
    
    try:
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)
        
        if file_size_mb > max_size_mb:
            return False, f"❌ File too large ({file_size_mb:.1f}MB). Maximum size: {max_size_mb}MB"
        
        return True, None
    except OSError:
        return False, "❌ Could not read file size"
