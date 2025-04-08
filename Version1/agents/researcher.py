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

# Use explicit phi3:3.8b tag
llm = OllamaLLM(model="ollama/llama3.2:latest")  # Updated to phi3:3.8b

researcher = Agent(
    role="Research Analyst",
    goal="Identify and summarize the latest research trends in AI, focusing on LLM alignment",
    backstory=(
        "An expert analyst with a PhD in computational linguistics, skilled in "
        "extracting academic insights from diverse sources and presenting them clearly."
    ),
    allow_delegation=False,
    llm=llm,
    verbose=True,
)

def get_researcher():
    logging.info("Researcher agent initialized.")
    return researcher