import pandas as pd
import spacy
from transformers import pipeline

reasons = pd.read_csv("./data/all_reasons.csv")

nlp = spacy.load("en_core_web_sm")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def split_into_meaningful_segments(sentence):
    """
    Splits a sentence into meaningful segments based on syntactic dependencies.
    """
    doc = nlp(sentence)
    segments = []
    current_segment = []

    for token in doc:
        current_segment.append(token.text)

        # Split on punctuation and coordinating conjunctions
        if token.dep_ in ("cc", "punct") and token.text in [",", ".", ";", "and", "but"]:
            segments.append(" ".join(current_segment).strip())
            current_segment = []

    if current_segment:
        segments.append(" ".join(current_segment).strip())

    return segments

def classify_segments(segments):
    """
    Classifies each segment as referring to chart, caption, or both.
    """
    candidate_labels = ["chart", "caption", "both"]
    classifications = []

    for segment in segments:
        result = classifier(segment, candidate_labels, multi_label=True)
        best_label = result["labels"][0]  # Take the highest confidence label
        classifications.append((segment, best_label))

    return classifications

def merge_segments(classifications):
    """
    Merges adjacent segments with the same classification.
    """
    merged_output = []
    prev_segment, prev_label = classifications[0]

    for i in range(1, len(classifications)):
        current_segment, current_label = classifications[i]

        if current_label == prev_label:
            prev_segment += " " + current_segment  # Merge with previous segment
        else:
            merged_output.append((prev_segment, prev_label))
            prev_segment, prev_label = current_segment, current_label

    merged_output.append((prev_segment, prev_label))  # Append last segment
    return merged_output

def flatten_reason():
    global reasons
    
    res1 = reasons[["image_id", "interpretability_rating_u_res1", "reason_u_res1"]]
    res1.rename(columns={"interpretability_rating_u_res1": "rating", "reason_u_res1": "reason"}, inplace=True)
    res2 = reasons[["image_id", "interpretability_rating_u_res2", "reason_u_res2"]]
    res2.rename(columns={"interpretability_rating_u_res2": "rating", "reason_u_res2": "reason"}, inplace=True)
    res3 = reasons[["image_id", "interpretability_rating_res1", "reason_res1"]]
    res3.rename(columns={"interpretability_rating_res1": "rating", "reason_res1": "reason"}, inplace=True)
    res4 = reasons[["image_id", "interpretability_rating_res2", "reason_res2"]]
    res4.rename(columns={"interpretability_rating_res2": "rating", "reason_res2": "reason"}, inplace=True)

    reasons = pd.concat([res1, res2, res3, res4])
    reasons.index.name = 'index'
    reasons = reasons.reset_index()
    reasons = reasons.rename(columns={'index': 'reason_id'})


def main():
  flatten_reason()
  for idx, row in reasons.iterrows():
    try:
      segments = split_into_meaningful_segments(row["reason"])
    except Exception as e:
      print(row["reason"])
      print(e)
      continue
    try:
      classified_segments = classify_segments(segments)
    except Exception as e:
      print(row["reason"])
      print(e)
      continue
    try:
      final_output = merge_segments(classified_segments)
      for segment, label in final_output:
        reasons.at[idx, label] = segment
    except Exception as e:
      print(row["reason"])
      print(e)
  reasons.to_csv("./data/reasons_segmented.csv", index=False)

if __name__ == "__main__":
    main()
