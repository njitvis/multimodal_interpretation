import torch
import torch.nn as nn
from transformers import BertModel
import torch.nn.functional as F

class BiLSTMWithBERT(nn.Module):
    """Bi-directional LSTM on top of BERT embeddings, + keyword-frequency branch."""

    def __init__(self, hidden_dim: int, num_labels: int, num_categories: int):
        super().__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased")
        self.lstm = nn.LSTM(
            input_size=768,
            hidden_size=hidden_dim,
            bidirectional=True,
            batch_first=True
        )
        self.dropout_text = nn.Dropout(0.3)

        self.fc_kw1    = nn.Linear(num_categories, 32)
        self.dropout_kw = nn.Dropout(0.3)
        self.fc_kw2    = nn.Linear(32, 16)

        combined_dim = hidden_dim * 2 + 16
        self.dropout_combined = nn.Dropout(0.3)
        self.fc = nn.Linear(combined_dim, num_labels)

    def forward(self,
                input_ids: torch.Tensor,
                attention_mask: torch.Tensor,
                kw_freq: torch.Tensor
               ) -> torch.Tensor:
        bert_out    = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        embeddings  = bert_out.last_hidden_state                   
        lstm_out, _ = self.lstm(embeddings)                       
        pooled      = torch.max(lstm_out, dim=1).values       
        t = self.dropout_text(pooled)

        k = F.relu(self.fc_kw1(kw_freq))                         
        k = self.dropout_kw(k)
        k = F.relu(self.fc_kw2(k))                        

        combined = torch.cat([t, k], dim=1)                     
        combined = self.dropout_combined(combined)
        logits   = self.fc(combined)                          
        return logits
