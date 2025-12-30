# 🤖 AI Job Tailor

**Struggling to land interviews?**

Let the AI Job Tailor supercharge your application by tailoring your resume to match a job description and generating a personalized cover letter.

## Features

- **Automatic Resume Parsing**: Extracts resume content from PDF, DOCX, or TXT files
- **Job Description Extraction**: Analyzes job descriptions to find important skills, requirements, and responsibilities
- **AI Resume Tailoring**: Uses AI models to optimize your resume for specific job descriptions
- **Personalized Cover Letter Generation**: Produces custom cover letters based on your resume and job description
- **Organized Downloadable Results**: Saves tailored resumes and cover letters in easily downloadable formats

## 🚀 Quick Start

1. **Clone the repository and change to the root directory**
   ```bash
   git clone https://github.com/1pjmcdonough/ai-resume-tailor.git
   cd ai-resume-tailor
   ```
2. **Create and activate a virtual environment**
   ```bash
   conda create -n job_tailor python=3.11.7
   conda activate job_tailor
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env # Edit .env and add your API keys
   ```

5. **Launch the Streamlit web app**
   ```bash
   python -m streamlit run src/homepage.py
   ```

### Note: Custom Guidelines

You can provide specific instructions for resume tailoring:

- Focus areas (technical skills, leadership, etc.)
- Industry-specific requirements
- Company culture considerations
- Format preferences
- Etc.