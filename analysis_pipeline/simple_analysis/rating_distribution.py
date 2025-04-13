import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def save_distribution(file):
	df = pd.read_csv(f"../data/average_rating{file}.csv")

	plt.figure(figsize=(8, 6))
	sns.histplot(data=df, x="mean_rating", bins=8, kde=False)
	plt.title("Distribution of Mean Rating")
	plt.xlabel("Mean Rating")
	plt.ylabel("Frequency")
	plt.savefig(f"./output/rating_vs/rating_distribution{file}.png", dpi=300)
	plt.close()


files = ["_rest", "_ug", ""]
for file in files:
	save_distribution(file)