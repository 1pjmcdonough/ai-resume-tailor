import sys
import requests
from bs4 import BeautifulSoup


# Parse the LinkedIn job posting URL
url = "https://www.linkedin.com/jobs/view/financial-analyst-residuals-at-netflix-4348383902?trk=public_jobs_topcard-title"
# url = "https://www.linkedin.com/jobs/view/valuation-analyst-at-the-equus-group-4341732808?position=10&pageNum=0&refId=AHWTjbGF1fllPHdkc%2FTLZg%3D%3D&trackingId=0L06k17JGJ3dHBi4dRdR2Q%3D%3D"
def parse_url(url):
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

parse_url(url)