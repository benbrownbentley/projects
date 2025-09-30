"""
UI components and styling for the Cover Letter Generator.

This module contains all Gradio UI components and styling, keeping the main app clean.
"""

import gradio as gr
from typing import Tuple, Any


def create_file_upload_section() -> Tuple[gr.File, gr.Dropdown]:
    """
    Create the file upload section with resume upload and file type selection.
    
    Returns:
        Tuple of (resume_file_input, file_type_dropdown)
    """
    with gr.Column():
        gr.Markdown("### 📄 Upload Resume")
        
        resume_file = gr.File(
            label="Upload your resume",
            file_types=[".pdf", ".docx", ".doc", ".txt"],
            file_count="single"
        )
        
        file_type = gr.Dropdown(
            choices=["auto", "pdf", "docx", "text"],
            value="auto",
            label="File type (auto-detect recommended)"
        )
        
        return resume_file, file_type


def create_job_description_section() -> gr.Textbox:
    """
    Create the job description input section.
    
    Returns:
        Job description textbox
    """
    gr.Markdown("### 📋 Job Description")
    
    job_description = gr.Textbox(
        label="Paste the job description here",
        placeholder="Copy and paste the complete job description...",
        lines=12,
        max_lines=20
    )
    
    return job_description


def create_generate_button() -> gr.Button:
    """
    Create the generate button.
    
    Returns:
        Generate button
    """
    return gr.Button(
        "🚀 Generate Cover Letter",
        variant="primary",
        size="lg"
    )


def create_output_section() -> Tuple[gr.Markdown, gr.Markdown]:
    """
    Create the output section with loading status and cover letter display.
    
    Returns:
        Tuple of (loading_status, cover_letter_output)
    """
    with gr.Column():
        gr.Markdown("### ✍️ Generated Cover Letter")
        
        # Loading status (initially hidden)
        loading_status = gr.Markdown(
            value="",
            visible=False,
            elem_classes=["loading-status"]
        )
        
        # Cover letter output
        cover_letter_output = gr.Textbox(
            label="Cover Letter",
            elem_classes=["cover-letter-output"],
            show_copy_button=True,
            value="Upload your resume and paste a job description to get started.",
            lines=20,
            max_lines=30,
            interactive=False
        )
        
        return loading_status, cover_letter_output


def create_examples_section() -> None:
    """Create the examples section with sample job descriptions."""
    with gr.Accordion("💡 Example Job Descriptions (click to copy)", open=False):
        gr.Markdown("""
        **Software Engineer Example:**
        ```
        Software Engineer - We are seeking a talented Software Engineer to join our team. 
        Requirements: 3+ years Python experience, React, AWS, Docker. 
        Responsibilities: Develop web applications, collaborate with team, maintain code quality.
        ```
        
        **Marketing Manager Example:**
        ```
        Marketing Manager - Looking for a creative Marketing Manager with 5+ years experience 
        in digital marketing, SEO, content creation, and social media management. 
        Must have strong analytical skills.
        ```
        """)


def create_footer() -> None:
    """Create the application footer."""
    gr.Markdown("""
    ---
    **💡 Tips for best results:**
    - Upload a complete, well-formatted resume
    - Include the full job description with requirements and responsibilities
    - The AI will automatically match your skills to job requirements
    - Generated cover letters are formatted in markdown for easy editing
    """)
    
    # Footer with attribution
    gr.Markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em; margin-top: 20px;'>
    AI Cover Letter Generator | Built with ❤️ using Gradio & OpenAI
    </div>
    """)


def get_css_styles() -> str:
    """
    Get the CSS styles for the application.
    
    Returns:
        CSS string for styling
    """
    return """
    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
    }
    .cover-letter-output {
        font-family: 'Georgia', serif !important;
        line-height: 1.6 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: pre-wrap !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
        word-break: break-word !important;
        resize: vertical !important;
    }
    .cover-letter-output textarea {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        word-break: break-word !important;
        white-space: pre-wrap !important;
        overflow-x: hidden !important;
        max-width: 100% !important;
        resize: vertical !important;
    }
    .loading-status {
        background-color: #f8f9fa !important;
        border: 2px solid #007bff !important;
        border-radius: 10px !important;
        margin: 10px 0 !important;
        animation: pulse 2s infinite !important;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    """



