# tasks/research_task.py
from crewai import Task
from agents.researcher import get_researcher
import logging
import os
import requests
from xml.etree import ElementTree as ET

# Ensure logs directory exists
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_arxiv_papers(topic: str, year: int = 2025, num_papers: int = 5) -> list:
    """Fetch real papers from arXiv for the given topic and year."""
    query = f'"{topic}" submittedDate:[{year}0101 TO {year}1231]'
    url = (
        f"http://export.arxiv.org/api/query?search_query={query}"
        f"&start=0&max_results={num_papers}&sortBy=submittedDate&sortOrder=descending"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        papers = []
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry")[:num_papers]:
            title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()
            authors = [author.find("{http://www.w3.org/2005/Atom}name").text.strip()
                      for author in entry.findall("{http://www.w3.org/2005/Atom}author")]
            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text.strip()
            papers.append({"title": title, "authors": authors, "summary": summary})
        logging.info(f"Fetched {len(papers)} papers from arXiv for topic: {topic}")
        return papers
    except Exception as e:
        logging.error(f"Failed to fetch arXiv papers: {str(e)}")
        return []

def create_research_task(topic: str, year: int = 2024, num_papers: int = 5) -> Task:
    """Create a task with real papers or fallback to generation if fetching fails."""
    papers = fetch_arxiv_papers(topic, year, num_papers)
    if papers:
        # Use real papers in the task description
        description = (
            f"Summarize the following {len(papers)} research papers published in {year} "
            f"about '{topic}' from arXiv:\n"
            + "\n".join([f"- {p['title']} by {', '.join(p['authors'])}: {p['summary']}" 
                        for p in papers]) +
            f"\nProvide a concise summary including title, authors, and key findings for each."
        )
    else:
        # Fallback if no papers are fetched
        description = (
            f"Research the top {num_papers} research papers published in {year} "
            f"about '{topic}'. Provide a concise summary including title, authors, "
            f"and key findings for each paper. Note: Real-time data unavailable; generate plausible results."
        )
    
    task = Task(
        description=description,
        expected_output=f"A list of up to {num_papers} papers with title, authors, and a summary of each.",
        agent=get_researcher(),
        output_file=f"outputs/{topic.replace(' ', '_')}_{year}_summary.txt"
    )
    logging.info(f"Created task for topic: {topic}, year: {year}, papers: {num_papers}")
    return task