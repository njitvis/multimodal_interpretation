import pandas as pd

graph_features = pd.read_csv('./data/reasons_chart_segment.csv')
graph_features['sentiment'] = graph_features['sentiment'].apply(lambda x: x.replace("**", ""))

sentiment_freq_keywords = {}
for sentiment in graph_features["sentiment"].unique():
	sentiment_freq_keywords[sentiment] = graph_features.loc[graph_features['sentiment'] == sentiment, "feature"].value_counts().to_dict()

for key, val in sentiment_freq_keywords.items():
	print(f"\n{key}")
	for k, v in val.items():
		print(f"\t{k}: {v}")
