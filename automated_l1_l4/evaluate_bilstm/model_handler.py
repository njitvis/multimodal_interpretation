import torch
import torch.nn as nn
from transformers import BertTokenizer, BertTokenizerFast
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torch.optim.lr_scheduler import StepLR
import os
import joblib

from model_def import BiLSTMWithBERT


class EarlyStopping:
    def __init__(self, patience: int = 3, min_delta: float = 0.0, path: str = "checkpoint.pth"):
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss = np.inf
        self.counter = 0
        self.path = path

    def __call__(self, val_loss: float, model: nn.Module) -> bool:
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
            torch.save(model.state_dict(), self.path)
        else:
            self.counter += 1
            if self.counter > self.patience:
                return True
        return False
    

class ModelHandler:
    def __init__(
        self,
        hidden_dim: int,
        num_labels: int
    ):
        self.hidden_dim = hidden_dim
        self.num_labels = num_labels
        self.device = torch.device("cpu")
        if torch.cuda.is_available():
            torch.cuda.set_device(0)
            self.device = torch.device("cuda:0")
        print(self.device)
        self.model = BiLSTMWithBERT(hidden_dim, num_labels).to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.mlb = MultiLabelBinarizer()

    def load_model(self, path: str, tokenizer_path: str, binarizer_path: str = "./bilstm/mlb.joblib") -> None:
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
        self.mlb = joblib.load(binarizer_path)
        state = torch.load(path, map_location=self.device)
        self.model.load_state_dict(state)
        self.model.to(self.device)
        self.model.eval()

    def train(
        self,
        texts: list[str],
        true_labels,
        epochs: int = 100,
        batch_size: int = 64,
        lr: float = 1e-4,
        binarizer_path: str = "./bilstm/mlb.joblib"
    ) -> None:
        encodings = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )
        input_ids = encodings["input_ids"]
        attention_mask = encodings["attention_mask"]

        labels = self.mlb.fit_transform(true_labels)
        labels_tensor = torch.tensor(labels, dtype=torch.float)

        joblib.dump(self.mlb, binarizer_path)
        print(f">>> Binarizer saved to {binarizer_path}")

        dataset = TensorDataset(input_ids, attention_mask, labels_tensor)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        criterion = nn.BCEWithLogitsLoss()
        optimizer = optim.Adam(
            filter(lambda p: p.requires_grad, self.model.parameters()),
            lr=lr
        )
        scheduler = StepLR(optimizer, step_size=3, gamma=0.5)
        early_stopper = EarlyStopping(patience=3, min_delta=1e-2, path="best_model.pth")

        for epoch in range(1, epochs + 1):
            self.model.train()
            total_loss = 0.0

            for batch in loader:
                ids, masks, targets = [t.to(self.device) for t in batch]
                optimizer.zero_grad()
                outputs = self.model(ids, masks)
                loss = criterion(outputs, targets)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                optimizer.step()
                total_loss += loss.item()

            scheduler.step()
            avg_loss = total_loss / len(loader)
            print(f"Epoch {epoch}, Loss: {avg_loss:.4f}")

            if early_stopper(avg_loss, self.model):
                print(f"Early stopping at epoch {epoch} (no improvement for {early_stopper.patience} epochs).")
                break

    def test(
        self,
        texts: list[str],
        threshold: float = 0.5
    ):
        encodings = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )
        input_ids = encodings["input_ids"].to(self.device)
        attention_mask = encodings["attention_mask"].to(self.device)

        self.model.eval()
        all_probs = []
        with torch.no_grad():
            logits = self.model(input_ids, attention_mask)
            probs = torch.sigmoid(logits).cpu().numpy()
            all_probs.extend(probs)
        all_probs = np.array(all_probs)
        preds = (all_probs >= 0.5).astype(int)
        return preds
    
    def save(self, path: str, tokenizer_path: str) -> None:
        torch.save(self.model.state_dict(), path)
        print(f">>> Model saved to {path}")
        os.makedirs(tokenizer_path, exist_ok=True)
        self.tokenizer.save_pretrained(tokenizer_path)
        print(f">>> Tokenizer saved to {tokenizer_path}")
