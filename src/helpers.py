from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ResumeData:
    """Data structure for parsed resume content"""
    text: str
    sections: Dict[str, str]
    word_count: int
    page_estimate: float

@dataclass
class JobDescription:
    """Data structure for parsed job description"""
    text: str
    keywords: List[str]
    requirements: List[str]
    responsibilities: List[str]

