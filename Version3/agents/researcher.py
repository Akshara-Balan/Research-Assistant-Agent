# agents/researcher.py
from crewai import Agent
import logging
import os
from datetime import datetime
from utils.ollama_wrapper import ollama_llm

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_researcher(topic: str) -> Agent:
    current_year = datetime.now().year
    researcher = Agent(
        role="Research Analyst",
        goal=f"Identify and summarize the latest research papers on '{topic}' from {current_year} downward",
        backstory=(
            "An expert analyst with a PhD in computational linguistics, skilled in "
            "extracting academic insights from diverse sources across all domains "
            "and presenting them clearly."
        ),
        allow_delegation=False,
        llm=ollama_llm,  # Direct Ollama LLM
        verbose=True,
    )
    logging.info(f"Researcher agent initialized for topic: {topic}, year range: {current_year - 5}-{current_year}")
    return researcher