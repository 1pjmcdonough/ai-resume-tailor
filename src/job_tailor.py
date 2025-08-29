import json
from pathlib import Path
from typing import Optional

import PyPDF2
from docx import Document
from openai import OpenAI

from helpers import Prompt, set_client


class JobTailor:
    def __init__(self):
        self.model: Optional[str] = "grok-4-0709"
        self.client: OpenAI = set_client(self.model)
        self.user_context: Optional[str] = ""
        self.resume_filename: Optional[str] = ""
        self.job_desc_filename: Optional[str] = ""


    def upload_resume(self, resume_path: Path) -> None:
        self.resume_text = self.parse_file(resume_path)

    
    def upload_job_desc(self, job_desc_path: Path) -> None:
        self.job_desc_text = self.parse_file(job_desc_path)


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

    
    def set_model(self, model: str) -> None:
        self.model = model


    def configure_client(self) -> None:
        self.client = set_client(self.model)

        
    def tailor_resume(self) -> None:
        try:
            resume_edits = self.generate_prompt("tailor_resume")
            self.save_response(resume_edits, "resume_edits")
        except Exception as e:
            raise Exception(f"Error tailoring resume: {str(e)}")
        
    
    def generate_cover_letter(self) -> None:
        try:
            cover_letter = self.generate_prompt("cover_letter")
            self.save_response(cover_letter, "cover_letter")
        except Exception as e:
            raise Exception(f"Error generating cover letter: {str(e)}")

        
    def generate_prompt(self, purpose: str) -> str:
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
        sys_prompt_path = Path( Path(__file__).parent.parent, "prompts", purpose, "sys_prompt.txt" )
        usr_prompt_path = Path( Path(__file__).parent.parent, "prompts", purpose, "usr_prompt.txt" )

        with open(sys_prompt_path, "r") as f:
            sys_prompt = f.read()

        with open(usr_prompt_path, "r") as f:
            usr_prompt = f.read()
            usr_prompt = usr_prompt.replace("{job_desc}", self.job_desc_text)
            usr_prompt = usr_prompt.replace("{resume}", self.resume_text)
            usr_prompt = usr_prompt.replace("{user_context}", self.user_context)

        return Prompt(sys_prompt=sys_prompt, usr_prompt=usr_prompt)


    def save_response(self, response: str, response_type: str) -> None:
        """Save a single response as a text file in organized folders"""
        try:
            response_history_path = Path(Path(__file__).parent.parent, "response_history")
            curr_response_folder = f"{self.resume_filename}_for_{self.job_desc_filename}"
            curr_response_path = Path(response_history_path, curr_response_folder) 
            curr_response_path.mkdir(exist_ok=True)

            filename = f"{response_type}.txt"
            response_path = Path(curr_response_folder, filename)
            with open(response_path, "w", encoding="utf-8") as f:
                f.write(response)
            
            metadata = {
                "resume_filename": self.resume_filename,
                "job_description_filename": self.job_desc_filename,
                "user_context": getattr(self, 'user_context', ''),
                "model_used": getattr(self, 'model', '')
            }
            
            metadata_path = Path(curr_response_folder, "metadata.json")
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
                
        except Exception as e:
            raise Exception(f"Error saving response: {str(e)}")


# jt = JobTailor()
# jt.upload_resume(Path("/Users/phillipmcdonough/Desktop/McDonough_Phil_J.pdf"))
# jt.upload_job_desc(Path("/Users/phillipmcdonough/Desktop/test.txt"))
# jt.generate_prompt("tailor_resume")