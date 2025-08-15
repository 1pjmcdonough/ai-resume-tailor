#!/usr/bin/env python3
"""
Basic usage example for the AI Resume Tailor system
"""
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from tailor_resume import TailorResume, ResumeData, JobDescription
from orchestrator import ResumeTailorOrchestrator

def create_sample_resume() -> str:
    """Create a sample resume text for demonstration"""
    return """
JOHN DOE
Software Engineer
john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe

SUMMARY
Experienced software engineer with 5+ years developing scalable web applications using Python, JavaScript, and cloud technologies. Proven track record of leading development teams and delivering high-quality software solutions.

EXPERIENCE
Senior Software Engineer | Tech Solutions Inc. | 2021-Present
• Led development of microservices architecture serving 100K+ users
• Implemented CI/CD pipelines reducing deployment time by 60%
• Mentored 3 junior developers and conducted code reviews
• Technologies: Python, Django, React, AWS, Docker, Kubernetes

Software Engineer | StartupXYZ | 2019-2021
• Developed RESTful APIs and frontend components for SaaS platform
• Collaborated with product team to define requirements and user stories
• Participated in agile development process with 2-week sprints
• Technologies: Python, Flask, JavaScript, PostgreSQL, Redis

EDUCATION
Bachelor of Science in Computer Science | University of Technology | 2019
• GPA: 3.8/4.0
• Relevant coursework: Data Structures, Algorithms, Software Engineering

SKILLS
Programming Languages: Python, JavaScript, Java, SQL
Frameworks: Django, Flask, React, Node.js
Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins
Databases: PostgreSQL, MongoDB, Redis
Tools: Git, JIRA, VS Code, Postman
"""

def create_sample_job_description() -> str:
    """Create a sample job description for demonstration"""
    return """
SENIOR SOFTWARE ENGINEER - FULL STACK
TechCorp Industries

About the Role:
We are seeking a Senior Software Engineer to join our growing development team. You will be responsible for designing, developing, and maintaining scalable web applications that serve millions of users worldwide.

Key Responsibilities:
• Design and implement scalable microservices architecture
• Develop and maintain RESTful APIs and frontend applications
• Collaborate with cross-functional teams to define requirements
• Lead technical initiatives and mentor junior developers
• Implement CI/CD pipelines and DevOps best practices
• Optimize application performance and ensure high availability

Required Qualifications:
• 5+ years of software development experience
• Strong proficiency in Python and JavaScript
• Experience with modern web frameworks (Django, React)
• Knowledge of cloud platforms (AWS, Azure, or GCP)
• Experience with containerization (Docker, Kubernetes)
• Understanding of database design and optimization
• Familiarity with agile development methodologies

Preferred Skills:
• Experience with microservices architecture
• Knowledge of CI/CD tools and practices
• Understanding of distributed systems
• Experience with monitoring and logging tools
• Knowledge of security best practices

What We Offer:
• Competitive salary and benefits
• Remote work opportunities
• Professional development and training
• Collaborative and innovative work environment
"""

def main():
    """Main demonstration function"""
    print("🤖 AI Resume Tailor - Basic Usage Example")
    print("=" * 50)
    
    try:
        # Initialize the AI agent
        print("🚀 Initializing AI agent...")
        agent = TailorResume()
        print("✅ AI agent initialized successfully!")
        
        # Create sample data
        print("\n📄 Creating sample resume and job description...")
        sample_resume = create_sample_resume()
        sample_job_desc = create_sample_job_description()
        
        # Parse the sample data
        print("🔍 Parsing sample data...")
        
        # For demonstration, we'll create ResumeData and JobDescription objects directly
        # In real usage, you'd use agent.parse_resume_file() and agent.parse_job_description()
        
        resume_data = ResumeData(
            text=sample_resume,
            sections={
                'summary': 'Experienced software engineer with 5+ years developing scalable web applications...',
                'experience': 'Senior Software Engineer at Tech Solutions Inc., Software Engineer at StartupXYZ...',
                'education': 'Bachelor of Science in Computer Science from University of Technology...',
                'skills': 'Python, JavaScript, Java, SQL, Django, Flask, React, Node.js, AWS, Docker, Kubernetes...'
            },
            word_count=len(sample_resume.split()),
            page_estimate=len(sample_resume.split()) / 250
        )
        
        job_desc = JobDescription(
            text=sample_job_desc,
            keywords=['python', 'javascript', 'django', 'react', 'aws', 'docker', 'kubernetes', 'microservices', 'ci/cd'],
            requirements=['5+ years experience', 'Python proficiency', 'JavaScript knowledge', 'Django experience', 'React experience', 'AWS knowledge', 'Docker experience', 'Kubernetes knowledge'],
            responsibilities=['Design microservices', 'Develop APIs', 'Collaborate with teams', 'Lead initiatives', 'Mentor developers', 'Implement CI/CD', 'Optimize performance']
        )
        
        print(f"✅ Resume parsed: {resume_data.word_count} words, {resume_data.page_estimate:.1f} pages")
        print(f"✅ Job description parsed: {len(job_desc.keywords)} keywords, {len(job_desc.requirements)} requirements")
        
        # Analyze keyword matching
        print("\n🔑 Analyzing keyword matching...")
        orchestrator = ResumeTailorOrchestrator()
        keyword_analysis = orchestrator.analyze_keyword_match(resume_data, job_desc)
        
        print(f"📊 Keyword Match Analysis:")
        print(f"   - Match Percentage: {keyword_analysis['match_percentage']:.1f}%")
        print(f"   - Matched Keywords: {', '.join(keyword_analysis['matched_keywords'])}")
        if keyword_analysis['missing_keywords']:
            print(f"   - Missing Keywords: {', '.join(keyword_analysis['missing_keywords'])}")
        
        # Demonstrate resume tailoring (without actual AI call for demo)
        print("\n🎯 Resume Tailoring Analysis:")
        print("   - Current resume length: Within acceptable limits")
        print("   - Keywords to emphasize: microservices, CI/CD, leadership")
        print("   - Areas for improvement: Add specific metrics, highlight team leadership")
        
        # Show what the AI would do
        print("\n🤖 AI Tailoring Recommendations:")
        print("   1. Emphasize microservices architecture experience")
        print("   2. Highlight CI/CD pipeline implementation")
        print("   3. Add specific metrics (100K+ users, 60% improvement)")
        print("   4. Strengthen leadership and mentoring sections")
        print("   5. Ensure 1-page limit compliance")
        
        print("\n📝 Cover Letter Focus Areas:")
        print("   1. Opening with microservices expertise")
        print("   2. Highlighting team leadership experience")
        print("   3. Demonstrating scalability knowledge")
        print("   4. Showing passion for modern development practices")
        
        print("\n🎉 Example completed successfully!")
        print("\n💡 To use with real files and AI processing:")
        print("   python src/cli.py --resume your_resume.pdf --job-desc job.pdf")
        print("   streamlit run src/ui.py")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Make sure you have:")
        print("   1. Set up your .env.txt file with XAI_API_KEY")
        print("   2. Installed all requirements: pip install -r requirements.txt")
        print("   3. Valid Grok AI API credentials")

if __name__ == "__main__":
    main()
