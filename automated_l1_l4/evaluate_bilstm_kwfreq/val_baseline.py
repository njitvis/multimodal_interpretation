from model_handler import ModelHandler
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
import torch
from sklearn.metrics import (
    hamming_loss,
    classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns


sentences = pd.read_csv("../label_train.csv")
sentences['semantic_level'] = sentences['semantic_level'].apply(lambda x: [f"L{x}"])

split = StratifiedShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
for train_index, sample_index in split.split(sentences, sentences['semantic_level']):
    test_sentences = sentences.iloc[sample_index]
train_sentences = sentences.drop(test_sentences.index)

handler = ModelHandler(hidden_dim=128, num_labels=4)
handler.load_model("./bilstm.pth")
y_preds, y_pred_label = handler.test(test_sentences["sentence"].to_list(), test_sentences["semantic_level"])

y_true_transformed = handler.mlb.transform(test_sentences["semantic_level"])
y_true_tensor = torch.tensor(y_true_transformed, dtype=torch.float)
y_true = y_true_tensor.numpy()

ham_loss = hamming_loss(y_true, y_preds)
print(f"Hamming loss: {ham_loss:.4f}")
print(f"Hamming accuracy: {1 - ham_loss:.4f}")

target_names = [str(c) for c in handler.mlb.classes_]
print("\nClassification report (per label):")
report_dict = classification_report(
    y_true,
    y_preds,
    target_names=[str(c) for c in handler.mlb.classes_],
    output_dict=True,
    zero_division=0
)

df_report = pd.DataFrame(report_dict).T

df_plot = df_report.drop(index=['micro avg', 'macro avg', 'weighted avg', 'samples avg'])

plt.figure(figsize=(8, 6))
sns.heatmap(
    df_plot.iloc[:, :3],
    annot=True,
    fmt=".2f",
    cmap="Blues",
    cbar_kws={'label': 'Score'}
)
plt.title("Per-Label Precision / Recall / F1-Score")
plt.ylabel("Labels")
plt.xlabel("Metrics")
plt.tight_layout()
plt.show()

print(df_report.T[['micro avg', 'macro avg', 'weighted avg', 'samples avg']])
