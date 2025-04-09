# Research Assistant Agent

## Version1

A modular AI-powered research assistant built with CrewAI, LangChain, and Ollama. This assistant identifies and summarizes the latest academic trends in AI, focusing on topics like LLM alignment, using local LLMs such as LLaMA 3.2. The generated report is a hallucination from the training data of the llama3.2 LLM.

Technologies Used:

* CrewAI

* LangChain

* Ollama

* LLaMA 3.2 (via Ollama)


## Version2

An AI-powered research assistant that finds and summarizes recent academic papers using Google Scholar (via SerpAPI), LLaMA 3.2 (via Ollama), CrewAI, and Flask. Enter a research topic, and the assistant will fetch relevant papers from the past 5 years and summarize key findings in a clear format.

Visit ``` http://localhost:5000 ``` once the server is running to use the assistant.

Features:

🔍 Topic-based search across recent research publications (last 5 years)

🤖 Agent-based summarization using LLaMA 3.2 via Ollama

📑 Clear, structured paper summaries: title, year, authors, findings

🌐 Fetches real academic results from Google Scholar via SerpAPI

💻 Clean web interface powered by Flask

📁 Logs and saves results to logs/ and outputs/ folders

Techologies Used:

* Flask - Web Framework

* CrewAI - Agent Orchestration

* LangChain + Ollama - Local LLM integration

* LLaMA 3.2 via Ollama - Large Language Model

* SerpAPI - Google Scholar search API


## Setup

1. Create a virtual environment 
```sh
python -m venv agent
```

2. Activate the virtual environment (Ubuntu)
```sh
source agent/bin/activate
```

3. Install dependencies
```sh
pip install -r requirements.txt
```

4. Run
```sh
python3 main.py
```
