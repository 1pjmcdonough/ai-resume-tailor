import os
import re
from typing import Dict, List
from dotenv import load_dotenv
from openai import OpenAI
import PyPDF2
import io
from helpers import ResumeData, JobDescription
from pathlib import Path
from docx import Document

# Load environment variables
dotenv_path = Path( Path(__file__).parent.parent, ".env" )
load_dotenv(dotenv_path=dotenv_path)
api_key = os.getenv("XAI_API_KEY")

class TailorResume:
    """AI Agent for tailoring resumes and generating cover letters"""
    
    def __init__(self, model: str = "grok-4-0709", base_url: str = "https://api.x.ai/v1"):
        """Initialize the Resume Tailor Agent"""
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        
        # System prompt for the AI agent
        self.system_prompt = ""

    def parse_resume_file(self, file_content: bytes, file_type: str) -> ResumeData:
        """Parse resume file (PDF or DOCX) and extract text content"""
        try:
            if file_type == "pdf":
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            elif file_type == "docx":
                doc = Document(io.BytesIO(file_content))
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            # Clean and structure the text
            text = self._clean_text(text)
            sections = self._extract_sections(text)
            word_count = len(text.split())
            page_estimate = word_count / 250  # Rough estimate: 250 words per page
            
            return ResumeData(
                text=text,
                sections=sections,
                word_count=word_count,
                page_estimate=page_estimate
            )
            
        except Exception as e:
            raise Exception(f"Error parsing resume file: {str(e)}")

    def parse_job_description(self, file_content: bytes, file_type: str) -> JobDescription:
        """Parse job description file and extract key information"""
        try:
            if file_type == "pdf":
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            elif file_type == "docx":
                doc = Document(io.BytesIO(file_content))
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            text = self._clean_text(text)
            keywords = self._extract_keywords(text)
            requirements = self._extract_requirements(text)
            responsibilities = self._extract_responsibilities(text)
            
            return JobDescription(
                text=text,
                keywords=keywords,
                requirements=requirements,
                responsibilities=responsibilities
            )
            
        except Exception as e:
            raise Exception(f"Error parsing job description: {str(e)}")

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        # Remove extra whitespace and normalize line breaks
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract common resume sections"""
        sections = {}
        
        # Common section headers
        section_patterns = {
            'summary': r'(?:summary|profile|objective|overview)[:\s]*(.*?)(?=\n\s*[A-Z][A-Z\s]+:|$)',
            'experience': r'(?:experience|work\s+history|employment)[:\s]*(.*?)(?=\n\s*[A-Z][A-Z\s]+:|$)',
            'education': r'(?:education|academic)[:\s]*(.*?)(?=\n\s*[A-Z][A-Z\s]+:|$)',
            'skills': r'(?:skills|technical\s+skills|competencies)[:\s]*(.*?)(?=\n\s*[A-Z][A-Z\s]+:|$)',
            'projects': r'(?:projects|portfolio)[:\s]*(.*?)(?=\n\s*[A-Z][A-Z\s]+:|$)'
        }
        
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sections[section_name] = match.group(1).strip()
        
        return sections

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract potential keywords from job description"""
        # Common technical and soft skill keywords
        common_keywords = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'aws', 'docker',
            'kubernetes', 'agile', 'scrum', 'leadership', 'communication', 'analytics',
            'machine learning', 'data science', 'project management', 'teamwork'
        ]
        
        found_keywords = []
        text_lower = text.lower()
        
        for keyword in common_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        # Add any capitalized technical terms
        tech_terms = re.findall(r'\b[A-Z][a-z]+(?:\.js|\.net|\.com)?\b', text)
        found_keywords.extend([term.lower() for term in tech_terms if len(term) > 2])
        
        return list(set(found_keywords))

    def _extract_requirements(self, text: str) -> List[str]:
        """Extract job requirements and qualifications"""
        requirements = []
        
        # Look for requirement patterns
        req_patterns = [
            r'(?:required|requirement|qualification|must have)[:\s]*(.*?)(?=\n|\.)',
            r'(?:minimum|minimum requirements)[:\s]*(.*?)(?=\n|\.)',
            r'(?:experience|years)[:\s]*(\d+\+?\s+years?.*?)(?=\n|\.)'
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            requirements.extend([match.strip() for match in matches])
        
        return requirements

    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities and duties"""
        responsibilities = []
        
        # Look for responsibility patterns
        resp_patterns = [
            r'(?:responsibilities|duties|key\s+responsibilities)[:\s]*(.*?)(?=\n\s*[A-Z][A-Z\s]+:|$)',
            r'(?:will|will be responsible for)[:\s]*(.*?)(?=\n|\.)'
        ]
        
        for pattern in resp_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            responsibilities.extend([match.strip() for match in matches])
        
        return responsibilities

    def tailor_resume(self, resume_data: ResumeData, job_desc: JobDescription, 
                      guidelines: str = "") -> Dict[str, str]:
        """Tailor resume to match job description using AI"""
        
        user_prompt = ""

        # Make the AI call
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                top_p=0.8,
                max_tokens=4000  # Increased for comprehensive output
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse the AI response into structured output
            return self._parse_ai_response(ai_response)
            
        except Exception as e:
            raise Exception(f"Error calling AI model: {str(e)}")

    def _parse_ai_response(self, ai_response: str) -> Dict[str, str]:
        """Parse AI response into structured sections"""
        sections = {
            'tailored_resume': '',
            'cover_letter': '',
            'changes_summary': '',
            'word_count': '',
            'recommendations': ''
        }
        
        # Simple parsing based on common section headers
        current_section = None
        lines = ai_response.split('\n')
        
        for line in lines:
            line_lower = line.lower().strip()
            
            if 'tailored resume' in line_lower or 'resume:' in line_lower:
                current_section = 'tailored_resume'
            elif 'cover letter' in line_lower or 'letter:' in line_lower:
                current_section = 'cover_letter'
            elif 'changes' in line_lower or 'summary' in line_lower:
                current_section = 'changes_summary'
            elif 'word count' in line_lower or 'page' in line_lower:
                current_section = 'word_count'
            elif 'recommendations' in line_lower or 'suggestions' in line_lower:
                current_section = 'recommendations'
            elif current_section and line.strip():
                sections[current_section] += line + '\n'
        
        return sections

    

# Example usage function
def main():
    """Example usage of the TailorResume"""
    agent = TailorResume()
    
    print("Resume Tailor AI Agent")
    print("=" * 50)
    print("This agent can:")
    print("1. Parse resume files (PDF/DOCX)")
    print("2. Extract job requirements and keywords") #remove this so the ai does it
    print("3. Tailor resumes to match job descriptions")
    print("4. Generate personalized cover letters") #change to different class
    print("5. Ensure 1-page limit compliance")
    print("\nUse the agent through the UI or import it into your scripts.") #remove cli.py probably

if __name__ == "__main__":
    main()