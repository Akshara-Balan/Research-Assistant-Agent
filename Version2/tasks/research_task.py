# tasks/research_task.py
from crewai import Task
from agents.researcher import get_researcher
import logging
import os
import requests
from datetime import datetime

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_serpapi_papers(topic: str, start_year: int = datetime.now().year, max_papers: int = 5) -> list:
    """Fetch real, relevant papers from Google Scholar via SerpAPI, from start_year downward."""
    api_key = "YOUR_SERAPI_KEY"  # Your SerpAPI key
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_scholar",
        "q": topic,  # No year in query to allow broader search
        "api_key": api_key,
        "num": max_papers * 2,  # Fetch extra to filter by year and relevance
        "as_ylo": start_year - 5,  # Look back 5 years from current year (e.g., 2020-2025)
        "as_yhi": start_year,     # Up to current year
        "sort": "pubdate"         # Sort by publication date (newest first)
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        papers = []
        topic_terms = topic.lower().split()  # Split topic for relevance check
        for result in data.get("organic_results", []):
            if len(papers) >= max_papers:
                break
            title = result.get("title", "No Title")
            authors = result.get("publication_info", {}).get("authors", ["Unknown"])
            summary = result.get("snippet", "No abstract available")
            pub_year = result.get("publication_info", {}).get("summary", "").split(" - ")[0] if " - " in result.get("publication_info", {}).get("summary", "") else str(start_year)
            try:
                pub_year = int(pub_year)
            except ValueError:
                pub_year = start_year  # Default to current year if parsing fails
            # Ensure relevance: at least one topic term in title or summary
            if any(term in title.lower() or term in summary.lower() for term in topic_terms):
                papers.append({
                    "title": title,
                    "authors": [a["name"] for a in authors] if authors else ["Unknown"],
                    "summary": summary,
                    "year": pub_year
                })
        # Sort by year in reverse chronological order
        papers.sort(key=lambda x: x["year"], reverse=True)
        logging.info(f"Fetched {len(papers)} relevant papers from SerpAPI for topic: {topic}, years: {min(p['year'] for p in papers)}-{max(p['year'] for p in papers)}")
        return papers
    except Exception as e:
        logging.error(f"Failed to fetch SerpAPI papers: {str(e)}")
        return []

def create_research_task(topic: str, start_year: int = datetime.now().year, max_papers: int = 5) -> Task:
    """Create a task with real, relevant papers in reverse chronological order."""
    papers = fetch_serpapi_papers(topic, start_year, max_papers)
    if papers:
        description = (
            f"Summarize the following {len(papers)} research paper{'s' if len(papers) != 1 else ''} "
            f"related to '{topic}' from Google Scholar, listed in reverse chronological order. "
            f"For each paper, include specific methods, results, or key findings from the abstract:\n"
            + "\n".join([f"- {p['title']} ({p['year']}) by {', '.join(p['authors'])}: {p['summary']}" 
                        for p in papers])
        )
        expected_output = f"A list of {len(papers)} relevant papers with title, year, authors, and a detailed summary of each, sorted newest to oldest."
    else:
        description = (
            f"No relevant research papers were found for '{topic}' on Google Scholar from {start_year - 5} to {start_year}. "
            f"Please try a different topic or broaden your search terms."
        )
        expected_output = "A message indicating no relevant papers were found."
    
    task = Task(
        description=description,
        expected_output=expected_output,
        agent=get_researcher(topic),
        output_file=f"outputs/{topic.replace(' ', '_')}_{start_year}_summary.txt"
    )
    logging.info(f"Created task for topic: {topic}, year range: {start_year - 5}-{start_year}, found papers: {len(papers)}")
    return task