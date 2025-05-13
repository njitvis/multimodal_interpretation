from model_handler import ModelHandler
import pandas as pd
import numpy as np
import torch
from sklearn.metrics import (
    hamming_loss,
    classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import multilabel_confusion_matrix
import ast


sentences = pd.read_csv("../all.csv")
sentences["label"] = sentences["label"].apply(lambda x: ast.literal_eval(x))

handler = ModelHandler(hidden_dim=256, num_labels=4)
handler.load_model("./bilstm.pth", "./bilstm/checkpoint/tokenizer")
y_preds = handler.test(sentences["text"].to_list())

y_true_transformed = handler.mlb.transform(sentences["label"])
y_true_tensor = torch.tensor(y_true_transformed, dtype=torch.float)
y_true = y_true_tensor.numpy()

ham_loss = hamming_loss(y_true, y_preds)
print(f"Hamming loss: {ham_loss:.4f}")
print(f"Hamming accuracy: {1 - ham_loss:.4f}")

mcm = multilabel_confusion_matrix(y_true, y_preds)
fig, axes = plt.subplots(2, 2, figsize=(5, 5))
axes = axes.flatten()

for i, ax in enumerate(axes):
    TN, FP, FN, TP = mcm[i].ravel()
    p = TP / (TP + FP)
    r = TP / (TP + FN)
    f1 = 2 * ((p*r)/ (p+r))
    sns.heatmap(
        mcm[i],
        ax=ax,
        annot=True,
        fmt="d",
        cbar=True,
        cmap="Blues",
        xticklabels=["0", "1"],
        yticklabels=["0", "1"]
    )
    ax.set_xlabel("Predicted\n")
    ax.set_ylabel("Actual")
    ax.set_title(f"\nConfusion Matrix L{i+1}\nF1 score: {f1:.2f}")

plt.tight_layout()
plt.show()


