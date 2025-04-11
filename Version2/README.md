# Research Assistant Agent - Version2

A Flask-based AI-powered research assistant that fetches real acdemic papers from Google Scholar (via SerpAPI), and summarizes them using a custom-built Research Analyst Agent powered by CrewAI, LangChain, and Ollama.

# Features

* Live search for papers from Google Scholar using SerpAPI

* Extracts and summarizes the latest top 5 papers on a given topic

* Includes authors, title, abstract highlights, and publication year

* Custom LangChain agent for domain-agnostic academic analysis

* Simple Flask web interface for user interaction

* Year based filtering

## Required Dependencies

- flask

- crewai

- langchain

- langchain_ollama

- requests

Update the ```api_key``` in ```tasks/research_task.py``` with you SERPAPI key.
You can get a free API key at https://serpapi.com/