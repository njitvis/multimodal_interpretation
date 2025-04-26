from model_handler import ModelHandler
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
from util import compute_category_vector


sentences = pd.read_csv("../label_train.csv")
sentences['semantic_level'] = sentences['semantic_level'].apply(lambda x: [f"L{x}"])
sentences['kw_freqs'] = sentences['sentence'].apply(
    lambda s: compute_category_vector(s)
)

split = StratifiedShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
for train_index, sample_index in split.split(sentences, sentences['semantic_level'], sentences['kw_freqs']):
    test_sentences = sentences.iloc[sample_index]
train_sentences = sentences.drop(test_sentences.index)

handler = ModelHandler(hidden_dim=128, num_labels=4, num_categories=8)
handler.train(texts=train_sentences["sentence"].to_list(), true_labels=train_sentences["semantic_level"], kw_vec=train_sentences["kw_freqs"], lr=6e-5, batch_size=16)
handler.save("./bilstm_kwfreq.pth", "./bilstm_kwfreq/checkpoint/tokenizer")

# import optuna
# import torch.nn.functional as F
# from torch.utils.data import DataLoader
# from sklearn.metrics import (
#     hamming_loss,
#     classification_report
# )
# import torch

# def objective(trial):
#     hidden_dim = trial.suggest_categorical("hidden_dim", [128, 256, 512])
#     lr = trial.suggest_loguniform("lr", 1e-5, 1e-3)
#     batch_size = trial.suggest_categorical("batch_size", [16, 32, 64])

#     handler = ModelHandler(hidden_dim=hidden_dim, num_labels=4, num_categories=8)
#     handler.train(texts=train_sentences["sentence"].to_list(), true_labels=train_sentences["semantic_level"], kw_vec=train_sentences["kw_freqs"].to_list(), lr=lr, batch_size=batch_size)
#     y_preds = handler.test(texts=test_sentences["sentence"].to_list(), kw_vec=test_sentences["kw_freqs"].to_list())
#     y_true_transformed = handler.mlb.transform(test_sentences["semantic_level"])
#     y_true_tensor = torch.tensor(y_true_transformed, dtype=torch.float)
#     y_true = y_true_tensor.numpy()
#     ham_loss = hamming_loss(y_true, y_preds)
#     return ham_loss

# study = optuna.create_study(direction="minimize")
# study.optimize(objective, n_trials=20)
