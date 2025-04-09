# agents/researcher.py
from crewai import Agent
from langchain_ollama import OllamaLLM
import logging
import os
from datetime import datetime

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

llm = OllamaLLM(model="ollama/llama3.2:latest")  # Or phi3:3.8b

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
        llm=llm,
        verbose=True,
    )
    logging.info(f"Researcher agent initialized for topic: {topic}, year range: {current_year - 5}-{current_year}")
    return researcher