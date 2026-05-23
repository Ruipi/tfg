import torch
import torch.nn as nn

from src.models.embeddings import MahjongEmbedding

class MahjongTransformer(nn.Module):

    def __init__(
        self,
        embedding_dim=128,
        num_heads=8,
        num_layers=4,
        ff_dim=512,
        dropout=0.1,
    ):

        super().__init__()

        self.embedding_layer = MahjongEmbedding(
            embedding_dim=embedding_dim
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_dim,

            nhead=num_heads,

            dim_feedforward=ff_dim,

            dropout=dropout,

            batch_first=True,
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers,
        )

        self.policy_head = nn.Linear(
            embedding_dim,
            1,
        )

    def forward(self, batch):

        embeddings = self.embedding_layer(batch)

        padding_mask = (
            batch["attention_mask"] == 0
        )

        hidden_states = self.transformer(
            embeddings,

            src_key_padding_mask=padding_mask,
        )

        batch_action_logits = []

        for batch_idx in range(
            hidden_states.shape[0]
        ):

            action_positions = batch[
                "action_indices"
            ][batch_idx]

            action_hidden = hidden_states[
                batch_idx,
                action_positions,
            ]

            logits = self.policy_head(
                action_hidden
            ).squeeze(-1)

            batch_action_logits.append(
                logits
            )

        return batch_action_logits