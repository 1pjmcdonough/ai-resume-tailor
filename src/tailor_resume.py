import os
import re
from typing import Dict, List
from dotenv import load_dotenv
from openai import OpenAI
import PyPDF2
import io
from data_classes import ResumeData, JobDescription
from pathlib import Path
from docx import Document

# Load environment variables
dotenv_path = Path( Path(__file__).parent.parent, ".env" )
load_dotenv(dotenv_path=dotenv_path)
api_key = os.getenv("XAI_API_KEY")

class TailorResume:
    
    def __init__(self):
        self.resume_path: Path
        self.job_desc_path: Path


    def parse_file(self, file_path: Path) -> str:
        """Extract text content from a file (pdf, docx, or txt)"""
        file_type = file_path.suffix.lower()

        if file_type == ".pdf":
            pdf_reader = PyPDF2.PdfReader(file_path)
            return "\n".join([p.extract_text() for p in pdf_reader.pages])
        elif file_type == ".docx":
            doc = Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        elif file_type == ".txt":
            with open(file_path, "r") as f:
                 return f.read()
        else:
            raise ValueError(f"Unsupported file type: {file_type}")


    def upload_resume(self) -> str:
        """Parse resume file (PDF or DOCX) and extract text content"""
        self.resume = self.parse_file(self.resume_path)


    def upload_job_desc(self) -> str:
        """Parse job description file and extract key information"""
        self.job_desc = self.parse_file(self.job_desc_path)


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