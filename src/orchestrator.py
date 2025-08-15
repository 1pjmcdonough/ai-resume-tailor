"""
Orchestrator module for coordinating resume tailoring workflow
"""
import os
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from tailor_resume import TailorResume, ResumeData, JobDescription

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeTailorOrchestrator:
    """Orchestrates the complete resume tailoring workflow"""
    
    def __init__(self, model: str = "grok-4-0709", base_url: str = "https://api.x.ai/v1"):
        """Initialize the orchestrator with AI agent"""
        self.agent = TailorResume(model=model, base_url=base_url)
        self.workflow_history = []
        
    def run_complete_workflow(self, 
                             resume_path: str,
                             job_desc_path: str,
                             output_dir: str = "output",
                             guidelines: str = "",
                             job_title: str = "",
                             company: str = "") -> Dict[str, str]:
        """
        Run the complete resume tailoring workflow
        
        Args:
            resume_path: Path to resume file
            job_desc_path: Path to job description file
            output_dir: Directory to save outputs
            guidelines: Custom tailoring guidelines
            job_title: Job title for cover letter
            company: Company name for cover letter
            
        Returns:
            Dictionary containing all results
        """
        try:
            logger.info("Starting resume tailoring workflow...")
            
            # Step 1: Parse resume
            logger.info("Parsing resume file...")
            resume_data = self._parse_file(resume_path, "resume")
            
            # Step 2: Parse job description
            logger.info("Parsing job description...")
            job_desc = self._parse_file(job_desc_path, "job_description")
            
            # Step 3: Tailor resume
            logger.info("Tailoring resume with AI...")
            results = self.agent.tailor_resume(resume_data, job_desc, guidelines)
            
            # Step 4: Generate cover letter if job details provided
            if job_title and company:
                logger.info("Generating cover letter...")
                cover_letter = self.agent.generate_cover_letter_template(
                    job_title, company, resume_data, job_desc
                )
                results['cover_letter'] = cover_letter
            
            # Step 5: Save outputs
            logger.info("Saving outputs...")
            output_files = self._save_outputs(results, output_dir, resume_path, job_title, company)
            
            # Step 6: Generate workflow report
            workflow_report = self._generate_workflow_report(
                resume_data, job_desc, results, output_files
            )
            
            # Store workflow history
            self.workflow_history.append({
                'timestamp': self._get_timestamp(),
                'resume_file': resume_path,
                'job_desc_file': job_desc_path,
                'results': results,
                'output_files': output_files,
                'workflow_report': workflow_report
            })
            
            logger.info("Workflow completed successfully!")
            return {
                'results': results,
                'output_files': output_files,
                'workflow_report': workflow_report
            }
            
        except Exception as e:
            logger.error(f"Workflow failed: {str(e)}")
            raise
    
    def _parse_file(self, file_path: str, file_type: str) -> ResumeData | JobDescription:
        """Parse file based on type"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine file type from extension
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.txt':
            mime_type = 'text/plain'
        elif file_ext == '.pdf':
            mime_type = 'application/pdf'
        elif file_ext == '.docx':
            mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        else:
            raise ValueError(f"Unsupported file extension: {file_ext}")
        
        # Read file content
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Parse based on file type
        if file_type == "resume":
            return self.agent.parse_resume_file(file_content, mime_type)
        elif file_type == "job_description":
            return self.agent.parse_job_description(file_content, mime_type)
        else:
            raise ValueError(f"Invalid file type: {file_type}")
    
    def _save_outputs(self, results: Dict[str, str], output_dir: str, 
                      resume_path: str, job_title: str, company: str) -> Dict[str, str]:
        """Save all outputs to files"""
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate base filename
        base_name = Path(resume_path).stem
        if job_title:
            base_name += f"_{job_title.replace(' ', '_')}"
        
        output_files = {}
        
        # Save tailored resume
        if results.get('tailored_resume'):
            resume_file = os.path.join(output_dir, f"{base_name}_tailored.txt")
            with open(resume_file, 'w', encoding='utf-8') as f:
                f.write(results['tailored_resume'])
            output_files['tailored_resume'] = resume_file
        
        # Save cover letter
        if results.get('cover_letter'):
            cover_file = os.path.join(output_dir, f"{base_name}_cover_letter.txt")
            with open(cover_file, 'w', encoding='utf-8') as f:
                f.write(results['cover_letter'])
            output_files['cover_letter'] = cover_file
        
        # Save changes summary
        if results.get('changes_summary'):
            changes_file = os.path.join(output_dir, f"{base_name}_changes.txt")
            with open(changes_file, 'w', encoding='utf-8') as f:
                f.write(results['changes_summary'])
            output_files['changes_summary'] = changes_file
        
        # Save recommendations
        if results.get('recommendations'):
            rec_file = os.path.join(output_dir, f"{base_name}_recommendations.txt")
            with open(rec_file, 'w', encoding='utf-8') as f:
                f.write(results['recommendations'])
            output_files['recommendations'] = rec_file
        
        # Save complete workflow report
        workflow_file = os.path.join(output_dir, f"{base_name}_workflow_report.txt")
        with open(workflow_file, 'w', encoding='utf-8') as f:
            f.write(f"Resume Tailoring Workflow Report\n")
            f.write(f"Generated: {self._get_timestamp()}\n")
            f.write(f"Original Resume: {resume_path}\n")
            if job_title:
                f.write(f"Job Title: {job_title}\n")
            if company:
                f.write(f"Company: {company}\n")
            f.write(f"\n{'='*50}\n\n")
            
            for key, value in results.items():
                f.write(f"{key.upper().replace('_', ' ')}:\n")
                f.write(f"{value}\n\n")
                f.write(f"{'='*50}\n\n")
        
        output_files['workflow_report'] = workflow_file
        
        return output_files
    
    def _generate_workflow_report(self, resume_data: ResumeData, 
                                 job_desc: JobDescription, 
                                 results: Dict[str, str],
                                 output_files: Dict[str, str]) -> str:
        """Generate a comprehensive workflow report"""
        report = f"""
