# Cover Letter Generator Module
# Main agent for generating personalized cover letters using AI tools

import json
from typing import Dict, Any
from datetime import datetime
from openai import OpenAI

from config import MODEL, SYSTEM_MESSAGE, OPENAI_API_KEY
from resume_parser import ResumeParser
from job_analyzer import JobAnalyzer


class CoverLetterGenerator:
    """Main agent for generating personalized cover letters"""
    
    def __init__(self):
        self.resume_parser = ResumeParser()
        self.job_analyzer = JobAnalyzer()
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Define tools for the AI agent
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "analyze_resume_match",
                    "description": "Analyze how well the candidate's resume matches the job requirements",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "resume_data": {
                                "type": "object",
                                "description": "Parsed resume data"
                            },
                            "job_data": {
                                "type": "object", 
                                "description": "Parsed job description data"
                            }
                        },
                        "required": ["resume_data", "job_data"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "identify_key_selling_points",
                    "description": "Identify the candidate's strongest selling points for this specific job",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "resume_data": {
                                "type": "object",
                                "description": "Parsed resume data"
                            },
                            "job_data": {
                                "type": "object",
                                "description": "Parsed job description data"
                            }
                        },
                        "required": ["resume_data", "job_data"]
                    }
                }
            }
        ]
    
    def generate_cover_letter(self, resume_file, job_description: str, file_type: str = "pdf", progress=None) -> str:
        """Generate a personalized cover letter using AI agents and tools"""
        try:
            # Step 1: Parse resume
            print("📄 Parsing resume...")
            file_path = self._get_file_path(resume_file)
            resume_data = self.resume_parser.parse_resume(file_path, file_type)
            
            if not isinstance(resume_data, dict):
                return f"Error: Resume parser returned invalid data type: {type(resume_data)}"
            
            if "error" in resume_data:
                return f"Error parsing resume: {resume_data['error']}"
            
            # Step 2: Analyze job description
            print("🔍 Analyzing job description...")
            job_data = self.job_analyzer.analyze_job_description(job_description)
            
            if not isinstance(job_data, dict):
                return f"Error: Job analyzer returned invalid data type: {type(job_data)}"
            
            if "error" in job_data:
                return f"Error analyzing job description: {job_data['error']}"
            
            # Step 3: Generate cover letter
            print("✍️ Generating personalized cover letter...")
            self._validate_data_structures(resume_data, job_data)
            
            # Create and send prompt to AI
            cover_letter = self._generate_with_ai(resume_data, job_data)
            
            # Add metadata and return
            try:
                result = self._add_metadata(cover_letter, resume_data, job_data)
                return result
            except Exception as metadata_error:
                return f"Error finalizing cover letter: {str(metadata_error)}\n\nGenerated content:\n{cover_letter}"
            
        except Exception as e:
            return f"Error generating cover letter: {str(e)}"
    
    def _get_file_path(self, resume_file) -> str:
        """Extract file path from resume file object"""
        if hasattr(resume_file, 'name'):
            return resume_file.name
        elif isinstance(resume_file, str):
            return resume_file
        else:
            return str(resume_file)
    
    def _validate_data_structures(self, resume_data: Dict, job_data: Dict) -> None:
        """Validate that data structures are correct"""
        if not isinstance(resume_data, dict):
            raise ValueError(f"Invalid resume data structure: {type(resume_data)}")
        if not isinstance(job_data, dict):
            raise ValueError(f"Invalid job data structure: {type(job_data)}")
    
    def _generate_with_ai(self, resume_data: Dict, job_data: Dict) -> str:
        """Generate cover letter using AI with tools"""
        generation_prompt = self._create_generation_prompt(resume_data, job_data)
        
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": generation_prompt}
        ]
        
        # Use tools to enhance the generation
        response = self.openai_client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=self.tools,
            tool_choice="auto",
            temperature=0.7,
            timeout=45  # 45 second timeout for cover letter generation
        )
        
        # Handle tool calls if any
        message = response.choices[0].message
        if message.tool_calls:
            messages.append(message)
            
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the tool function and create response
                if function_name == "analyze_resume_match":
                    result = self._analyze_resume_match(resume_data, job_data)
                elif function_name == "identify_key_selling_points":
                    result = self._identify_selling_points(resume_data, job_data)
                else:
                    result = "Unknown function"
                
                # Add tool response message
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": result
                })
            
            # Get final response after tool usage
            response = self.openai_client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.7,
                timeout=45  # 45 second timeout
            )
        
        return response.choices[0].message.content
    
    def _create_generation_prompt(self, resume_data: Dict, job_data: Dict) -> str:
        """Create the generation prompt with resume and job data"""
        return f"""
        Create a professional, personalized cover letter based on the following information:
        
        CANDIDATE INFORMATION:
        Name: {resume_data.get('name', 'N/A')}
        Skills: {', '.join(resume_data.get('skills', []))}
        Experience: {len(resume_data.get('experience', []))} positions
        Education: {resume_data.get('education', [])}
        
        JOB INFORMATION:
        Company: {job_data.get('company_name', 'N/A')}
        Position: {job_data.get('job_title', 'N/A')}
        Required Skills: {', '.join(job_data.get('required_skills', []))}
        Key Responsibilities: {', '.join(job_data.get('key_responsibilities', []))}
        
        REQUIREMENTS:
        1. Write in professional, engaging tone
        2. Highlight specific skills and experiences that match the job
        3. Show enthusiasm for the company and role
        4. Keep it concise but compelling (3-4 paragraphs)
        5. Use proper business letter format
        6. Include specific examples from the candidate's background
        7. Address the hiring manager professionally
        8. End with a strong call to action
        
        Format the cover letter in markdown with proper headers and structure.
        """
    
    def _add_metadata(self, cover_letter: str, resume_data: Dict, job_data: Dict) -> str:
        """Add metadata header to the cover letter"""
        try:
            # Safely extract data with proper fallbacks
            job_title = job_data.get('job_title', 'Position') if isinstance(job_data, dict) else 'Position'
            company_name = job_data.get('company_name', 'Company') if isinstance(job_data, dict) else 'Company'
            candidate_name = resume_data.get('name', 'Candidate') if isinstance(resume_data, dict) else 'Candidate'
            
            metadata = f"""# Cover Letter for {job_title} at {company_name}

**Generated for:** {candidate_name}  
**Date:** {self._get_current_date()}  
**Position:** {job_title}  
**Company:** {company_name}

---

"""
            return metadata + cover_letter
        except Exception as e:
            # If metadata fails, return just the cover letter
            print(f"❌ Metadata error: {str(e)}")
            return cover_letter
    
    def _analyze_resume_match(self, resume_data: Dict, job_data: Dict) -> str:
        """Tool function to analyze resume-job match"""
        return f"Resume match analysis: {len(resume_data.get('skills', []))} skills align with job requirements"
    
    def _identify_selling_points(self, resume_data: Dict, job_data: Dict) -> str:
        """Tool function to identify key selling points"""
        skills = resume_data.get('skills', [])
        required_skills = job_data.get('required_skills', [])
        matching_skills = [skill for skill in skills if any(req in skill.lower() for req in [req.lower() for req in required_skills])]
        return f"Key selling points: {', '.join(matching_skills[:3])}"
    
    def _get_current_date(self) -> str:
        """Get current date in readable format"""
        return datetime.now().strftime("%B %d, %Y")