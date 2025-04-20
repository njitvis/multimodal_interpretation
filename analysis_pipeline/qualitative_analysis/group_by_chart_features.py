import requests
import time
import re
import pandas as pd


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

reasons = pd.read_csv("./data/reasons_chart_segment.csv")

def get_code(text):
    prompt = f"""
You are a response analyst. Your task is to label the given text as either .

Examples:
Text: "detailed caption that provides the main key takeaway"
Label: useful

Text: "the caption does not explain the context or trend" 
Label: not_useful

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

def extract_label(sentence):
    match = re.search(r'\b(useful|not_useful|neutral)\b', sentence, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return None

print("🧠 Thematic Coding Results:\n")
for idx, reason in reasons.iterrows():
    code = get_code(reason['reason'])
    reasons.at[idx, "usefulness"] = extract_label(code)
    time.sleep(1)

reasons.to_csv("./data/reasons_caption_segment.csv", index=False)