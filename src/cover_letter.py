from helpers import ResumeData, JobDescription

def generate_cover_letter_template(self, job_title: str, company: str, 
                                     resume_data: ResumeData, job_desc: JobDescription) -> str:
        """Generate a cover letter template using AI"""
        
        user_prompt = ""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                top_p=0.8,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error generating cover letter: {str(e)}")