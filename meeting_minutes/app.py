"""
Meeting Minutes Generator - Main Application

A Gradio-based application that processes MP3 meeting recordings and generates
comprehensive meeting summaries with action items and next steps.

Features:
- MP3 audio file upload and processing
- AI-powered meeting transcription
- Intelligent meeting summarization
- Action item extraction
- Next steps identification
- Professional formatting
"""

import gradio as gr
import os
import tempfile
from typing import Tuple, Optional
from datetime import datetime

# Import our modules
from audio_processor import AudioProcessor
from meeting_analyzer import MeetingAnalyzer
from config import OPENAI_API_KEY, MAX_FILE_SIZE_MB


class MeetingMinutesGenerator:
    """Main application class for generating meeting minutes."""
    
    def __init__(self):
        """Initialize the meeting minutes generator."""
        self.audio_processor = AudioProcessor()
        self.meeting_analyzer = MeetingAnalyzer()
    
    def process_meeting(self, audio_file, meeting_title: str = "", participants: str = "") -> Tuple[str, str]:
        """
        Process an MP3 meeting recording and generate minutes.
        
        Args:
            audio_file: Uploaded MP3 file
            meeting_title: Optional meeting title
            participants: Optional list of participants
            
        Returns:
            Tuple of (summary, action_items)
        """
        if audio_file is None:
            return "❌ Please upload an MP3 file.", ""
        
        try:
            # Step 1: Validate file
            if not self._validate_audio_file(audio_file):
                return "❌ Invalid file format. Please upload an MP3 file.", ""
            
            # Step 2: Transcribe audio
            transcription = self.audio_processor.transcribe_audio(audio_file)
            if not transcription:
                return "❌ Failed to transcribe audio. Please check your file.", ""
            
            # Step 3: Analyze meeting
            summary, action_items = self.meeting_analyzer.analyze_meeting(
                transcription, 
                meeting_title, 
                participants
            )
            
            return summary, action_items
            
        except Exception as e:
            return f"❌ Error processing meeting: {str(e)}", ""
    
    def _validate_audio_file(self, audio_file) -> bool:
        """Validate the uploaded audio file."""
        if not audio_file:
            return False
        
        # Check file extension
        if not audio_file.name.lower().endswith('.mp3'):
            return False
        
        # Check file size
        try:
            file_size_mb = os.path.getsize(audio_file.name) / (1024 * 1024)
            if file_size_mb > MAX_FILE_SIZE_MB:
                return False
        except:
            return False
        
        return True


def create_interface() -> gr.Blocks:
    """Create the Gradio interface for the meeting minutes generator."""
    
    generator = MeetingMinutesGenerator()
    
    with gr.Blocks(
        title="Meeting Minutes Generator",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: auto !important;
        }
        .meeting-output {
            font-family: 'Georgia', serif;
            line-height: 1.6;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            white-space: pre-wrap !important;
            max-width: 100% !important;
        }
        .action-items {
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 15px;
            margin: 10px 0;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🎙️ Meeting Minutes Generator
        
        Upload an MP3 recording of your meeting to automatically generate:
        - 📝 Comprehensive meeting summary
        - ✅ Action items and next steps
        - 👥 Participant identification
        - 🎯 Key decisions and outcomes
        
        **Features:**
        - 🎵 Supports MP3 audio files (max 50MB)
        - 🤖 AI-powered transcription and analysis
        - 📋 Professional meeting minutes format
        - ⚡ Fast processing with progress indicators
        """)
        
        with gr.Row():
            # Left column: Inputs
            with gr.Column(scale=1):
                gr.Markdown("### 📁 Upload Meeting Recording")
                
                audio_file = gr.File(
                    label="Upload MP3 file",
                    file_types=[".mp3"],
                    type="filepath"
                )
                
                meeting_title = gr.Textbox(
                    label="Meeting Title (Optional)",
                    placeholder="e.g., Weekly Team Standup",
                    lines=1
                )
                
                participants = gr.Textbox(
                    label="Participants (Optional)",
                    placeholder="e.g., John, Sarah, Mike",
                    lines=2
                )
                
                process_btn = gr.Button(
                    "🚀 Generate Meeting Minutes",
                    variant="primary",
                    size="lg"
                )
            
            # Right column: Outputs
            with gr.Column(scale=2):
                gr.Markdown("### 📋 Generated Meeting Minutes")
                
                # Loading status
                loading_status = gr.Markdown(
                    value="",
                    visible=False,
                    elem_classes=["loading-status"]
                )
                
                # Meeting summary output
                summary_output = gr.Textbox(
                    label="Meeting Summary",
                    elem_classes=["meeting-output"],
                    lines=15,
                    max_lines=25,
                    interactive=False,
                    show_copy_button=True,
                    value="Upload an MP3 file to generate meeting minutes."
                )
                
                # Action items output
                action_items_output = gr.Textbox(
                    label="Action Items & Next Steps",
                    elem_classes=["action-items"],
                    lines=10,
                    max_lines=20,
                    interactive=False,
                    show_copy_button=True,
                    value=""
                )
        
        # Event handlers
        process_btn.click(
            fn=lambda: (gr.update(visible=True, value="🔄 Processing audio file..."), gr.update(value="")),
            outputs=[loading_status, summary_output]
        ).then(
            fn=generator.process_meeting,
            inputs=[audio_file, meeting_title, participants],
            outputs=[summary_output, action_items_output],
            show_progress=True
        ).then(
            fn=lambda: gr.update(visible=False),
            outputs=[loading_status]
        )
        
        # Examples section
        with gr.Accordion("💡 Tips for Best Results", open=False):
            gr.Markdown("""
            **For optimal results:**
            - 🎤 Use clear audio recordings with minimal background noise
            - 📝 Provide meeting title and participants for better context
            - ⏱️ Keep recordings under 2 hours for best processing speed
            - 🗣️ Ensure speakers are clearly audible and distinct
            
            **Supported formats:**
            - ✅ MP3 files only
            - ✅ Maximum file size: 50MB
            - ✅ Any meeting length (processing time varies)
            """)
        
        # Footer
        gr.Markdown("""
        <div style='text-align: center; color: #666; font-size: 0.9em; margin-top: 20px;'>
        Meeting Minutes Generator | Built with ❤️ using Gradio & OpenAI
        </div>
        """)
    
    return interface


def main():
    """Main function to run the application."""
    print("🚀 Starting Meeting Minutes Generator...")
    print("📱 Opening Gradio interface...")
    
    interface = create_interface()
    
    # Try different ports if 7860 is occupied
    ports_to_try = [7860, 7861, 7862, 7863, 7864]
    
    for port in ports_to_try:
        try:
            print(f"🚀 Trying to launch on port {port}...")
            print(f"✅ Successfully launched on port {port}!")
            print(f"🌐 Local access: http://127.0.0.1:{port}")
            print(f"🌍 Public URL will be generated by Gradio...")
            
            interface.launch(
                server_name="0.0.0.0",
                server_port=port,
                share=True,
                show_error=True,
                quiet=False,
                inbrowser=True
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
