import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


df = pd.read_csv('../data/average_rating.csv')
df.drop(columns=["mean_rating"], inplace=True)
df = df.astype(int)
df.rename(columns={
	'interpretability_rating_phd_res1': "Annotator_1",
	'interpretability_rating_phd_res2': "Annotator_2",
	'interpretability_rating_u_res1': "Annotator_3",
	'interpretability_rating_u_res2': "Annotator_4"
}, inplace=True)

def compute_agreement(labels):
    counts = Counter(labels)
    return len(counts)

df['Agreement'] = df[["Annotator_1", "Annotator_2", "Annotator_3", "Annotator_4"]].apply(compute_agreement, axis=1)
df.sort_values(by="Agreement", ascending=False, inplace=True)
df.drop(columns=["Agreement"], inplace=True)

df['image_id'] = df['image_id'].astype(str)
df['image_id'] = pd.Categorical(df['image_id'], categories=df['image_id'], ordered=True)
df_melted = pd.melt(
    df,
    id_vars=['image_id'],
    value_vars=[
        'Annotator_1',
        'Annotator_2',
        'Annotator_3',
        'Annotator_4'
    ],
    var_name='Rater',
    value_name='Rating'
)
df_melted['Group'] = df_melted['Rater'].apply(
    lambda r: 'PhD' if r in ['Annotator_1', 'Annotator_2'] else 'UG'
)
df_melted['image_id'] = pd.Categorical(df_melted['image_id'], categories=df['image_id'], ordered=True)

custom_palette = {
    "PhD": 'orange',  
    "UG": 'blue',  
}

plt.figure(figsize=(10, 60))

sns.swarmplot(
	x="Rating", y="image_id", data=df_melted,
	hue="Group",
	size=10,
    palette=custom_palette, 
	linewidth=1, 
	edgecolor="w",
	orient="v"
)

labels = df['image_id'].tolist()
positions = np.arange(len(labels))
midpoints = (positions[:-1] + positions[1:]) / 2
plt.gca().set_yticks(midpoints, minor=True)
plt.grid(which='minor', axis='y', linestyle='--', linewidth=0.5, color='gray')
plt.ylim(-0.5, len(labels) - 0.5)
plt.yticks(ticks=df_melted['image_id'].to_list(), labels=df_melted['image_id'].to_list())
plt.title("Interpretability Ratings by Rater")
plt.legend(title="Rating", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f"./output/rating_vs/rating_by_rater.png", dpi=300)
plt.close()