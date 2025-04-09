# utils/ollama_wrapper.py
import ollama
import logging
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "research.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def ollama_completion(prompt: str, model: str = "llama3.2:latest") -> str:
    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        result = response["message"]["content"]
        logging.info(f"Ollama completion successful for prompt: {prompt[:50]}...")
        return result
    except Exception as e:
        logging.error(f"Ollama completion failed: {str(e)}")
        raise e