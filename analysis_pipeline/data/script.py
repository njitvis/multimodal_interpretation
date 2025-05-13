 import pandas as pd

captions = pd.read_csv("./captions.csv")
subset = pd.read_csv("./chart_vectors_complete.csv")

captions = captions[captions["image_id"].isin(subset["image_id"])]

captions.to_csv("./captions_subset.csv", index=False)