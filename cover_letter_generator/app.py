"""
Clean, educational main application for the Cover Letter Generator.

This module demonstrates:
- Clean separation of concerns
- Type hints for better code understanding
- Comprehensive error handling
- Educational docstrings and comments
- Simple, readable structure

Learning objectives:
1. How to structure a Gradio application
2. How to separate UI from business logic
3. How to handle errors gracefully
4. How to use type hints effectively
5. How to create maintainable code
"""

import gradio as gr
from typing import Tuple

# Import our clean, modular components
from ui_components import (
    create_file_upload_section,
    create_job_description_section, 
    create_generate_button,
    create_output_section,
    create_examples_section,
    create_footer,
    get_css_styles
)
from processors import CoverLetterProcessor


def create_interface() -> gr.Blocks:
    """
    Create the main Gradio interface.
    
    This function demonstrates how to build a clean, modular Gradio app:
    - Separates UI creation from business logic
    - Uses helper functions for each section
    - Keeps the main function focused and readable
    
    Returns:
        Configured Gradio Blocks interface
    """
    # Initialize our processor (contains all business logic)
    processor = CoverLetterProcessor()
    
    # Create the main interface with styling
    with gr.Blocks(
        title="AI Cover Letter Generator",
        theme=gr.themes.Soft(),
        css=get_css_styles()
    ) as interface:
        
        # Main header
        gr.Markdown("""
        # 🤖 AI-Powered Cover Letter Generator
        
        Upload your resume and paste a job description to generate a personalized, professional cover letter using advanced AI analysis.
        
        **Features:**
        - 📄 Supports PDF, DOCX, and text files (max 2MB)
        - 🔍 Intelligent resume and job description analysis
        - ✍️ Personalized cover letter generation
        - 🎯 Matches your skills to job requirements
        - 📝 Professional formatting in markdown
        - ⏱️ Optimized for fast processing with API timeouts
        """)
        
        # Create the main layout using helper functions
        with gr.Row():
            # Left column: Inputs
            with gr.Column(scale=1):
                resume_file, file_type = create_file_upload_section()
                job_description = create_job_description_section()
                generate_btn = create_generate_button()
            
            # Right column: Outputs
            with gr.Column(scale=2):
                loading_status, cover_letter_output = create_output_section()
        
        # Set up event handlers (this is where the magic happens!)
        _setup_event_handlers(
            generate_btn, 
            resume_file, 
            job_description, 
            file_type,
            cover_letter_output, 
            loading_status,
            processor
        )
        
        # Add examples and footer
        create_examples_section()
        create_footer()
    
    return interface


def _setup_event_handlers(
    generate_btn: gr.Button,
    resume_file: gr.File,
    job_description: gr.Textbox,
    file_type: gr.Dropdown,
    cover_letter_output: gr.Markdown,
    loading_status: gr.Markdown,
    processor: CoverLetterProcessor
) -> None:
    """
    Set up the event handlers for the interface.
    
    This function demonstrates:
    - How to chain Gradio events (.click().then())
    - How to separate UI logic from business logic
    - How to handle multiple outputs cleanly
    
    Args:
        generate_btn: The generate button
        resume_file: File upload input
        job_description: Text input for job description
        file_type: Dropdown for file type selection
        cover_letter_output: Markdown output for cover letter
        loading_status: Markdown output for loading status
        processor: The business logic processor
    """
    # Chain two events:
    # 1. First: Show loading status immediately when clicked
    # 2. Then: Process the cover letter and update outputs
    generate_btn.click(
        fn=processor.show_loading_status,  # Show loading immediately and clear output
        outputs=[loading_status, cover_letter_output]
    ).then(
        fn=processor.process_cover_letter,  # Then process the request
        inputs=[resume_file, job_description, file_type],
        outputs=[cover_letter_output, loading_status],
        show_progress=False  # Disable Gradio's built-in progress indicator
    )


def main() -> None:
    """
    Main function to run the application.
    
    This demonstrates:
    - Simple application startup
    - Port handling for development
    - Clean error handling
    """
    print("🚀 Starting AI Cover Letter Generator...")
    print("📱 Opening Gradio interface...")
    print("💡 If browser doesn't open automatically, look for the URL in the output below!")
    
    # Create the interface
    interface = create_interface()
    
    # Try different ports if the default is occupied
    ports_to_try = [7860, 7861, 7862, 7863, 7864]
    
    for port in ports_to_try:
        try:
            print(f"🚀 Trying to launch on port {port}...")
            print(f"✅ Successfully launched on port {port}!")
            print(f"🌐 Local access: http://127.0.0.1:{port}")
            print(f"🌍 Public URL will be generated by Gradio...")
            
            interface.launch(
                server_name="0.0.0.0",  # Allow external connections
                server_port=port,
                share=True,  # Enable Gradio's public sharing
                show_error=True,
                quiet=False,
                inbrowser=True  # Automatically open browser
            )
            break
            
        except OSError as e:
            if "Cannot find empty port" in str(e) and port < ports_to_try[-1]:
                print(f"❌ Port {port} is busy, trying next port...")
                continue
            else:
                print(f"❌ Failed to launch: {e}")
                break


# This is the standard Python idiom for running a script
if __name__ == "__main__":
    main()

