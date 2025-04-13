import pandas as pd

captions = pd.read_csv("./data/captions.csv")
vectors = pd.read_csv("./data/chart_vectors_complete.csv")
cc = pd.read_csv("./data/claim_evidence_interpretation.csv")
rating = pd.read_csv("./data/average_rating.csv")

df = pd.merge(vectors, captions, on='image_id', how="inner")
df = pd.merge(df, cc, on='image_id', how="left")
df = pd.merge(df, rating, on='image_id', how="left")

df.drop(columns=["l1_l4_vector_weighted", "domain", "caption",
                 "keyword_vector_weighted", 'interpretability_rating_res1', 'interpretability_rating_res2',
       'interpretability_rating_u_res1', 'interpretability_rating_u_res2',
                 "source", "views"], inplace=True)

df.to_csv("./data/download.csv", index=False)