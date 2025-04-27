from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd
from statsmodels.tools.tools import add_constant


clarity = pd.read_csv("../qualitative_analysis/data/reasons_chart_segment.csv")
usefulness = pd.read_csv("../qualitative_analysis/data/reasons_caption_segment.csv")

merged = pd.merge(clarity, usefulness, on=["reason_id", "image_id", "rating"])
merged.drop(columns=["reason_x", "reason_y", "feature_x", "feature_y"], inplace=True)
merged["sentiment"] = merged["sentiment"].apply(lambda x: x.replace('**', ''))
merged_cleaned = merged[merged['sentiment'] != 'Neutral'].copy()
merged_cleaned = merged_cleaned[merged_cleaned['usefulness'] != 'neutral'].copy()

usefulness_map = {
	"useful": 1,
	"not_useful": 0
}
sentiment_map = {
	"Strong Positive": 1,
	"Moderate Positive": 1,
	"Moderate Negative": 0,
	"Strong Negative": 0,
}
merged_cleaned["usefulness"] = merged_cleaned["usefulness"].map(usefulness_map)
merged_cleaned["sentiment"] = merged_cleaned["sentiment"].map(sentiment_map)

merged_subset = merged_cleaned[["sentiment",  "usefulness"]]
merged_subset.rename(columns={"sentiment": "sentiment_towards_chart", "usefulness": "caption_usefulness"}, inplace=True)

X = merged_subset
X = add_constant(X)

vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)