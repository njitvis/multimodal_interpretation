import pandas as pd
import re

caption_features = pd.read_csv('./data/reasons_caption_segment.csv')
caption_features['usefulness'] = caption_features['usefulness'].apply(lambda x: x.replace("**", ""))
caption_features['feature'] = caption_features['feature'].apply(lambda x: x.replace("**", ""))
caption_features['feature'] = caption_features['feature'].apply(lambda x: x.replace('"', ""))
caption_features['feature'] = caption_features['feature'].apply(
    lambda x: re.sub(r'\d+\.\s*', '', x.replace('Label: ', ""))
)

usefulness_freq_keywords = {}
for usefulness in caption_features["usefulness"].unique():
	usefulness_freq_keywords[usefulness] = caption_features.loc[caption_features['usefulness'] == usefulness, "feature"].value_counts().to_dict()

for key, val in usefulness_freq_keywords.items():
	print(f"\n{key}")
	for k, v in val.items():
		print(f"\t{k}: {v}")
