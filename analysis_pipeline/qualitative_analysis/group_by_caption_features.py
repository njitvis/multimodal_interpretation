import requests
import time
import re
import pandas as pd


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

reasons = pd.read_csv("./data/reasons_caption_segment.csv")

def get_code(text):
    prompt = f"""
You analyze user feedback about captions and classify each comment into one of six feature clusters based on what aspect of the caption the user focuses on.

## Feature Clusters

1. Insufficient or Unclear Description
  - The caption either lacks essential details or poorly describes the visualization, leaving viewers uncertain about what the chart shows. It may be vague, incomplete, or indirectly related to the chart content.

2. Observed Pattern Not Explained
  - The caption mentions or implies a pattern, trend, or relationship observed in the visualization but does not adequately explain or clarify why that pattern exists or what its significance is.

3. Missing or Unclear Takeaway Message
  - Although the caption may describe elements of the chart, it fails to deliver a clear takeaway message or summary point. Viewers struggle to quickly grasp the main insight or implication of the visualization.

4. Detailed and Informative
  - The caption effectively and clearly describes the chart content, providing thorough context, relevant details, and information that significantly aids interpretation without being overwhelming or excessive.

5. Detailed but Overloaded with Information
  - The caption contains detailed descriptions or extensive information, but it is overly lengthy or complex, potentially obscuring key points or making it challenging for readers to easily identify the main insights.

6. Clear and Good Quality
  - The caption clearly summarizes and highlights essential insights from the chart. It strikes a good balance by succinctly providing context, clearly stating observed trends or patterns, and making the chart easy to interpret at a glance.

## Instructions
1. Read the user comment about a caption
2. Identify which feature cluster best matches the comment's focus
3. Return ONLY the name of the chosen cluster (e.g., "Caption Clarity Lost in Translation")

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

print("🧠 Thematic Coding Results:\n")
for idx, reason in reasons.iterrows():
    reasons.at[idx, "feature"] = get_code(reason['reason'])
    time.sleep(1)

reasons.to_csv("./data/reasons_caption_segment.csv", index=False)