# agents/reviewer.py
from crewai import Agent
import logging
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_reviewer(topic: str) -> Agent:
    reviewer = Agent(
        role="Paper Reviewer",
        goal=f"Categorize and review research papers on '{topic}' for relevance and subdomain",
        backstory=(
            "A meticulous reviewer with expertise in academic analysis, capable of "
            "categorizing papers by subdomain (e.g., NLP, CV) and assessing their quality."
        ),
        allow_delegation=False,
        verbose=True,
    )
    logging.info(f"Reviewer agent initialized for topic: {topic}")
    return reviewer