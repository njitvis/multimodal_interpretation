import requests
import time
import re
import pandas as pd


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

reasons = pd.read_csv("./data/reasons_chart_segment.csv")

def get_code(text):
    prompt = f"""
You are a specialized classifier for short sentences reviewing data visualizations. For each input, classify it into EXACTLY ONE of these three categories:
Categories

Now, label the following text:
Text: "{text}"
Label: """
    
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()

for idx, reason in reasons.iterrows():
    reasons.at[idx, "clarity"] = get_code(reason['reason'])
    time.sleep(1)

reasons.to_csv("./data/reasons_chart_segment.csv", index=False)