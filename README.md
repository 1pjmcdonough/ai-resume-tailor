# 🤖 AI Resume Tailor

An intelligent AI agent that automatically tailors your resume to match job descriptions and generates personalized cover letters. Built with Python and powered by Grok AI.

## ✨ Features

- **📄 Smart Resume Parsing**: Automatically extracts content from PDF, DOCX, and TXT files
- **🔍 Job Description Analysis**: Identifies key requirements, skills, and responsibilities
- **🎯 AI-Powered Tailoring**: Uses advanced AI to optimize resume content for specific jobs
- **✉️ Cover Letter Generation**: Creates personalized cover letters based on resume and job description
- **📏 Length Management**: Ensures resumes stay within 1-page limit
- **🔑 Keyword Optimization**: Maximizes alignment with job requirements
- **📊 Analytics**: Provides detailed analysis of keyword matching and content optimization
- **💾 Multiple Output Formats**: Saves results in organized, downloadable formats

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Grok AI API key
- Resume file (PDF, DOCX, or TXT)
- Job description file (PDF, DOCX, or TXT)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-resume-tailor.git
   cd ai-resume-tailor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp config/env.example .env.txt
   # Edit .env.txt and add your Grok AI API key
   echo "XAI_API_KEY=your_api_key_here" > .env.txt
   ```

### Usage

#### 🌐 Web Interface (Recommended)

Launch the Streamlit web app:

```bash
streamlit run src/ui.py
```

Open your browser and navigate to `http://localhost:8501`

#### 💻 Command Line Interface

For automation and scripting:

```bash
# Basic usage
python src/cli.py --resume my_resume.pdf --job-desc job_description.pdf

# With custom guidelines
python src/cli.py --resume resume.docx --job-desc job.txt \
  --guidelines "Focus on technical skills and leadership experience" \
  --output-dir ./results

# Generate cover letter with job details
python src/cli.py --resume resume.pdf --job-desc job.pdf \
  --job-title "Senior Software Engineer" \
  --company "Tech Corp Inc."

# Analyze files without AI processing
python src/cli.py --resume resume.pdf --job-desc job.pdf --analyze-only
```

#### 🔧 Python API

```python
from src.tailor_resume import TailorResume
from src.orchestrator import ResumeTailorOrchestrator

# Initialize the AI agent
agent = TailorResume()

# Parse files
resume_data = agent.parse_resume_file(resume_content, "application/pdf")
job_desc = agent.parse_job_description(job_content, "application/pdf")

# Tailor resume
results = agent.tailor_resume(resume_data, job_desc, "Focus on technical skills")

# Or use the orchestrator for complete workflow
orchestrator = ResumeTailorOrchestrator()
results = orchestrator.run_complete_workflow(
    "resume.pdf", 
    "job.pdf", 
    output_dir="./output",
    guidelines="Custom guidelines here"
)
```

## 🏗️ Architecture

### Core Components

1. **`TailorResume`** (`src/tailor_resume.py`)
   - AI-powered resume analysis and tailoring
   - Cover letter generation
   - Content optimization algorithms

2. **`ResumeTailorOrchestrator`** (`src/orchestrator.py`)
   - Workflow coordination
   - File management
   - Output generation and reporting

3. **Web Interface** (`src/ui.py`)
   - Streamlit-based user interface
   - File upload and configuration
   - Results visualization

4. **CLI Interface** (`src/cli.py`)
   - Command-line automation
   - Batch processing capabilities
   - Scripting integration

### Data Structures

- **`ResumeData`**: Parsed resume content with sections and metadata
- **`JobDescription`**: Extracted job requirements and keywords
- **`TailoringResults`**: AI-generated outputs and recommendations

## 📋 System Prompts

The AI agent uses carefully crafted system prompts to ensure:

- **Professional Standards**: Industry-best practices for resume writing
- **ATS Compatibility**: Optimized for Applicant Tracking Systems
- **Content Truthfulness**: All modifications are verifiable and honest
- **Keyword Optimization**: Strategic placement of relevant skills and experience
- **Length Management**: Automatic 1-page limit enforcement

## 🔧 Configuration

### Environment Variables

```bash
# Required
XAI_API_KEY=your_grok_api_key_here

# Optional
GROK_BASE_URL=https://api.x.ai/v1
AI_MODEL=grok-4-0709
```

### Custom Guidelines

You can provide specific instructions for resume tailoring:

- Focus areas (technical skills, leadership, etc.)
- Industry-specific requirements
- Company culture considerations
- Format preferences

## 📊 Output Analysis

The system provides comprehensive analytics:

- **Keyword Matching**: Percentage of job requirements covered
- **Content Optimization**: Before/after analysis
- **Length Validation**: Page count and word limit compliance
- **Section Analysis**: Resume structure and content distribution
- **Recommendations**: Improvement suggestions and best practices

## 🚀 Advanced Features

### Batch Processing

```bash
# Process multiple resumes
for resume in resumes/*.pdf; do
  python src/cli.py --resume "$resume" --job-desc job.pdf --output-dir ./batch_output
done
```

### Custom AI Models

```python
# Use different AI models
agent = TailorResume(model="grok-beta")
orchestrator = ResumeTailorOrchestrator(model="grok-1")
```

### Workflow Automation

```python
# Integrate with existing systems
orchestrator = ResumeTailorOrchestrator()
workflow_history = orchestrator.get_workflow_history()

# Analyze keyword trends
keyword_analysis = orchestrator.analyze_keyword_match(resume_data, job_desc)
```

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or test individual components:

```bash
python src/tailor_resume.py
python src/orchestrator.py
python src/cli.py --help
```

## 📁 Project Structure

```
ai-resume-tailor/
├── src/
│   ├── tailor_resume.py      # Core AI agent
│   ├── orchestrator.py       # Workflow management
│   ├── ui.py                 # Streamlit web interface
│   └── cli.py               # Command-line interface
├── config/
│   └── env.example          # Environment configuration
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run code formatting
black src/ tests/

# Run linting
flake8 src/ tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the web interface
- Powered by [Grok AI](https://x.ai/) for intelligent content generation
- Uses [PyPDF2](https://pypdf2.readthedocs.io/) and [python-docx](https://python-docx.readthedocs.io/) for document parsing

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-resume-tailor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-resume-tailor/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/ai-resume-tailor/wiki)

---

**Made with ❤️ by the AI Resume Tailor team**
