"""
Meeting Analysis Module for Meeting Minutes Generator

This module handles AI-powered analysis of meeting transcriptions to generate
comprehensive summaries and extract action items.
"""

from typing import Tuple, Optional
from openai import OpenAI
from config import OPENAI_API_KEY


class MeetingAnalyzer:
    """Handles AI-powered meeting analysis and summarization."""
    
    def __init__(self):
        """Initialize the meeting analyzer with OpenAI client."""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def analyze_meeting(self, transcription: str, meeting_title: str = "", participants: str = "") -> Tuple[str, str]:
        """
        Analyze a meeting transcription and generate summary with action items.
        
        Args:
            transcription: The transcribed meeting text
            meeting_title: Optional meeting title for context
            participants: Optional list of participants
            
        Returns:
            Tuple of (summary, action_items)
        """
        try:
            # Generate meeting summary
            summary = self._generate_summary(transcription, meeting_title, participants)
            
            # Extract action items
            action_items = self._extract_action_items(transcription, participants)
            
            return summary, action_items
            
        except Exception as e:
            error_msg = f"Error analyzing meeting: {str(e)}"
            return error_msg, ""
    
    def _generate_summary(self, transcription: str, meeting_title: str, participants: str) -> str:
        """
        Generate a comprehensive meeting summary.
        
        Args:
            transcription: The meeting transcription
            meeting_title: Optional meeting title
            participants: Optional participants list
            
        Returns:
            Formatted meeting summary
        """
        # Build context for the AI
        context = f"""
        Meeting Title: {meeting_title if meeting_title else "Not specified"}
        Participants: {participants if participants else "Not specified"}
        
        Meeting Transcription:
        {transcription}
        """
        
        system_prompt = """You are an expert meeting analyst. Create a comprehensive, professional meeting summary that includes:

        1. Meeting Overview
        2. Key Discussion Points
        3. Decisions Made
        4. Important Information Shared
        5. Next Steps Overview

        Format the summary in a clear, professional manner suitable for meeting minutes.
        Use bullet points and clear headings for easy reading.
        Focus on actionable information and key outcomes.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def _extract_action_items(self, transcription: str, participants: str) -> str:
        """
        Extract action items and next steps from the meeting transcription.
        
        Args:
            transcription: The meeting transcription
            participants: Optional participants list
            
        Returns:
            Formatted action items list
        """
        context = f"""
        Participants: {participants if participants else "Not specified"}
        
        Meeting Transcription:
        {transcription}
        """
        
        system_prompt = """You are an expert at extracting action items from meeting discussions. Analyze the transcription and identify:

        1. Specific tasks assigned to individuals
        2. Deadlines and due dates mentioned
        3. Follow-up actions required
        4. Decisions that need implementation
        5. Next meeting or check-in dates

        Format the action items clearly with:
        - Who is responsible (if mentioned)
        - What needs to be done
        - When it's due (if mentioned)
        - Priority level (if apparent)

        If no clear action items are found, indicate that no specific action items were identified.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error extracting action items: {str(e)}"
    
    def _format_meeting_minutes(self, summary: str, action_items: str, meeting_title: str, participants: str) -> str:
        """
        Format the complete meeting minutes document.
        
        Args:
            summary: Meeting summary
            action_items: Action items list
            meeting_title: Meeting title
            participants: Participants list
            
        Returns:
            Formatted meeting minutes document
        """
        from datetime import datetime
        
        current_date = datetime.now().strftime("%B %d, %Y")
        
        minutes = f"""
# Meeting Minutes

**Date:** {current_date}
**Meeting:** {meeting_title if meeting_title else "Untitled Meeting"}
**Participants:** {participants if participants else "Not specified"}

---

## Meeting Summary

{summary}

---

## Action Items & Next Steps

{action_items}

---

*Generated by Meeting Minutes Generator*
        """
        
        return minutes.strip()
