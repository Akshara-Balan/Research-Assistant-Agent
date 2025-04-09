# tasks/review_task.py
from crewai import Task
from agents.reviewer import get_reviewer
import logging
import os
from utils.ollama_wrapper import ollama_completion

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_review_task(topic: str, research_task: Task) -> Task:
    description = (
        f"Review and categorize the following summarized research papers on '{topic}' "
        f"for relevance and subdomain (e.g., NLP, CV, Other). Provide a brief assessment:\n"
        f"{research_task.expected_output}"
    )
    # Execute Ollama directly
    review = ollama_completion(description)
    expected_output = review

    task = Task(
        description=description,
        expected_output=expected_output,
        agent=get_reviewer(topic),
        output_file=f"outputs/{topic.replace(' ', '_')}_review.txt"
    )
    logging.info(f"Created review task for topic: {topic}")
    return task