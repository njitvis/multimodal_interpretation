import matplotlib.pyplot as plt
import pandas as pd

captions = pd.read_csv("../data/captions.csv")

def save_vis(file):
	ratings = pd.read_csv(f"../data/average_rating{file}.csv")
	df = pd.merge(captions, ratings, on="image_id", how="right")
	df = df[["image_id", "caption", "mean_rating"]]

	df['caption_length_rounded'] = df['caption'].apply(lambda x: round(len(x.split()), -1))
	grouped = df.groupby('caption_length_rounded')['mean_rating'].mean().reset_index()

	plt.plot(grouped['caption_length_rounded'], grouped['mean_rating'], marker='o')

	plt.xlabel('Caption Word Count (Rounded to Nearest 10)')
	plt.ylabel('Average Interpretability Rating')
	plt.title('Rounded Caption Length vs Average Interpretability Rating')
	plt.grid(True)
	plt.savefig(f"./output/rating_vs/rating_vs_length{file}.png", dpi=300)
	plt.close()

files = ["_rest", "_ug", ""]
for file in files:
	save_vis(file)