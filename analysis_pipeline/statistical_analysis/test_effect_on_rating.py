import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

pandas2ri.activate()

VGAM = importr('VGAM')

r = ro.r


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

merged_subset = merged_cleaned[["rating",  "sentiment",  "usefulness"]]
merged_subset.rename(columns={"sentiment": "sentiment_towards_chart", "usefulness": "caption_usefulness", "rating": "interpretability_rating"}, inplace=True)


r.assign('df', pandas2ri.py2rpy(merged_subset))

r('''
library(VGAM)
model_ppom <- vglm(
  interpretability_rating ~ caption_usefulness * sentiment_towards_chart,
  family = cumulative(parallel = FALSE ~ caption_usefulness, link = "logit"),
  data = df
)
''')

print(r('summary(model_ppom)'))


