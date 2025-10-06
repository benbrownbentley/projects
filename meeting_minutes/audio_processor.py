"""
Audio Processing Module for Meeting Minutes Generator

This module handles MP3 audio file processing and transcription using OpenAI's Whisper API.
"""

import os
import tempfile
from typing import Optional
from openai import OpenAI
from config import OPENAI_API_KEY


class AudioProcessor:
    """Handles audio file processing and transcription."""
    
    def __init__(self):
        """Initialize the audio processor with OpenAI client."""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        """
        Transcribe an MP3 audio file to text using OpenAI Whisper.
        
        Args:
            audio_file_path: Path to the MP3 audio file
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            # Validate file exists
            if not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            # Open the audio file
            with open(audio_file_path, "rb") as audio_file:
                # Transcribe using OpenAI Whisper
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
                
                return transcript
                
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return None
    
    def validate_audio_file(self, file_path: str) -> bool:
        """
        Validate that the uploaded file is a valid MP3 audio file.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check file extension
            if not file_path.lower().endswith('.mp3'):
                return False
            
            # Check file exists
            if not os.path.exists(file_path):
                return False
            
            # Check file size (basic validation)
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                return False
            
            return True
            
        except Exception:
            return False
    
    def get_audio_duration(self, file_path: str) -> Optional[float]:
        """
        Get the duration of an audio file in seconds.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Duration in seconds or None if failed
        """
        try:
            # This is a placeholder - in a real implementation, you might use
            # libraries like pydub or librosa to get accurate duration
            # For now, we'll estimate based on file size (rough approximation)
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            
            # Rough estimate: 1MB ≈ 1 minute of MP3 audio
            estimated_duration = file_size_mb * 60
            
            return estimated_duration
            
        except Exception:
            return None
