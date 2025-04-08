# agents/researcher.py
from crewai import Agent
from langchain_ollama import OllamaLLM
import logging
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Use a working model (e.g., llama3.2 or phi3:3.8b)
llm = OllamaLLM(model="ollama/llama3.2")  # Adjust to phi3:3.8b if preferred

def get_researcher(topic: str) -> Agent:
    """Create a Research Analyst agent with a dynamic goal based on the user's topic."""
    researcher = Agent(
        role="Research Analyst",
        goal=f"Identify and summarize the latest research papers on '{topic}' from 2024",
        backstory=(
            "An expert analyst with a PhD in '{topic}' , skilled in "
            "extracting academic insights from diverse sources across all domains "
            "and presenting them clearly."
        ),
        allow_delegation=False,
        llm=llm,
        verbose=True,
    )
    logging.info(f"Researcher agent initialized for topic: {topic}")
    return researcher