# Main Gradio Application for Cover Letter Generator
# Clean, focused UI with progress indicators

import gradio as gr
from cover_letter_generator import CoverLetterGenerator


def create_gradio_interface():
    """Create and configure the Gradio interface"""
    
    generator = CoverLetterGenerator()
    
    def process_cover_letter(resume_file, job_description, file_type, progress=gr.Progress()):
        """Process the cover letter generation with progress updates"""
        if resume_file is None:
            return "❌ Please upload a resume file.", "❌ Please upload a resume file."
        
        if not job_description.strip():
            return "❌ Please provide a job description.", "❌ Please provide a job description."
        
        try:
            progress(0.1, desc="📄 Starting cover letter generation...")
            status = "📄 Starting cover letter generation..."
            
            # Determine file type if not specified
            if file_type == "auto":
                if resume_file.name.lower().endswith('.pdf'):
                    file_type = "pdf"
                elif resume_file.name.lower().endswith(('.docx', '.doc')):
                    file_type = "docx"
                else:
                    file_type = "text"
            
            progress(0.2, desc="🔍 Analyzing resume...")
            status = "🔍 Analyzing resume content..."
            
            # Generate cover letter
            result = generator.generate_cover_letter(resume_file, job_description, file_type, progress)
            
            progress(1.0, desc="✅ Cover letter generated successfully!")
            status = "✅ Cover letter generated successfully!"
            
            return result, status
            
        except Exception as e:
            progress(1.0, desc="❌ Error occurred")
            error_msg = f"❌ Error: {str(e)}"
            return error_msg, error_msg
    
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
        """
    ) as interface:
        
        gr.Markdown("""
        # 🤖 AI-Powered Cover Letter Generator
        
        Upload your resume and paste a job description to generate a personalized, professional cover letter using advanced AI analysis.
        
        **Features:**
        - 📄 Supports PDF, DOCX, and text files
        - 🔍 Intelligent resume and job description analysis
        - ✍️ Personalized cover letter generation
        - 🎯 Matches your skills to job requirements
        - 📝 Professional formatting in markdown
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
                    lines=15,
                    max_lines=20
                )
                
                generate_btn = gr.Button(
                    "🚀 Generate Cover Letter",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=2):
                gr.Markdown("### ✍️ Generated Cover Letter")
                
                # Status message
                status_message = gr.Markdown(
                    value="Ready to generate cover letter. Upload your resume and paste a job description.",
                    label="Status"
                )
                
                cover_letter_output = gr.Markdown(
                    label="Cover Letter",
                    elem_classes=["cover-letter-output"],
                    show_copy_button=True
                )
        
        # Event handlers
        generate_btn.click(
            fn=process_cover_letter,
            inputs=[resume_file, job_description, file_type],
            outputs=[cover_letter_output, status_message],
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
    
    return interface


def main():
    """Main function to run the application"""
    print("🚀 Starting AI Cover Letter Generator...")
    print("📱 Opening Gradio interface...")
    
    interface = create_gradio_interface()
    
    # Try different ports if 7860 is occupied
    ports_to_try = [7860, 7861, 7862, 7863, 7864]
    
    for port in ports_to_try:
        try:
            print(f"🚀 Trying to launch on port {port}...")
            interface.launch(
                server_name="127.0.0.1",
                server_port=port,
                share=False,
                show_error=True,
                quiet=False
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
