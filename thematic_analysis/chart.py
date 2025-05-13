import pandas as pd

df = pd.read_csv("./reasons_chart_segment.csv")
df["sentiment"] = df["sentiment"].apply(lambda x: x.replace("**", ""))
df["sentiment"] = df["sentiment"].map({"Strong Positive": "positive", "Moderate Positive": "positive", "Moderate Negative": "negative", "Strong Negative": "negative"})

df_all = pd.read_csv("./all_reasons.csv")

positive = df[df["sentiment"] == "positive"].copy()
negative = df[df["sentiment"] == "negative"].copy()
mixed = pd.merge(positive, negative, on="image_id", how="inner")
# mixed.rename(columns={"reason_x": "reason_useful", "reason_y": "reason_not_useful"}, inplace=True)

positive = positive[~positive["image_id"].isin(mixed["image_id"])].copy()
negative = negative[~negative["image_id"].isin(mixed["image_id"])].copy()

positive.drop_duplicates(subset=["image_id"], inplace=True)
negative.drop_duplicates(subset=["image_id"], inplace=True)
mixed.drop_duplicates(subset=["image_id"], inplace=True)

print(positive.shape, negative.shape, mixed.shape)

# useful = pd.merge(useful, captions, on="image_id", how="left")
# not_useful = pd.merge(not_useful, captions, on="image_id", how="left")
# mixed = pd.merge(mixed, captions, on="image_id", how="left")

# # def find_expertise(val):
# # 	cols = ["reason_u_res1", "reason_u_res2", "reason_res1", "reason_res2"]
# # 	for col in cols:
# # 		if val in df_all[col].values:
# # 			return col

# # mixed["expertise_useful"] = mixed["reason_useful"].apply(find_expertise)
# # mixed["expertise_not_useful"] = mixed["reason_not_useful"].apply(find_expertise)

# # mixed["expertise_useful"] = mixed["expertise_useful"].map({"reason_u_res1": "ug", "reason_u_res2": "ug", "reason_res1": "phd", "reason_res2": "phd"})
# # mixed["expertise_not_useful"] = mixed["expertise_not_useful"].map({"reason_u_res1": "ug", "reason_u_res2": "ug", "reason_res1": "phd", "reason_res2": "phd"})

# mixed_all = pd.merge(df_all, mixed, on="image_id", how="left")
# mixed_all.dropna(subset=["usefulness_x", "usefulness_y"],inplace=True)
# print(mixed_all.columns)

# # print(mixed[(mixed["expertise_useful"].isna()) & (mixed["expertise_not_useful"].isna())])
# # phd_useful = mixed[mixed["expertise_useful"] == "phd"]
# # phd_not_useful = mixed[mixed["expertise_not_useful"] == "phd"]
# # ug_useful = mixed[mixed["expertise_useful"] == "ug"]
# # ug_not_useful = mixed[mixed["expertise_not_useful"] == "ug"]

# # print(phd_useful.shape, phd_not_useful.shape, ug_useful.shape, ug_not_useful.shape)
# positive.to_csv("./positive_chart.csv", index=False)
# negative.to_csv("./negative_chart.csv", index=False)
# mixed.to_csv("./mixed_chart.csv", index=False)
# mixed_all.to_csv("./mixed_all.csv", index=False)

print(sorted(negative["image_id"].to_list()))