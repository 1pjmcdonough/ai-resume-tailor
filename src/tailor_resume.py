import json
import os
from pathlib import Path

import PyPDF2
from docx import Document
from dotenv import load_dotenv
from openai import OpenAI

from data_classes import Prompt
from models import set_client

# Load environment variables
dotenv_path = Path( Path(__file__).parent.parent, ".env" )
load_dotenv(dotenv_path=dotenv_path)
api_key = os.getenv("XAI_API_KEY")

class TailorResume:
    def __init__(self, resume_path: Path, job_desc_path: Path):
        self.resume_path: Path = resume_path
        self.job_desc_path: Path = job_desc_path
        self.resume_text = self.upload_resume(resume_path)
        self.job_desc_text = self.upload_job_desc(job_desc_path)


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


    def upload_resume(self, resume_path: Path) -> str:
        """Parse resume file (PDF or DOCX) and extract text content"""
        return self.parse_file(resume_path)


    def upload_job_desc(self, job_desc_path: Path) -> str:
        """Parse job description file and extract key information"""
        return self.parse_file(job_desc_path)

    
    def configure_client(self, model: str = "grok-4-0709") -> OpenAI:
        self.client = set_client(model)


    def get_prompt(self, user_context: str = "") -> Prompt:
        sys_prompt_path = Path( Path(__file__).parent.parent, "prompts", "full_sys_prompt.txt" )
        usr_prompt_path = Path( Path(__file__).parent.parent, "prompts", "usr_prompt.txt" )

        with open(sys_prompt_path, "r") as f:
            sys_prompt = f.read()

        with open(usr_prompt_path, "r") as f:
            usr_prompt = f.read()
            usr_prompt = usr_prompt.replace("{job_desc}", self.job_desc_text)
            usr_prompt = usr_prompt.replace("{resume}", self.resume_text)
            usr_prompt = usr_prompt.replace("{user_context}", user_context)

        return Prompt(sys_prompt=sys_prompt, usr_prompt=usr_prompt)

        
    def tailor_resume(self, user_context: str = "") -> json:
        """Tailor resume to match job description using AI"""
        prompt = self.get_prompt(user_context)

        # Make the AI call
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt.sys_prompt},
                    {"role": "user", "content": prompt.usr_prompt}
                ],
                temperature=0.7,
                top_p=0.8,
                max_tokens=4000  # Increased for comprehensive output
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse the AI response into structured output
            return ai_response
            
        except Exception as e:
            raise Exception(f"Error calling AI model: {str(e)}")

# resume = Path("/Users/phillipmcdonough/Desktop/McDonough_Phil_J.pdf")
# jd = Path("/Users/phillipmcdonough/Downloads/job_desc.pdf")
# test = TailorResume(resume, jd)
# test.configure_client()
# from pprint import pprint
# pprint(test.tailor_resume())