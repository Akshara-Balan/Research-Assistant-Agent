from crewai import Task
from agents.researcher import get_researcher
import logging
import os
import requests
from xml.etree import ElementTree as ET
import spacy
import re
from datetime import datetime

# Setup logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def extract_topic_from_prompt(prompt: str) -> str:
    """Extract the most relevant noun phrase from the prompt."""
    doc = nlp(prompt)
    noun_phrases = [chunk.text.strip() for chunk in doc.noun_chunks if 2 <= len(chunk.text.split()) <= 6]
    return noun_phrases[0] if noun_phrases else prompt

def extract_year_from_prompt(prompt: str, default_year: int = None) -> int:
    """Extract a 4-digit year from the prompt, fallback to default or current year."""
    match = re.search(r"\b(20\d{2})\b", prompt)
    if match:
        return int(match.group(1))
    return default_year or datetime.now().year

def fetch_arxiv_papers(topic: str, year: int = 2025, num_papers: int = 5) -> list:
    """Fetch papers from arXiv using their API."""
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
            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text.strip().replace("\n", " ")
            papers.append({"title": title, "authors": authors, "summary": summary})
        logging.info(f"Fetched {len(papers)} papers from arXiv for topic: {topic}")
        return papers
    except Exception as e:
        logging.error(f"Failed to fetch arXiv papers: {str(e)}")
        return []

def create_research_task(prompt: str, year: int = None, num_papers: int = 5) -> Task:
    """Create a research task from a natural language prompt."""
    topic = extract_topic_from_prompt(prompt)
    year = extract_year_from_prompt(prompt, default_year=year or datetime.now().year)
    papers = fetch_arxiv_papers(topic, year, num_papers)

    if papers:
        bullet_points = "\n".join([
            f"- **{p['title']}** by {', '.join(p['authors'])}: {p['summary']}"
            for p in papers
        ])
        description = (
            f"Summarize the following {len(papers)} research papers published in {year} "
            f"about **{topic}** from arXiv:\n\n{bullet_points}\n\n"
            "Provide a concise summary including title, authors, and key findings for each."
        )
    else:
        description = (
            f"Research the top {num_papers} papers published in {year} about '{topic}'. "
            "Provide a concise summary including title, authors, and key findings. "
            "Note: Real-time data unavailable; generate plausible results."
        )

    output_filename = f"outputs/{topic.replace(' ', '_')}_{year}_summary.txt"

    task = Task(
        description=description,
        expected_output=f"A list of up to {num_papers} papers with title, authors, and a summary of each.",
        agent=get_researcher(topic),
        output_file=output_filename
    )

    logging.info(f"Created task for topic: {topic}, year: {year}, papers: {num_papers}")
    return task
