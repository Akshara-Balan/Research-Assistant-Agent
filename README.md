# Research-Assistant-Agent

## Version1

This version will read a topic from user and then give a report where the report may not be real time data. The generated report is a hallucination from the training data of the llama3.2 LLM.

## Version2

This version will read the papers from google scholar and give response accordingly. There is no hallucination. Implemented a frontend module.

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