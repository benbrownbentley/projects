"""
Configuration settings for the Meeting Minutes Generator.

This module contains all configuration settings, API keys, and constants.
"""

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

# Application Settings
MAX_FILE_SIZE_MB = 50  # Maximum MP3 file size in MB
SUPPORTED_FORMATS = [".mp3"]
DEFAULT_MODEL = "gpt-4o-mini"
WHISPER_MODEL = "whisper-1"

# UI Settings
MAX_SUMMARY_LENGTH = 2000
MAX_ACTION_ITEMS_LENGTH = 1500
DEFAULT_TEMPERATURE = 0.3

# File Processing Settings
TEMP_DIR = "/tmp"  # Directory for temporary files
MAX_TRANSCRIPTION_LENGTH = 100000  # Maximum characters in transcription

# Error Messages
ERROR_MESSAGES = {
    "no_file": "❌ Please upload an MP3 file.",
    "invalid_format": "❌ Invalid file format. Please upload an MP3 file.",
    "file_too_large": f"❌ File too large. Maximum size: {MAX_FILE_SIZE_MB}MB",
    "transcription_failed": "❌ Failed to transcribe audio. Please check your file.",
    "analysis_failed": "❌ Failed to analyze meeting. Please try again.",
    "api_error": "❌ API error. Please check your OpenAI API key."
}

# Success Messages
SUCCESS_MESSAGES = {
    "processing": "🔄 Processing audio file...",
    "transcribing": "🎙️ Transcribing audio...",
    "analyzing": "🧠 Analyzing meeting content...",
    "generating": "📝 Generating meeting minutes...",
    "complete": "✅ Meeting minutes generated successfully!"
}
