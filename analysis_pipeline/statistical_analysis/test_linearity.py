import pandas as pd
import numpy as np
import ast
import statsmodels.api as sm

usefulness = pd.read_csv("../qualitative_analysis/data/reasons_caption_segment.csv")
usefulness.drop(columns=["rating", "reason", "feature"], inplace=True)
usefulness = usefulness[usefulness["usefulness"] != "neutral"]

semantic_structure = pd.read_csv("../data/chart_vectors_complete.csv")
semantic_structure.drop(columns=["l1_l4_vector_weighted", "l1_l4_cluster",  "keyword_vector_weighted", "keyword_vector", "keyword_cluster"], inplace=True)


df = pd.merge(usefulness, semantic_structure, on="image_id", how="left")

def parse_norm(vec_str):
    counts = ast.literal_eval(vec_str)
    total = sum(counts)
    return [c / total if total > 0 else 0 for c in counts]

df[['l1', 'l2', 'l3', 'l4']] = (
    df['l1_l4_vector']
      .apply(parse_norm)
      .apply(pd.Series)
)

for col in ['l1', 'l2', 'l3']:
    df[col] = df[col].replace(0, 1e-6)

for col in ['l1', 'l2', 'l3']:
    df[f'{col}_log'] = df[col] * np.log(df[col])

df['useful_bin'] = df['usefulness'].map({'useful': 1, 'not_useful': 0})
predictors = ['l1', 'l2', 'l3']
interaction_terms = [f'{col}_log' for col in predictors]

X = df[predictors + interaction_terms]
X = sm.add_constant(X)
y = df['useful_bin']

model_bt = sm.Logit(y, X).fit(disp=False)
print(model_bt.summary())
