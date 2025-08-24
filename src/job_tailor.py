import json
import os
from pathlib import Path

import PyPDF2
from docx import Document

from helpers import Prompt, set_client, Model


class JobTailor:
    def __init__(self, resume_path: Path, job_desc_path: Path):
        self.resume_filename = resume_path.name
        self.resume_text = self.parse_file(resume_path)

        self.job_desc_filename = job_desc_path.name
        self.job_desc_text = self.parse_file(job_desc_path)

        self.user_context: str = ""

        self.model: Model = Model.GROK


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


    def add_user_context(self, user_context: str) -> None:
        self.user_context = user_context

    
    def configure_client(self, model: Model) -> None:
        self.client = set_client(model)

        
    def tailor_resume(self) -> json:
        try:
            return self.generate_prompt("tailor_resume")
        except Exception as e:
            raise Exception(f"Error tailoring resume: {str(e)}")

    
    def generate_cover_letter(self) -> json:
        try:
            return self.generate_prompt("cover_letter")
            #TODO: add functionality to convert output into a docx file and return that instead
        except Exception as e:
            raise Exception(f"Error tailoring resume: {str(e)}")

    
    def generate_prompt(self, purpose: str) -> json:
        """Tailor resume to match job description using AI"""
        prompt = self.get_prompt(purpose)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt.sys_prompt},
                {"role": "user", "content": prompt.usr_prompt}
            ],
            temperature=0.7,
            top_p=0.8,
            max_tokens=4000
        )
        
        return response.choices[0].message.content


    def get_prompt(self, purpose: str) -> Prompt:
        sys_prompt_path = Path( Path(__file__).parent.parent, "prompts", {purpose}, "sys_prompt.txt" )
        usr_prompt_path = Path( Path(__file__).parent.parent, "prompts", {purpose}, "usr_prompt.txt" )

        with open(sys_prompt_path, "r") as f:
            sys_prompt = f.read()

        with open(usr_prompt_path, "r") as f:
            usr_prompt = f.read()
            usr_prompt = usr_prompt.replace("{job_desc}", self.job_desc_text)
            usr_prompt = usr_prompt.replace("{resume}", self.resume_text)
            usr_prompt = usr_prompt.replace("{user_context}", self.user_context)

        return Prompt(sys_prompt=sys_prompt, usr_prompt=usr_prompt)