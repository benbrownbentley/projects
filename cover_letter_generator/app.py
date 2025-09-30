# Main Gradio Application for Cover Letter Generator
# Clean, focused UI with progress indicators

import gradio as gr
from cover_letter_generator import CoverLetterGenerator


def create_gradio_interface():
    """Create and configure the Gradio interface"""
    
    generator = CoverLetterGenerator()
    
    def show_loading():
        """Show loading status"""
        return gr.update(
            visible=True, 
            value="<div style='text-align: center; padding: 20px; font-size: 18px; color: #007bff;'>🔍 Analyzing - this may take a few minutes...</div>"
        )
    
    def process_cover_letter(resume_file, job_description, file_type, progress=gr.Progress()):
        """Process the cover letter generation with progress updates"""
        if resume_file is None:
            return "❌ Please upload a resume file."
        
        if not job_description.strip():
            return "❌ Please provide a job description."
        
        try:
            # Show loading animation
            progress(None, desc="🔍 Analyzing - this may take a few minutes...")
            
            # Determine file type if not specified
            if file_type == "auto":
                if resume_file.name.lower().endswith('.pdf'):
                    file_type = "pdf"
                elif resume_file.name.lower().endswith(('.docx', '.doc')):
                    file_type = "docx"
                else:
                    file_type = "text"
            
            # Generate cover letter (timeout handled by OpenAI client timeouts)
            result = generator.generate_cover_letter(resume_file, job_description, file_type, progress)
            
            return result, gr.update(visible=False)
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            return error_msg, gr.update(visible=False)
    
    # Create Gradio interface
    with gr.Blocks(
        title="AI Cover Letter Generator",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: auto !important;
        }
        .cover-letter-output {
            font-family: 'Georgia', serif;
            line-height: 1.6;
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
    ) as interface:
        
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
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📄 Upload Resume")
                resume_file = gr.File(
                    label="Upload your resume",
                    file_types=[".pdf", ".docx", ".doc", ".txt"],
                    type="filepath"
                )
                
                file_type = gr.Radio(
                    choices=["auto", "pdf", "docx", "text"],
                    value="auto",
                    label="File type (auto-detect recommended)"
                )
                
                gr.Markdown("### 📋 Job Description")
                job_description = gr.Textbox(
                    label="Paste the job description here",
                    placeholder="Copy and paste the complete job description...",
                    lines=12,
                    max_lines=20
                )
                
                generate_btn = gr.Button(
                    "🚀 Generate Cover Letter",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=2):
                gr.Markdown("### ✍️ Generated Cover Letter")
                
                # Loading status (initially hidden)
                loading_status = gr.Markdown(
                    value="",
                    visible=False,
                    elem_classes=["loading-status"]
                )
                
                # Cover letter output
                cover_letter_output = gr.Markdown(
                    label="Cover Letter",
                    elem_classes=["cover-letter-output"],
                    show_copy_button=True,
                    value="Upload your resume and paste a job description to get started."
                )
        
        # Event handlers
        generate_btn.click(
            fn=show_loading,
            outputs=[loading_status]
        ).then(
            fn=process_cover_letter,
            inputs=[resume_file, job_description, file_type],
            outputs=[cover_letter_output, loading_status],
            show_progress=True
        )
        
        # Example job descriptions (removed gr.Examples to avoid file path issues)
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
        
        gr.Markdown("""
        ---
        **💡 Tips for best results:**
        - Upload a complete, well-formatted resume
        - Include the full job description with requirements and responsibilities
        - The AI will automatically match your skills to job requirements
        - Generated cover letters are formatted in markdown for easy editing
        """)
        
        # Footer
        gr.Markdown("""
        <div style='text-align: center; color: #666; font-size: 0.9em; margin-top: 20px;'>
        AI Cover Letter Generator | Built with ❤️ using Gradio & OpenAI
        </div>
        """)
    
    return interface


def main():
    """Main function to run the application"""
    print("🚀 Starting AI Cover Letter Generator...")
    print("📱 Opening Gradio interface...")
    print("💡 If browser doesn't open automatically, look for the URL in the output below!")
    
    interface = create_gradio_interface()
    
    # Try different ports if 7860 is occupied
    ports_to_try = [7860, 7861, 7862, 7863, 7864]
    
    for port in ports_to_try:
        try:
            print(f"🚀 Trying to launch on port {port}...")
            print(f"✅ Successfully launched on port {port}!")
            print(f"🌐 Opening browser to: http://127.0.0.1:{port}")
            
            interface.launch(
                server_name="127.0.0.1",
                server_port=port,
                share=False,
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


if __name__ == "__main__":
    main()
