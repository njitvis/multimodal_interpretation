import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

captions = pd.read_csv("../data/captions.csv")
vectors = pd.read_csv("../data/chart_vectors_complete.csv")
cc = pd.read_csv("../data/claim_evidence_interpretation.csv")

df = pd.merge(vectors, captions, on='image_id', how="inner")
df = pd.merge(df, cc, on='image_id', how="left")

df.drop(columns=["l1_l4_vector_weighted", "l1_l4_cluster", 
                 "keyword_vector_weighted", "keyword_cluster", 
                 "source"], inplace=True)

df['clarity'] = df['clarity'].fillna('Missing Clarity')
df['complexity'] = df['complexity'].fillna('Missing Complexity')
df['clarity_complexity'] = df['clarity'] + ' + ' + df['complexity']

plt.figure(figsize=(7, 5))
sns.countplot(x='domain', data=df)
plt.title("Domain Frequency")
plt.tight_layout()
plt.savefig("./output/domain_frequency.png", dpi=300)
plt.close()

plt.figure(figsize=(7, 5))
sns.countplot(x='chart_type', data=df)
plt.title("Chart Type Frequency")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("./output/chart_type_frequency.png", dpi=300)
plt.close()

plt.figure(figsize=(7, 5))
sns.countplot(x='views', data=df)
plt.title("Views Frequency")
plt.tight_layout()
plt.savefig("./output/views_frequency.png", dpi=300)
plt.close()

plt.figure(figsize=(8, 5))
sns.countplot(x='clarity_complexity', data=df)
plt.title("Clarity & Complexity Frequency")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("./output/clarity_complexity_frequency.png", dpi=300)
plt.close()