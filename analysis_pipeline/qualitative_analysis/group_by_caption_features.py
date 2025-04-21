import requests
import time
import re
import pandas as pd


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

reasons = pd.read_csv("./data/reasons_caption_segment.csv")

def get_code(text):
    prompt = f"""
You analyze user feedback about captions and classify each comment into one of nine feature clusters based on what aspect of the caption the user focuses on.

## Feature Clusters

### 1. Caption Clarity Lost in Translation
- **FOCUS:** Translation issues or excessive references making captions hard to follow
- **KEY TERMS:** reading, lost, citations, translation
- **EXAMPLES:**
  - "Caption has too many citations; lost reading caption"
  - "Caption clearly explains the labels used, caption is lost in translation"

### 2. Lack of Summary or Takeaway
- **FOCUS:** Missing concise summary or main message
- **KEY TERMS:** summarize, main, takeaway, trend
- **EXAMPLES:**
  - "Caption does not summarize the clear takeaway message"
  - "Caption does not summarize a takeaway message"

### 3. Overloaded with Information
- **FOCUS:** Too much raw information without synthesis
- **KEY TERMS:** provides, information, too much, context
- **EXAMPLES:**
  - "Caption has too much information"
  - "Provides a lot of context but not summarizing the main takeaway"

### 4. Missing or Poor Trend Explanation
- **FOCUS:** Inadequate explanation of data trends
- **KEY TERMS:** explain, trend, better
- **EXAMPLES:**
  - "The caption doesn't explain the trend"
  - "The caption can be better by explaining the trend"

### 5. Missing Clear Takeaway Message
- **FOCUS:** Lack of clear communication of insights or conclusions
- **KEY TERMS:** message, takeaway, clear, explain
- **EXAMPLES:**
  - "Chart A caption does not explain the takeaway clearly"
  - "No clear explanation about the chart and no clear takeaway mentioned"

### 6. Helpful Main Takeaway or Comparison
- **FOCUS:** Positive feedback on conveying trends or comparisons
- **KEY TERMS:** main, trends, takeaway, understand
- **EXAMPLES:**
  - "The caption makes it easy to understand the main key takeaway"
  - "Caption complements... does not state the main takeaway"

### 7. Caption Length – Too Long or Cluttered
- **FOCUS:** Overly long or visually overwhelming captions
- **KEY TERMS:** large, cluttered, unnecessarily, too long
- **EXAMPLES:**
  - "The caption is also too large"
  - "Cluttered and large caption"

### 8. Detailed but Possibly Excessive
- **FOCUS:** Detailed information that might be too extensive
- **KEY TERMS:** detailed, long, context, informative
- **EXAMPLES:**
  - "Detailed caption"
  - "Long caption"

### 9. General Positivity or Praise
- **FOCUS:** Overall positive assessment with minimal criticism
- **KEY TERMS:** good, effective, clear, explanation
- **EXAMPLES:**
  - "The caption is good"
  - "Caption are good"

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