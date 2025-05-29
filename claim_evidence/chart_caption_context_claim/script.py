import pandas as pd

captions = pd.read_csv("./captions.csv")
captions = captions[["image_id", "caption"]]

context = pd.read_csv("./context.csv")
context = context[["image_id", "context"]]
context.drop_duplicates(subset=["image_id"], inplace=True)

claims = pd.read_csv("./claims.csv")
print("claims: ", claims.shape)

captions = captions[captions["image_id"].isin(claims["image_id"])]
context = context[context["image_id"].isin(claims["image_id"])]
print("captions: ", captions.shape)
print("context: ", context.shape)

all = pd.merge(claims, captions, on="image_id", how="inner")
all = pd.merge(all, context, on="image_id", how="inner")
print("all: ", all.shape)

all.to_csv("./all.csv")