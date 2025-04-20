import requests
import time
import re
import pandas as pd


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

reasons = pd.read_csv("./data/reasons_chart_segment.csv")

def get_code(text):
    prompt = f"""
# Chart Review Sentiment Classifier

You are a sentiment classifier for short reviews about data visualizations. For each input review, classify it into EXACTLY ONE of these five sentiment categories:

## Sentiment Categories
1. **Strong Positive**
2. **Moderate Positive**
3. **Neutral**
4. **Moderate Negative**
5. **Strong Negative**

## Category Definitions

### 1. Strong Positive
- **WHEN TO USE:** Review shows clear enthusiasm, satisfaction, or strong praise
- **EMOTIONAL TONE:** Very pleased, impressed, enthusiastic
- **EXAMPLES:** 
  - "Easy to compare stabilization categories"
  - "The design is very clear and engaging"

### 2. Moderate Positive
- **WHEN TO USE:** Review shows general approval or mild satisfaction
- **EMOTIONAL TONE:** Pleased, satisfied, but not overly enthusiastic
- **EXAMPLES:** 
  - "The chart is clear, allows for comparison"
  - "Clean layout, I can see trends easily"

### 3. Neutral
- **WHEN TO USE:** Review is factual or descriptive without clear sentiment
- **EMOTIONAL TONE:** Matter-of-fact, objective, neither positive nor negative
- **EXAMPLES:** 
  - "Chart has different curves representing different stocks"
  - "The trend is understandable"

### 4. Moderate Negative
- **WHEN TO USE:** Review contains mild criticism or notes minor issues
- **EMOTIONAL TONE:** Slightly dissatisfied, constructively critical
- **EXAMPLES:** 
  - "The takeaway is not very clear"
  - "Too many lines make it hard to follow"

### 5. Strong Negative
- **WHEN TO USE:** Review shows frustration, confusion, or strong disapproval
- **EMOTIONAL TONE:** Very dissatisfied, frustrated, confused
- **EXAMPLES:** 
  - "Cluttered visualization"
  - "I can't tell what this is showing—it's overwhelming"

## Instructions
1. Read the input review carefully
2. Consider the emotional tone and sentiment expressed
3. Match to EXACTLY ONE category above
4. Respond ONLY with the category name (e.g., "Strong Positive"), nothing else

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
    reasons.at[idx, "sentiment"] = get_code(reason['reason'])
    time.sleep(1)

reasons.to_csv("./data/reasons_caption_segment.csv", index=False)