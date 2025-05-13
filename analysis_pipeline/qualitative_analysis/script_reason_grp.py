import pandas as pd 

clarity = pd.read_csv("./data/reasons_chart_segment.csv")
usefulness = pd.read_csv("./data/reasons_caption_segment.csv")
grp = pd.read_csv("./reasons_with_group_revised.csv")
grp = grp[["reason_id", "group"]]

merged = pd.merge(clarity, grp, on="reason_id", how="left")
merged.to_csv("./data/reasons_chart_segment_grp.csv", index=False)

merged = pd.merge(usefulness, grp, on="reason_id", how="left")
merged.to_csv("./data/reasons_caption_segment_grp.csv", index=False)