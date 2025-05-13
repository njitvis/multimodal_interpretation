import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


clarity = pd.read_csv("./data/reasons_chart_segment.csv")
usefulness = pd.read_csv("./data/reasons_caption_segment.csv")

merged = pd.merge(clarity, usefulness, on=["reason_id", "image_id", "rating"])
merged.drop(columns=["reason_x", "reason_y"], inplace=True)
merged["sentiment"] = merged["sentiment"].apply(lambda x: x.replace('**', ''))

rating_map = {
	1: "Low",
	2: "Low",
	3: "Moderate",
	4: "High",
	5: "High",
}
merged["rating_category"] = merged["rating"].map(rating_map)
print(merged.value_counts(subset=["sentiment", "usefulness", "rating_category"]))

def map_size(count):
		if count < 15:
			return 15
		elif count < 30:
			return 30
		elif count < 45:
			return 45
		else:
			return 60
grouped = merged.groupby(['sentiment', 'usefulness', 'rating_category']).size().reset_index(name='count')
grouped = grouped[grouped["sentiment"] != "Neutral"]
grouped['count'] = grouped['count'].apply(map_size)

sentiment_order = ["Strong Positive", "Moderate Positive", "Moderate Negative", "Strong Negative"]
sentiment_map = {sent: i for i, sent in enumerate(sentiment_order)}
grouped['sentiment_pos'] = grouped['sentiment'].map(sentiment_map)

rating_categories = grouped['rating_category'].unique()
offset_map = {
    cat: i - (len(rating_categories) - 1)/2 for i, cat in enumerate(rating_categories)
}
grouped['sentiment_dodged'] = grouped['sentiment_pos'] + grouped['rating_category'].map(offset_map) * 0.15

grouped = grouped[grouped["usefulness"] != "neutral"]

grouped['usefulness'] = pd.Categorical(grouped['usefulness'], ['not_useful', 'useful'])
grouped.sort_values(by=['usefulness'], inplace=True)

custom_palette = {
    'High': 'blue',
    'Moderate': 'grey',
    'Low': 'orange'
}
grouped[["sentiment",  "usefulness", "rating_category",  "count"]].to_csv("./data/clarity_usefulness_rating_data.csv", index=False)
plt.figure(figsize=(12, 5))
sns.scatterplot(
    data=grouped,
    x='sentiment_dodged',
    y='usefulness',
    hue='rating_category',
    size='count',
    palette=custom_palette,
    alpha=0.7,
    sizes=(100, 400),
    edgecolor='black',
    linewidth=0.5,
    legend='full',
)

plt.xticks(ticks=list(sentiment_map.values()), labels=list(sentiment_map.keys()))
plt.xlabel("Sentiment towards chart")
plt.ylabel("Caption usefulness")
manual_usefulness_order = ["Not useful", "Useful"]
plt.yticks(
    ticks=range(len(manual_usefulness_order)),
    labels=manual_usefulness_order
)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("./output/clarity_usefulness_rating.png", dpi=300)
plt.close()
