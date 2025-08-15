#!/usr/bin/env python3
"""
Command-line interface for the Resume Tailor AI Agent
"""
import argparse
import sys
import os
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tailor_resume import TailorResume, ResumeData, JobDescription
from orchestrator import ResumeTailorOrchestrator

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="AI Resume Tailor - Tailor your resume to match job descriptions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic resume tailoring
  python cli.py --resume my_resume.pdf --job-desc job_description.pdf
  
  # With custom guidelines and output directory
  python cli.py --resume resume.docx --job-desc job.txt --guidelines "Focus on technical skills" --output-dir ./results
  
  # Generate cover letter with job details
  python cli.py --resume resume.pdf --job-desc job.pdf --job-title "Software Engineer" --company "Tech Corp"
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--resume', '-r',
        required=True,
        help='Path to resume file (PDF, DOCX, or TXT)'
    )
    
    parser.add_argument(
        '--job-desc', '-j',
        required=True,
        help='Path to job description file (PDF, DOCX, or TXT)'
    )
    
    # Optional arguments
    parser.add_argument(
        '--output-dir', '-o',
        default='./output',
        help='Output directory for results (default: ./output)'
    )
    
    parser.add_argument(
        '--guidelines', '-g',
        default='',
        help='Custom guidelines for tailoring the resume'
    )
    
    parser.add_argument(
        '--job-title',
        help='Job title for cover letter generation'
    )
    
    parser.add_argument(
        '--company',
        help='Company name for cover letter generation'
    )
    
    parser.add_argument(
        '--model',
        default='grok-4-0709',
        choices=['grok-4-0709', 'grok-beta', 'grok-1'],
        help='AI model to use (default: grok-4-0709)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--analyze-only',
        action='store_true',
        help='Only analyze files without AI processing'
    )
    
    args = parser.parse_args()
    
    # Validate input files
    if not os.path.exists(args.resume):
        print(f"❌ Error: Resume file not found: {args.resume}")
        sys.exit(1)
    
    if not os.path.exists(args.job_desc):
        print(f"❌ Error: Job description file not found: {args.job_desc}")
        sys.exit(1)
    
    try:
        # Initialize the orchestrator
        print("🚀 Initializing AI Resume Tailor...")
        orchestrator = ResumeTailorOrchestrator(model=args.model)
        
        if args.verbose:
            print(f"✅ Using AI model: {args.model}")
            print(f"📁 Output directory: {args.output_dir}")
        
        # Run the workflow
        if args.analyze_only:
            print("\n📊 Analyzing files only...")
            results = orchestrator.run_complete_workflow(
                args.resume,
                args.job_desc,
                args.output_dir,
                args.guidelines,
                args.job_title or "",
                args.company or ""
            )
            
            # Display analysis results
            print("\n📋 ANALYSIS RESULTS:")
            print("=" * 50)
            
            # Resume analysis
            resume_data = orchestrator._parse_file(args.resume, "resume")
            print(f"📄 Resume Analysis:")
            print(f"   - Word Count: {resume_data.word_count}")
            print(f"   - Estimated Pages: {resume_data.page_estimate:.1f}")
            print(f"   - Sections: {', '.join(resume_data.sections.keys())}")
            
            # Job description analysis
            job_desc = orchestrator._parse_file(args.job_desc, "job_description")
            print(f"\n💼 Job Description Analysis:")
            print(f"   - Keywords Found: {len(job_desc.keywords)}")
            print(f"   - Requirements: {len(job_desc.requirements)}")
            print(f"   - Responsibilities: {len(job_desc.responsibilities)}")
            
            # Keyword matching analysis
            keyword_analysis = orchestrator.analyze_keyword_match(resume_data, job_desc)
            print(f"\n🔑 Keyword Matching:")
            print(f"   - Match Percentage: {keyword_analysis['match_percentage']:.1f}%")
            print(f"   - Matched Keywords: {', '.join(keyword_analysis['matched_keywords'][:10])}")
            if keyword_analysis['missing_keywords']:
                print(f"   - Missing Keywords: {', '.join(keyword_analysis['missing_keywords'][:10])}")
            
        else:
            print("\n🤖 Running complete AI workflow...")
            results = orchestrator.run_complete_workflow(
                args.resume,
                args.job_desc,
                args.output_dir,
                args.guidelines,
                args.job_title or "",
                args.company or ""
            )
            
            # Display results summary
            print("\n🎯 WORKFLOW COMPLETED!")
            print("=" * 50)
            
            if results['results'].get('tailored_resume'):
                print("✅ Resume tailored successfully")
                
                # Validate length
                length_validation = orchestrator.validate_resume_length(
                    results['results']['tailored_resume']
                )
                print(f"📏 Length: {length_validation['word_count']} words ({length_validation['page_estimate']:.1f} pages)")
                print(f"📋 Status: {'✅ Within limit' if length_validation['within_limit'] else '⚠️ Over limit'}")
                if not length_validation['within_limit']:
                    print(f"💡 Recommendation: {length_validation['recommendation']}")
            
            if results['results'].get('cover_letter'):
                print("✅ Cover letter generated")
            
            if results['results'].get('changes_summary'):
                print("✅ Changes documented")
            
            if results['results'].get('recommendations'):
                print("✅ Recommendations provided")
            
            # Show output files
            print(f"\n📁 Output files saved to: {args.output_dir}")
            for file_type, file_path in results['output_files'].items():
                print(f"   - {file_type}: {os.path.basename(file_path)}")
        
        print(f"\n🎉 Process completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
