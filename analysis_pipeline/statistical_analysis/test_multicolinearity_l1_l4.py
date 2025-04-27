from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd
from statsmodels.tools.tools import add_constant
import ast
import numpy as np


usefulness = pd.read_csv("../qualitative_analysis/data/reasons_caption_segment.csv")
usefulness.drop(columns=["rating", "reason", "feature"], inplace=True)
usefulness = usefulness[usefulness["usefulness"] != "neutral"]

semantic_structure = pd.read_csv("../data/chart_vectors_complete.csv")
semantic_structure.drop(columns=["l1_l4_vector_weighted", "l1_l4_cluster",  "keyword_vector_weighted", "keyword_vector", "keyword_cluster"], inplace=True)


merged = pd.merge(usefulness, semantic_structure, on="image_id", how="left")

def parse_norm(vec_str):
    counts = ast.literal_eval(vec_str) 
    total = sum(counts)
    return [c / total if total>0 else 0 for c in counts]

merged[['l1','l2','l3','l4']] = merged['l1_l4_vector'].apply(parse_norm).apply(pd.Series)
merged_cleaned = merged[merged['usefulness'] != 'neutral'].copy()


merged_cleaned[['l1','l2','l3','l4']] = merged_cleaned[['l1','l2','l3','l4']].replace(0, 1e-6)

merged_subset = merged_cleaned[['l1','l2','l3','l4']]

X = merged_subset
X = add_constant(X)

vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)