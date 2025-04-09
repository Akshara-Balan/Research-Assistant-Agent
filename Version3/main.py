# main.py
from flask import Flask, render_template, request, send_file
from crewai import Crew
from tasks.research_task import create_research_task
from tasks.review_task import create_review_task
import logging
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

app = Flask(__name__)

log_dir = "logs"
output_dir = "outputs"
download_dir = "static/downloads"
os.makedirs(log_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(download_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def generate_pdf(content, filename):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph(f"Research Results for '{content['topic']}'", styles['Title'])]
    story.append(Spacer(1, 12))
    for line in content['results'].split('\n'):
        story.append(Paragraph(line.replace('\n', '<br />'), styles['BodyText']))
        story.append(Spacer(1, 6))
    doc.build(story)
    buffer.seek(0)
    with open(filename, 'wb') as f:
        f.write(buffer.read())
    return filename

def generate_markdown(content, filename):
    with open(filename, 'w') as f:
        f.write(f"# Research Results for '{content['topic']}'\n\n")
        f.write(content['results'].replace('\n', '\n\n'))
    return filename

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form.get('topic', '').strip()
        subdomain = request.form.get('subdomain', '').strip()
        export_type = request.form.get('export', None)
        if not topic:
            return render_template('index.html', error="Topic cannot be empty.")

        try:
            search_query = f"{topic} {subdomain}" if subdomain else topic
            research_task = create_research_task(search_query)
            review_task = create_review_task(search_query, research_task)
            crew = Crew(
                agents=[research_task.agent, review_task.agent],
                tasks=[research_task, review_task],
                verbose=True
            )
            logging.info(f"Starting crew execution for topic: {search_query}")
            # Since LLM is handled in tasks, just collect results
            research_result = f"{research_task.expected_output}\n\n{review_task.expected_output}"
            logging.info("Crew execution completed successfully.")
            
            content = {"topic": search_query, "results": research_result}
            
            if export_type == "pdf":
                filename = os.path.join(download_dir, f"{search_query.replace(' ', '_')}_{datetime.now().year}.pdf")
                generate_pdf(content, filename)
                return send_file(filename, as_attachment=True)
            elif export_type == "markdown":
                filename = os.path.join(download_dir, f"{search_query.replace(' ', '_')}_{datetime.now().year}.md")
                generate_markdown(content, filename)
                return send_file(filename, as_attachment=True)
            else:
                return render_template('results.html', topic=search_query, results=research_result)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return render_template('index.html', error=f"Error: {str(e)}")
    
    return render_template('index.html', error=None)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)