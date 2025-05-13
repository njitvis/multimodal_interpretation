import pandas as pd

df = pd.read_csv("./reasons_caption_segment.csv")
df_all = pd.read_csv("./all_reasons.csv")
captions = pd.read_csv("./captions.csv")
captions.drop(columns=["source","domain","chart_type","views"], inplace=True)

useful = df[df["usefulness"] == "useful"].copy()
not_useful = df[df["usefulness"] == "not_useful"].copy()
mixed = pd.merge(useful, not_useful, on="image_id", how="inner")
mixed.rename(columns={"reason_x": "reason_useful", "reason_y": "reason_not_useful"}, inplace=True)

useful = useful[~useful["image_id"].isin(mixed["image_id"])].copy()
not_useful = not_useful[~not_useful["image_id"].isin(mixed["image_id"])].copy()

useful.drop_duplicates(subset=["image_id"], inplace=True)
not_useful.drop_duplicates(subset=["image_id"], inplace=True)
mixed.drop_duplicates(subset=["image_id"], inplace=True)

print(useful.shape, not_useful.shape, mixed.shape)

useful = pd.merge(useful, captions, on="image_id", how="left")
not_useful = pd.merge(not_useful, captions, on="image_id", how="left")
mixed = pd.merge(mixed, captions, on="image_id", how="left")

# def find_expertise(val):
# 	cols = ["reason_u_res1", "reason_u_res2", "reason_res1", "reason_res2"]
# 	for col in cols:
# 		if val in df_all[col].values:
# 			return col

# mixed["expertise_useful"] = mixed["reason_useful"].apply(find_expertise)
# mixed["expertise_not_useful"] = mixed["reason_not_useful"].apply(find_expertise)

# mixed["expertise_useful"] = mixed["expertise_useful"].map({"reason_u_res1": "ug", "reason_u_res2": "ug", "reason_res1": "phd", "reason_res2": "phd"})
# mixed["expertise_not_useful"] = mixed["expertise_not_useful"].map({"reason_u_res1": "ug", "reason_u_res2": "ug", "reason_res1": "phd", "reason_res2": "phd"})

mixed_all = pd.merge(df_all, mixed, on="image_id", how="left")
mixed_all.dropna(subset=["usefulness_x", "usefulness_y"],inplace=True)
print(mixed_all.columns)

# print(mixed[(mixed["expertise_useful"].isna()) & (mixed["expertise_not_useful"].isna())])
# phd_useful = mixed[mixed["expertise_useful"] == "phd"]
# phd_not_useful = mixed[mixed["expertise_not_useful"] == "phd"]
# ug_useful = mixed[mixed["expertise_useful"] == "ug"]
# ug_not_useful = mixed[mixed["expertise_not_useful"] == "ug"]

# print(phd_useful.shape, phd_not_useful.shape, ug_useful.shape, ug_not_useful.shape)
# useful.to_csv("./useful_captions.csv", index=False)
# not_useful.to_csv("./not_useful_captions.csv", index=False)
# mixed.to_csv("./mixed.csv", index=False)
mixed_all.to_csv("./mixed_all.csv", index=False)