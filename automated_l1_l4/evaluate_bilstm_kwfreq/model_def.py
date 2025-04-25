import torch
import torch.nn as nn
from transformers import BertModel


class BiLSTMWithBERTkwfreq(nn.Module):
    """Bi-directional LSTM on top of BERT embeddings with keyword feature."""

    def __init__(self, hidden_dim: int, num_labels: int):
        super().__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased")
        self.lstm = nn.LSTM(
            input_size=768,
            hidden_size=hidden_dim,
            bidirectional=True,
            batch_first=True
        )
        self.dropout = nn.Dropout(0.3)
        self.fc = nn.Linear(hidden_dim * 2, num_labels)

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        bert_out = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        embeddings = bert_out.last_hidden_state
        lstm_out, _ = self.lstm(embeddings)
        pooled = torch.max(lstm_out, dim=1).values
        dropped = self.dropout(pooled)
        logits = self.fc(dropped)
        return logits


