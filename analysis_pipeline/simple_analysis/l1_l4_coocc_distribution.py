import ast
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import permutations


def generate_cooccurrence_heatmap(df, title):
	sentence_types = ["l1", "l2", "l3", "l4"]
	cooccurrence = {pair: 0 for pair in permutations(sentence_types, 2)}
	for _, row in df.iterrows():
			for pair in cooccurrence.keys():
					if row[pair[0]] > 0 and row[pair[1]] > 0:
							cooccurrence[pair] += 1

	cooccurrence_df = pd.DataFrame.from_dict(cooccurrence, orient='index', columns=["Frequency"])
	cooccurrence_df["Frequency"] = (cooccurrence_df["Frequency"] / 200) * 100

	cooccurrence_df = cooccurrence_df.reset_index()
	cooccurrence_df[['Sentence Type 1', 'Sentence Type 2']] = pd.DataFrame(cooccurrence_df['index'].tolist(), index=cooccurrence_df.index)
	cooccurrence_pivot = cooccurrence_df.pivot_table(index="Sentence Type 1", columns="Sentence Type 2", values="Frequency", fill_value=0)

	plt.figure(figsize=(8, 6))
	ax = sns.heatmap(cooccurrence_pivot, annot=True, cmap="Blues", linewidths=0.5, fmt=".2f", vmax=50, vmin=0) 

	for text in ax.texts:
			text.set_text(f"{text.get_text()}%")

	plt.xlabel("Sentence Type")
	plt.ylabel("Sentence Type")

	plt.title(f"")
	plt.savefig(f"./output/coocurrence/l1_l4_coocurrence_prob_{title}.png", dpi=300)
	plt.close()


df = pd.read_csv('../data/chart_vectors_complete.csv')
df = df[["image_id", "l1_l4_vector"]]
rating = pd.read_csv('../data/average_rating.csv')
rating = rating[["image_id", "mean_rating"]]
df = pd.merge(df, rating, on="image_id")

df[["l1", "l2", "l3", "l4"]] = df["l1_l4_vector"].apply(lambda x: pd.Series(ast.literal_eval(x)))
df.drop(columns=["l1_l4_vector"], inplace=True)

generate_cooccurrence_heatmap(df, "200")
generate_cooccurrence_heatmap(df[df["mean_rating"] >= 4], "High Rated")
generate_cooccurrence_heatmap(df[df["mean_rating"] <= 2], "Low Rated")