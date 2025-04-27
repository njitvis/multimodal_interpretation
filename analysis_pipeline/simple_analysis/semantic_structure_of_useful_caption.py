import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns


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

useful = merged[merged["usefulness"] == "useful"]
not_useful = merged[merged["usefulness"] == "not_useful"]


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 12), sharey=True)

sns.heatmap(
    useful[['l1','l2','l3','l4']].astype(float),
    ax=axes[0],
    cmap="Blues",
    vmin=0, vmax=1,
    cbar_kws={'label': 'Proportion'},
    xticklabels=['l1','l2','l3','l4'],
    yticklabels=False,
    linewidths=0.1,
    linecolor='white',
    square=False
)
axes[0].set_title("Useful Captions\nSemantic Level Distribution")
axes[0].set_xlabel("Semantic Level")
axes[0].set_ylabel("Reason Index")

sns.heatmap(
    not_useful[['l1','l2','l3','l4']].astype(float),
    ax=axes[1],
    cmap="Blues",
    vmin=0, vmax=1,
    cbar_kws={'label': 'Proportion'},
    xticklabels=['l1','l2','l3','l4'],
    yticklabels=False,
    linewidths=0.1,
    linecolor='white',
    square=False
)
axes[1].set_title("Not-Useful Captions\nSemantic Level Distribution")
axes[1].set_xlabel("Semantic Level")
axes[1].set_ylabel("") 

plt.tight_layout()
plt.savefig("./output/semantic_level_heatmaps.png", dpi=300)
plt.show()