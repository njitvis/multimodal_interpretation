import pandas as pd

reasons = pd.read_csv("./data/reasons_segmented.csv")

segments = ["chart", "both", "caption"]

for segment in segments:
	segment_df = reasons[["reason_id", "image_id", "rating", segment]]
	segment_df.dropna(inplace=True)
	segment_df.rename(columns={f"{segment}": "reason"}, inplace=True)
	segment_df.to_csv(f"./data/reasons_{segment}_segment.csv", index=False)