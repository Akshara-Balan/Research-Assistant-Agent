# tasks/research_task.py
from crewai import Task
from agents.researcher import get_researcher
import logging
import os

# Ensure logs directory exists
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_research_task(topic: str, year: int = 2024, num_papers: int = 5) -> Task:
    """
    Create a research task to find and summarize top papers on a given topic.
    
    Args:
        topic (str): Research topic (e.g., "LLM alignment").
        year (int): Year of publication to filter (default: 2024).
        num_papers (int): Number of papers to retrieve (default: 5).
    
    Returns:
        Task: Configured CrewAI task object.
    """
    task = Task(
        description=(
            f"Research the top {num_papers} research papers published in {year} "
            f"about '{topic}'. Provide a concise summary including title, authors, "
            f"and key findings for each paper."
        ),
        expected_output=(
            f"A list of {num_papers} papers with title, authors, and a summary of each."
        ),
        agent=get_researcher(),
        output_file=f"outputs/{topic.replace(' ', '_')}_{year}_summary.txt"
    )
    logging.info(f"Created task for topic: {topic}, year: {year}, papers: {num_papers}")
    return task