# main.py
from flask import Flask, render_template, request
from crewai import Crew
from tasks.research_task import create_research_task
import logging
import os
from datetime import datetime

app = Flask(__name__)

log_dir = "logs"
output_dir = "outputs"
os.makedirs(log_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form.get('topic', '').strip()
        if not topic:
            return render_template('index.html', error="Topic cannot be empty.")
        
        try:
            task = create_research_task(topic=topic, start_year=datetime.now().year, max_papers=5)
            crew = Crew(
                agents=[task.agent],
                tasks=[task],
                verbose=True
            )
            logging.info(f"Starting research crew execution for topic: {topic}")
            result = crew.kickoff()
            logging.info("Research task completed successfully.")
            return render_template('results.html', topic=topic, results=str(result))
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return render_template('index.html', error=f"Error: {str(e)}")
    
    return render_template('index.html', error=None)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)