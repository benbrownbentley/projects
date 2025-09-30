# Resume Parser Module
# Handles parsing and extracting information from resume files

import json
import re
from typing import Dict, Any
import PyPDF2
from docx import Document
from openai import OpenAI

from config import (
    MODEL, RESUME_ANALYSIS_PROMPT, RESUME_TEMPLATE, 
    FALLBACK_RESUME_DATA, OPENAI_API_KEY
)


class ResumeParser:
    """Tool for parsing and analyzing resume content"""
    
    def __init__(self):
        self.parsed_data = {}
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    def extract_text_from_docx(self, docx_file) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    def parse_resume(self, resume_file_path: str, file_type: str) -> Dict[str, Any]:
        """Parse resume and extract structured information"""
        try:
            # Check file size (limit to 2MB)
            import os
            file_size = os.path.getsize(resume_file_path)
            if file_size > 2 * 1024 * 1024:  # 2MB limit
                print(f"⚠️ File too large: {file_size} bytes (max 2MB)")
                return {"error": "Resume file is too large. Please use a file smaller than 2MB."}
            
            # Extract text based on file type
            resume_text = self._extract_resume_text(resume_file_path, file_type)
            
            # Limit text length to prevent API timeouts
            if len(resume_text) > 10000:  # 10k character limit
                resume_text = resume_text[:10000] + "..."
                print(f"⚠️ Resume text truncated to 10,000 characters")
            
            # Use AI to analyze and structure the resume
            structured_data = self._analyze_with_ai(resume_text)
            
            self.parsed_data = structured_data
            return structured_data
            
        except Exception as e:
            print(f"❌ Resume parsing error: {str(e)}")
            return {"error": f"Failed to parse resume: {str(e)}"}
    
    def _extract_resume_text(self, file_path: str, file_type: str) -> str:
        """Extract text from resume file based on type"""
        if file_type.lower() == 'pdf':
            with open(file_path, 'rb') as file:
                return self.extract_text_from_pdf(file)
        elif file_type.lower() in ['docx', 'doc']:
            return self.extract_text_from_docx(file_path)
        else:
            # For text files or other formats
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
    
    def _analyze_with_ai(self, resume_text: str) -> Dict[str, Any]:
        """Use AI to analyze and structure resume content"""
        analysis_prompt = f"""
        Analyze this resume and extract the following information in JSON format:
        
        {json.dumps(RESUME_TEMPLATE, indent=2)}
        
        Resume text:
        {resume_text}
        
        Return only valid JSON, no additional text.
        """
        
        response = self.openai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": RESUME_ANALYSIS_PROMPT},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.1,
            timeout=30  # 30 second timeout
        )
        
        # Parse JSON response
        json_str = response.choices[0].message.content.strip()
        print(f"🔍 AI Response: {json_str[:200]}...")  # Debug output
        
        # Clean up the response to ensure valid JSON
        json_str = re.sub(r'```json\s*', '', json_str)
        json_str = re.sub(r'```\s*$', '', json_str)
        
        try:
            parsed_data = json.loads(json_str)
            print(f"✅ Successfully parsed resume data: {list(parsed_data.keys())}")
            return parsed_data
        except json.JSONDecodeError as json_err:
            print(f"❌ JSON parsing error: {json_err}")
            print(f"❌ Problematic JSON string: {json_str}")
            return FALLBACK_RESUME_DATA
        except Exception as e:
            print(f"❌ Resume parsing error: {str(e)}")
            return FALLBACK_RESUME_DATA
