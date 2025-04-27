import pandas as pd
import numpy as np
import ast
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler


usefulness = pd.read_csv("../qualitative_analysis/data/reasons_caption_segment.csv")
usefulness.drop(columns=["rating", "reason", "feature"], inplace=True)
usefulness = usefulness[usefulness["usefulness"] != "neutral"]

semantic_structure = pd.read_csv("../data/chart_vectors_complete.csv")
semantic_structure.drop(columns=["l1_l4_vector_weighted", "l1_l4_cluster",  "keyword_vector_weighted", "keyword_vector", "keyword_cluster"], inplace=True)


df = pd.merge(usefulness, semantic_structure, on="image_id", how="left")

def parse_norm(vec_str):
    counts = ast.literal_eval(vec_str) 
    total = sum(counts)
    return [c / total if total>0 else 0 for c in counts]

df[['l1','l2','l3','l4']] = df['l1_l4_vector'].apply(parse_norm).apply(pd.Series)

df[['l1','l2','l3','l4']] = df[['l1','l2','l3','l4']].replace(0, 1e-6)
df["useful_bin"] = df["usefulness"].map({"useful": 1, "not_useful": 0})

df['gm'] = (df[['l1','l2','l3','l4']].prod(axis=1))**(1/4)

# 3) CLR transform
for j in range(1,5):
    df[f'clr_l{j}'] = np.log(df[f'l{j}'] / df['gm'])

# 4) standardize CLR features
X_raw = df[[f'clr_l{j}' for j in range(1,5)]]
scaler = StandardScaler().fit(X_raw)
Xs = scaler.transform(X_raw)

# 5) fit a ridge‐penalized logistic (via statsmodels’ fit_regularized)
X_design = sm.add_constant(Xs)
y = df['useful_bin']

model_clr = sm.Logit(y, X_design)
res_clr  = model_clr.fit_regularized(alpha=1.0, L1_wt=0.0)  
print("Intercept:", res_clr.params[0])
for i,coef in enumerate(res_clr.params[1:], start=1):
    print(f"clr_l{i} coef = {coef:.3f}")
    
print()
for i,coef in enumerate(res_clr.params[1:], start=1):
    if coef == 0:
        print(f"L{i} shows no distinct effect once the others are accounted for.")
    else:
        print(f"increasing proportion of L{i} sentence {"increases" if coef > 0 else "decreases"} usefulness by {np.exp(coef):.3f}")
