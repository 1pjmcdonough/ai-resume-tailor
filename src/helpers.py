"""
Helper utilities for the AI resume tailoring application.
"""

from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import os

dotenv_path = Path( Path(__file__).parent.parent, ".env" )
load_dotenv(dotenv_path=dotenv_path)


@dataclass
class Prompt:
    """Data class representing a prompt pair for AI model interactions."""
    sys_prompt: str  # System prompt that defines the AI's role and behavior
    usr_prompt: str  # User prompt containing the specific request


@dataclass
class UserInfo:
    """Data class containing user input for resume tailoring."""
    resume: str  # The user's resume content
    job_desc: str  # The job description to tailor the resume for
    model: str  # The AI model to use
    usr_context: str  # Additional user context or instructions


class Model(Enum):
    """Enumeration of supported AI models for resume tailoring."""
    GROK4 = "grok-4-0709"
    GPT4o = "gpt-4o-mini"


def set_client(model: str) -> OpenAI:
    """
    Creates and returns an OpenAI-compatible client configured for the specified model.
    
    Args:
        model: The model identifier (must match a Model enum value)
        
    Returns:
        OpenAI: Configured client instance for the specified model
    """
    if model == Model.GROK4.value:
        return OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
    elif model == Model.GPT4o.value:
        return OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1"
        )


def parse_url(url):
    #TODO
    return
    """
    Fetches and parses the job description from a LinkedIn job posting URL.
    
    Args:
        url (str): The LinkedIn job posting URL.
        
    Returns:
        str or None: The extracted job description text, or None if not found.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all <p dir="ltr"> elements and extract their text
    # Remove the element with class "top-level-modal-container" if it exists
    modal = soup.find(class_="top-level-modal-container")
    if modal:
        modal.decompose()
    p = soup.find('p', dir='ltr')
    job_description = p.get_text(separator='\n', strip=True) if p else None

    if job_description:
        print("Job Description Found:")
        print("=" * 80)
        print(job_description)
    return job_description