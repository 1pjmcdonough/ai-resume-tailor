with open("prompts/cover_letter_template.txt", "r") as f:
    cover_letter_template = f.read()

with open("prompts/system_prompt.txt", "r") as f:
    system_prompt = f.read()


sys_template = f"""
Blah blah blah

{cover_letter_template}

other stuff
"""

user_prompt = f"""
TASK: Tailor the following resume to match the job description and create a cover letter.

RESUME CONTENT:
{resume_data.text}

JOB DESCRIPTION:
{job_desc.text}

KEYWORDS TO INCORPORATE:
{', '.join(job_desc.keywords)}

JOB REQUIREMENTS:
{chr(10).join(f'- {req}' for req in job_desc.requirements)}

JOB RESPONSIBILITIES:
{chr(10).join(f'- {resp}' for resp in job_desc.responsibilities)}

CURRENT STATS:
- Word count: {resume_data.word_count}
- Estimated pages: {resume_data.page_estimate:.1f}

ADDITIONAL GUIDELINES:
{guidelines if guidelines else 'Focus on highlighting relevant experience and skills that match the job requirements. Ensure the resume stays within 1 page.'}

REQUIRED OUTPUT FORMAT:
1. TAILORED RESUME: Provide the complete tailored resume text
2. COVER LETTER: Generate a compelling cover letter
3. CHANGES SUMMARY: List key modifications made
4. WORD COUNT: Final word count and page estimate
5. RECOMMENDATIONS: Any additional suggestions for improvement

IMPORTANT: Ensure the final resume is under 1 page (approximately 250-300 words) and maximizes keyword alignment with the job description.
"""

########Cover Letter Template########

user_prompt = f"""
Generate a professional cover letter template for the following position:

JOB TITLE: {job_title}
COMPANY: {company}

CANDIDATE BACKGROUND (from resume):
{resume_data.text[:500]}...

JOB DESCRIPTION:
{job_desc.text[:500]}...

REQUIREMENTS:
{chr(10).join(f'- {req}' for req in job_desc.requirements[:5])}

Please create a compelling cover letter that:
1. Opens with a strong hook
2. Highlights relevant experience from the resume
3. Shows understanding of the role and company
4. Includes specific examples of achievements
5. Closes with a call to action
6. Maintains professional tone throughout

Format the letter with proper business letter structure.
"""