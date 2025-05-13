import pandas as pd


clarity = pd.read_csv("./data/reasons_chart_segment.csv")
usefulness = pd.read_csv("./data/reasons_caption_segment.csv")

clarity["sentiment"] = clarity["sentiment"].apply(lambda x: x.replace('**', ''))
neutral_chart = clarity[clarity["sentiment"] == "Neutral"]
neutral_chart = neutral_chart["reason_id"].to_list()

neutral_cap = usefulness[usefulness["usefulness"] == "neutral"]
neutral_cap = neutral_cap["reason_id"].to_list()

reasons_seg = pd.read_csv("./data/reasons_segmented.csv")
all_reasons = pd.read_csv("../data/all_reasons.csv")

reasons_seg = reasons_seg[(reasons_seg["reason_id"].isin(clarity["reason_id"])) & (reasons_seg["reason_id"].isin(usefulness["reason_id"]))]

for idx, row in reasons_seg.iterrows():
	image_id = row["image_id"]
	reason = row["reason"]
	rating = row["rating"]
	found = False
	for col in ["_u_res1","_u_res2","_res1","_res2"]:
		group_row = all_reasons[(all_reasons["image_id"] == image_id) & (all_reasons[f"interpretability_rating{col}"] == rating) & (all_reasons[f"reason{col}"] == reason)]
		if not group_row.empty:
				reasons_seg.at[idx, "group"] = col
				found = True
				break

print("\n\n")
unmatched_rows = reasons_seg[reasons_seg["group"].isna()]
unmatched_rows = unmatched_rows[~unmatched_rows["reason_id"].isin(neutral_chart)]
unmatched_rows = unmatched_rows[~unmatched_rows["reason_id"].isin(neutral_cap)]

print(unmatched_rows.shape)
print(reasons_seg[~reasons_seg["reason_id"].isin(unmatched_rows["reason_id"])])

reasons_seg.to_csv("./reasons_with_group.csv", index = False)


