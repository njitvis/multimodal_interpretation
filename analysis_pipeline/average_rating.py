import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


df1 = pd.read_csv("./data/average_rating_rest.csv")
df2 = pd.read_csv("./data/average_rating_ug.csv")
df = pd.merge(df1, df2, on="image_id")
df["mean_rating"] = (df["interpretability_rating_res1"] + df["interpretability_rating_res2"] + df["interpretability_rating_u_res1"] + df["interpretability_rating_u_res2"]) / 4
df.drop(columns=['mean_rating_x', 'mean_rating_y'], inplace=True)
df.to_csv("./data/average_rating.csv", index=False)
