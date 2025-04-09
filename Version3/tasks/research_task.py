# tasks/research_task.py
from crewai import Task
from agents.researcher import get_researcher
import logging
import os
import requests
from datetime import datetime
from utils.ollama_wrapper import ollama_completion

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_serpapi_papers(topic: str, start_year: int = datetime.now().year, max_papers: int = 5) -> list:
    api_key = "e2401a14b790c9d4a8a5ddb30a18ea4aa9b757406302a392265544762ed2712d"
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_scholar",
        "q": topic,
        "api_key": api_key,
        "num": max_papers * 2,
        "as_ylo": start_year - 5,
        "as_yhi": start_year,
        "sort": "pubdate"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        logging.info(f"SerpAPI raw response for '{topic}': {data.get('organic_results', [])[:3]}")
        papers = []
        topic_terms = topic.lower().split()
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
                pub_year = start_year
            if any(term in title.lower() or term in summary.lower() for term in topic_terms):
                papers.append({
                    "title": title,
                    "authors": [a["name"] for a in authors] if authors else ["Unknown"],
                    "summary": summary,
                    "year": pub_year
                })
        papers.sort(key=lambda x: x["year"], reverse=True)
        logging.info(f"Fetched {len(papers)} relevant papers for topic: {topic}")
        return papers
    except Exception as e:
        logging.error(f"Failed to fetch SerpAPI papers: {str(e)}")
        return []

def create_research_task(topic: str, start_year: int = datetime.now().year, max_papers: int = 5) -> Task:
    papers = fetch_serpapi_papers(topic, start_year, max_papers)
    if papers:
        description = (
            f"Summarize the following {len(papers)} research paper{'s' if len(papers) != 1 else ''} "
            f"related to '{topic}' from Google Scholar, listed in reverse chronological order. "
            f"For each paper, include specific methods, results, or key findings from the abstract:\n"
            + "\n".join([f"- {p['title']} ({p['year']}) by {', '.join(p['authors'])}: {p['summary']}" 
                        for p in papers])
        )
        # Execute Ollama directly here
        summary = ollama_completion(description)
        expected_output = summary  # Use the result directly
    else:
        description = (
            f"No relevant research papers were found for '{topic}' on Google Scholar from {start_year - 5} to {start_year}. "
            f"Please try a different topic or broaden your search terms."
        )
        expected_output = description
    
    task = Task(
        description=description,
        expected_output=expected_output,
        agent=get_researcher(topic),
        output_file=f"outputs/{topic.replace(' ', '_')}_{start_year}_summary.txt"
    )
    logging.info(f"Created research task for topic: {topic}, year range: {start_year - 5}-{start_year}, found papers: {len(papers)}")
    return task