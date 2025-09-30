# Job Analyzer Module
# Handles parsing and analyzing job descriptions

import json
import re
from typing import Dict, Any
from openai import OpenAI

from config import (
    MODEL, JOB_ANALYSIS_PROMPT, JOB_TEMPLATE, 
    FALLBACK_JOB_DATA, OPENAI_API_KEY
)


class JobAnalyzer:
    """Tool for analyzing job descriptions"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
    
    def analyze_job_description(self, job_description: str) -> Dict[str, Any]:
        """Analyze job description and extract key requirements"""
        try:
            analysis_prompt = f"""
            Analyze this job description and extract the following information in JSON format:
            
            {json.dumps(JOB_TEMPLATE, indent=2)}
            
            Job Description:
            {job_description}
            
            Return only valid JSON, no additional text.
            """
            
            response = self.openai_client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": JOB_ANALYSIS_PROMPT},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.1,
                timeout=30  # 30 second timeout
            )
            
            # Parse JSON response
            json_str = response.choices[0].message.content.strip()
            print(f"🔍 Job Analysis AI Response: {json_str[:200]}...")  # Debug output
            
            json_str = re.sub(r'```json\s*', '', json_str)
            json_str = re.sub(r'```\s*$', '', json_str)
            
            try:
                job_data = json.loads(json_str)
                print(f"✅ Successfully parsed job data: {list(job_data.keys())}")
                return job_data
            except json.JSONDecodeError as json_err:
                print(f"❌ Job analysis JSON parsing error: {json_err}")
                print(f"❌ Problematic JSON string: {json_str}")
                return FALLBACK_JOB_DATA
            
        except Exception as e:
            print(f"❌ Job analysis error: {str(e)}")
            return {"error": f"Failed to analyze job description: {str(e)}"}