RESUME TAILORING WORKFLOW REPORT
{'='*50}

ORIGINAL RESUME ANALYSIS:
- Word Count: {resume_data.word_count}
- Estimated Pages: {resume_data.page_estimate:.1f}
- Sections Detected: {', '.join(resume_data.sections.keys())}

JOB DESCRIPTION ANALYSIS:
- Keywords Found: {len(job_desc.keywords)}
- Requirements Identified: {len(job_desc.requirements)}
- Responsibilities Listed: {len(job_desc.responsibilities)}

AI PROCESSING RESULTS:
- Resume Tailored: {'Yes' if results.get('tailored_resume') else 'No'}
- Cover Letter Generated: {'Yes' if results.get('cover_letter') else 'No'}
- Changes Documented: {'Yes' if results.get('changes_summary') else 'No'}
- Recommendations Provided: {'Yes' if results.get('recommendations') else 'No'}

OUTPUT FILES GENERATED:
"""
        
        for file_type, file_path in output_files.items():
            report += f"- {file_type}: {file_path}\n"
        
        report += f"\nWorkflow completed at: {self._get_timestamp()}"
        
        return report
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_workflow_history(self) -> List[Dict]:
        """Get workflow execution history"""
        return self.workflow_history
    
    def analyze_keyword_match(self, resume_data: ResumeData, 
                             job_desc: JobDescription) -> Dict[str, float]:
        """Analyze keyword matching between resume and job description"""
        resume_words = set(resume_data.text.lower().split())
        job_keywords = set(job_desc.keywords)
        
        # Calculate match percentages
        total_keywords = len(job_keywords)
        if total_keywords == 0:
            return {'match_percentage': 0.0, 'matched_keywords': [], 'missing_keywords': []}
        
        matched_keywords = resume_words.intersection(job_keywords)
        missing_keywords = job_keywords - resume_words
        
        match_percentage = (len(matched_keywords) / total_keywords) * 100
        
        return {
            'match_percentage': match_percentage,
            'matched_keywords': list(matched_keywords),
            'missing_keywords': list(missing_keywords),
            'total_keywords': total_keywords
        }
    
    def validate_resume_length(self, resume_text: str, target_words: int = 300) -> Dict[str, any]:
        """Validate if resume meets length requirements"""
        word_count = len(resume_text.split())
        page_estimate = word_count / 250  # Rough estimate
        
        return {
            'word_count': word_count,
            'page_estimate': page_estimate,
            'within_limit': word_count <= target_words,
            'words_over_limit': max(0, word_count - target_words),
            'recommendation': self._get_length_recommendation(word_count, target_words)
        }
    
    def _get_length_recommendation(self, current_words: int, target_words: int) -> str:
        """Get recommendation based on current word count"""
        if current_words <= target_words:
            return "Resume length is within acceptable limits."
        elif current_words <= target_words * 1.2:
            return "Resume is slightly over the limit. Consider condensing some bullet points."
        else:
            return "Resume is significantly over the limit. Focus on most relevant experience and achievements."

# Example usage
def main():
    """Example usage of the orchestrator"""
    orchestrator = ResumeTailorOrchestrator()
    
    print("Resume Tailor Orchestrator")
    print("=" * 50)
    print("This orchestrator provides:")
    print("1. Complete workflow management")
    print("2. File parsing and analysis")
    print("3. AI-powered resume tailoring")
    print("4. Output file management")
    print("5. Workflow reporting and analytics")
    print("\nUse it to automate the entire resume tailoring process.")

if __name__ == "__main__":
    main()
