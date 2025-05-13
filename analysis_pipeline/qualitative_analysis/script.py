import pandas as pd

captions = pd.read_csv("./data/reasons_caption_segment.csv")
charts = pd.read_csv("./data/reasons_chart_segment.csv")

reasons = pd.merge(captions, charts, on="reason_id", how="inner")

reasons.drop(columns=["image_id_x", "rating_x"], inplace=True)
reasons.rename(columns={"image_id_y": "image_id", "rating_y": "rating"}, inplace=True)
reasons["sentiment"] = reasons["sentiment"].apply(lambda x: x.replace("**", ""))

reasons["sentiment"] = reasons["sentiment"].map({"Strong Negative": "negative", "Moderate Negative": "negative", "Strong Positive": "positive", "Moderate Positive": "positive"})

reasons = reasons[["image_id", "reason_id", "rating", "sentiment", "usefulness"]].sort_values(by="image_id")

print(reasons[(reasons["sentiment"] == "positive") & (reasons["usefulness"] == "not_useful")])
# print(reasons[(reasons["sentiment"] == "negative") & (reasons["usefulness"] == "useful")].shape)
# print(reasons[(reasons["sentiment"] == "positive") & (reasons["usefulness"] == "useful")].shape)
# print(reasons[(reasons["sentiment"] == "negative") & (reasons["usefulness"] == "not_useful")].shape)
# print(reasons[(reasons["sentiment"] == "positive") & (reasons["usefulness"] == "not_useful")].shape)