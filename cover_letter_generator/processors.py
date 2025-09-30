"""
Core processing logic for the Cover Letter Generator.

This module contains the main business logic, separated from UI concerns.
"""

from typing import Tuple, Optional
import gradio as gr

from data_types import ResumeFile, FileType, ProcessingResult
from validators import validate_inputs, detect_file_type, validate_file_size
from cover_letter_generator import CoverLetterGenerator


class CoverLetterProcessor:
    """
    Main processor for cover letter generation.
    
    This class handles the complete workflow from input validation to output generation.
    """
    
    def __init__(self):
        """Initialize the processor with a cover letter generator."""
        self.generator = CoverLetterGenerator()
    
    def show_loading_status(self) -> Tuple[gr.update, gr.update]:
        """
        Show the loading status in the UI and clear the cover letter output.
        
        Returns:
            Tuple of (loading_status_update, cover_letter_clear_update)
        """
        loading_update = gr.update(
            visible=True, 
            value="<div style='text-align: center; padding: 20px; font-size: 18px; color: #007bff;'>🔍 Analyzing - this may take a few minutes...</div>"
        )
        cover_letter_clear = gr.update(value="")
        return loading_update, cover_letter_clear
    
    def hide_loading_status(self) -> gr.update:
        """
        Hide the loading status in the UI.
        
        Returns:
            Gradio update object to hide loading message
        """
        return gr.update(visible=False)
    
    def process_cover_letter(
        self, 
        resume_file: ResumeFile, 
        job_description: str, 
        file_type: FileType,
        progress: Optional[gr.Progress] = None
    ) -> Tuple[str, gr.update]:
        """
        Process cover letter generation with comprehensive error handling.
        
        This method orchestrates the entire cover letter generation process:
        1. Validates inputs
        2. Detects file type
        3. Validates file size
        4. Generates cover letter
        5. Returns result with proper error handling
        
        Args:
            resume_file: The uploaded resume file
            job_description: The job description text
            file_type: User-specified file type or "auto"
            progress: Optional Gradio progress callback
            
        Returns:
            Tuple of (result_content, loading_status_update)
            
        Examples:
            >>> processor = CoverLetterProcessor()
            >>> result, status = processor.process_cover_letter(file, "Software Engineer", "auto")
            >>> print(result[:50])
            "# Cover Letter for Software Engineer at Company"
        """
        # Step 1: Validate inputs
        is_valid, error_message = validate_inputs(resume_file, job_description)
        if not is_valid:
            return error_message, self.hide_loading_status()
        
        try:
            # Step 2: Show loading animation
            if progress:
                progress(None, desc="🔍 Analyzing - this may take a few minutes...")
            
            # Step 3: Detect file type
            detected_file_type = detect_file_type(resume_file.name, file_type)
            
            # Step 4: Validate file size
            is_size_valid, size_error = validate_file_size(resume_file.name)
            if not is_size_valid:
                return size_error, self.hide_loading_status()
            
            # Step 5: Generate cover letter
            result = self.generator.generate_cover_letter(
                resume_file, 
                job_description, 
                detected_file_type, 
                progress
            )
            
            # Step 6: Return success result
            return result, self.hide_loading_status()
            
        except FileNotFoundError as e:
            error_msg = f"❌ File not found: {str(e)}"
            return error_msg, self.hide_loading_status()
            
        except PermissionError as e:
            error_msg = f"❌ Permission denied: {str(e)}"
            return error_msg, self.hide_loading_status()
            
        except Exception as e:
            error_msg = f"❌ Unexpected error: {str(e)}"
            return error_msg, self.hide_loading_status()
    
    def get_processing_result(
        self, 
        resume_file: ResumeFile, 
        job_description: str, 
        file_type: FileType
    ) -> ProcessingResult:
        """
        Get a structured processing result (useful for testing).
        
        Args:
            resume_file: The uploaded resume file
            job_description: The job description text
            file_type: User-specified file type or "auto"
            
        Returns:
            ProcessingResult object with success status and content/error
        """
        try:
            content, _ = self.process_cover_letter(resume_file, job_description, file_type)
            
            # Check if content starts with error indicators
            if content.startswith("❌") or content.startswith("Error"):
                return ProcessingResult(
                    success=False,
                    error_message=content
                )
            else:
                return ProcessingResult(
                    success=True,
                    content=content
                )
                
        except Exception as e:
            return ProcessingResult(
                success=False,
                error_message=f"Processing failed: {str(e)}"
            )
