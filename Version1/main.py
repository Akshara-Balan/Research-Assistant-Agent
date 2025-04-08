# main.py
from crewai import Crew
from tasks.research_task import create_research_task
import logging
import os
import sys

log_dir = "logs"
output_dir = "outputs"
os.makedirs(log_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    try:
        topic = input("Enter the research topic (e.g., 'LLM alignment'): ").strip()
        if not topic:
            raise ValueError("Topic cannot be empty.")

        task = create_research_task(topic=topic, year=2024, num_papers=5)
        crew = Crew(
            agents=[task.agent],
            tasks=[task],
            verbose=True
        )

        logging.info(f"Starting research crew execution for topic: {topic}")
        result = crew.kickoff()
        
        print(f"Research Results for '{topic}':")
        print(result)
        logging.info("Research task completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()