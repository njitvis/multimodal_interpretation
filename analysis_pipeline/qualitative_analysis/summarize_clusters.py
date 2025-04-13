import pandas as pd
import requests
import json


#segments = ["captions", "charts", "both"]
segments = ["captions"]
usefulness_groups = ["useful", "not_useful", "neutral"]

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def get_summary(sentences):
    input_text = "\n".join([f"- {sentence}" for sentence in sentences])
    
    prompt = f"""
You are a helpful summarization assistant. Your task is to create a concise summary of the following sentences.
Create a summary that captures the key points in 1-2 sentences.

Sentences to summarize:
{input_text}

Summary:"""
    
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()

for segment in segments:
  for usefulness_group in usefulness_groups:
      df = pd.read_csv(f"./data/clustered_{usefulness_group}_{segment}.csv")

      clusters = {}

      for cluster in df['cluster'].unique():
        cluster_pop = df[df["cluster"] == cluster]
        clusters[str(cluster)] = get_summary(cluster_pop['reason'].to_list())

      with open(f"./data/{usefulness_group}_{segment}_cluster_def.json", "w") as f:
        json.dump(clusters, f, indent=2)