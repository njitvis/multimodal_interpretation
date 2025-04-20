import requests
import time
import re
import pandas as pd


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

reasons = pd.read_csv("./data/reasons_chart_segment.csv")

def get_code(text):
    prompt = f"""
You are a specialized classifier for short sentences reviewing data visualizations. For each input, classify it into EXACTLY ONE of these five categories:
Categories

Visual Density / Clutter
Labels-Titles-Legend-Scale
Trend / Pattern Depiction
Chart Type & Layout Choice
Aesthetics-Clarity-Comparison

Category Definitions
1. Visual Density / Clutter

CHOOSE THIS IF: Review mentions too much information, overcrowding, overlapping elements
KEY TERMS: cluttered, dense, busy, crowded, overlapping, too many elements, hard to see due to overlap
EXAMPLE: "The visualization is cluttered and everything overlaps."
NOT THIS: "Colours are confusing" (→ Labels-Titles-Legend-Scale)

2. Labels-Titles-Legend-Scale

CHOOSE THIS IF: Review focuses on descriptive elements or color choices needed for interpretation
KEY TERMS: axis labels, titles, ticks, units, scale, legend, key, color choices
EXAMPLE: "Axes lack units and the legend colours are hard to match."
NOT THIS: "Bars overlap too much" (→ Visual Density / Clutter)

3. Trend / Pattern Depiction

CHOOSE THIS IF: Review comments on how well data behavior over time or categories is conveyed
KEY TERMS: trend, pattern, increase, decrease, rise, drop, trajectory, fluctuation, change over time
EXAMPLE: "The declining trend after 2010 isn't obvious."
NOT THIS: "The line chart is a poor choice" (→ Chart Type & Layout Choice)

4. Chart Type & Layout Choice

CHOOSE THIS IF: Review judges suitability of the chart type or arrangement of elements
KEY TERMS: specific chart types (bar, line, pie), multi-panel layouts, 3D, radial vs. cartesian
EXAMPLE: "The pie chart should have been a bar chart for easier comparison."
NOT THIS: "Too many slices make it cluttered" (→ Visual Density / Clutter)

5. Aesthetics-Clarity-Comparison

CHOOSE THIS IF: Review makes general quality remarks about readability, appeal, or comparison ease
KEY TERMS: clear, readable, appealing, professional, intuitive, simple, easy/hard to understand
EXAMPLE: "The chart is clean and the message is immediately clear."
NOT THIS: "No axis label, so the message is unclear" (→ Labels-Titles-Legend-Scale)

Instructions

Read the input review sentence carefully
Identify the main issue being described
Match to EXACTLY ONE category above
Respond ONLY with the category name, nothing else

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
    reasons.at[idx, "feature"] = get_code(reason['reason'])
    time.sleep(1)

reasons.to_csv("./data/reasons_chart_segment.csv", index=False)