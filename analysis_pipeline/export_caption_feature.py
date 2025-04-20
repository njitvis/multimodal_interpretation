import pandas as pd
import nltk
import re
from collections import Counter


CAPTION_PATTERN = r'\b(fig(?:ure)?\.?\s*\d+(?:\.\d+)?[a-zA-Z0-9\.-]*\s*(?:[:\-]?\s*\(\s*[a-zA-Z0-9\.-]+\s*\))?[:\-]?)\s*'

def remove_captions(text):
    return re.sub(CAPTION_PATTERN, '', text, flags=re.IGNORECASE)

nltk.download('punkt_tab')

captions = pd.read_csv("./data/captions.csv")
vectors = pd.read_csv("./data/chart_vectors_complete.csv")
cc = pd.read_csv("./data/claim_evidence_interpretation.csv")
rating = pd.read_csv("./data/average_rating.csv")

df = pd.merge(vectors, captions, on='image_id', how="inner")
df = pd.merge(df, cc, on='image_id', how="left")
df = pd.merge(df, rating, on='image_id', how="left")
df['sentence_count'] = df['caption'].apply(lambda x: len(nltk.sent_tokenize(remove_captions(x))))

def compute_agreement(labels):
    counts = Counter(labels)
    return len(counts)
df['Agreement'] = df[['interpretability_rating_phd_res1', 'interpretability_rating_phd_res2',
       'interpretability_rating_u_res1', 'interpretability_rating_u_res2']].apply(compute_agreement, axis=1)

df.drop(columns=['l1_l4_vector_weighted', 'l1_l4_cluster',
       'keyword_vector_weighted', 'keyword_cluster',
       'source', 'caption', 'Unnamed: 0',
       'interpretability_rating_phd_res1', 'interpretability_rating_phd_res2',
       'interpretability_rating_u_res1', 'interpretability_rating_u_res2'], inplace=True)

df.to_csv("./data/download.csv", index=False)