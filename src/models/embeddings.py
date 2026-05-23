import torch
import torch.nn as nn

from src.utils.constants import (
    TOKEN_TYPES,
    ACTION_TYPE_IDS,
)

# ============================================================
# VOCAB SIZES
# ============================================================

TOKEN_TYPE_VOCAB_SIZE = 7

TILE_VOCAB_SIZE = 35
# 34 tiles + PAD

COPY_VOCAB_SIZE = 5
# 0-3 + PAD

PLAYER_VOCAB_SIZE = 5
# 0-3 + PAD

ACTION_TYPE_VOCAB_SIZE = 13
# 0-11 + PAD

POSITION_VOCAB_SIZE = 512
# More than enough initially

class MahjongEmbedding(nn.Module):

    def __init__(self, embedding_dim=128):

        super().__init__()

        self.embedding_dim = embedding_dim

        self.token_type_embedding = nn.Embedding(
            TOKEN_TYPE_VOCAB_SIZE,
            embedding_dim,
        )

        self.tile_embedding = nn.Embedding(
            TILE_VOCAB_SIZE,
            embedding_dim,
        )

        self.copy_embedding = nn.Embedding(
            COPY_VOCAB_SIZE,
            embedding_dim,
        )

        self.player_embedding = nn.Embedding(
            PLAYER_VOCAB_SIZE,
            embedding_dim,
        )

        self.action_type_embedding = nn.Embedding(
            ACTION_TYPE_VOCAB_SIZE,
            embedding_dim,
        )

        self.position_embedding = nn.Embedding(
            POSITION_VOCAB_SIZE,
            embedding_dim,
        )
    
    def forward(self, batch):

        token_type_emb = self.token_type_embedding(
            batch["token_type_ids"]
        )

        tile_emb = self.tile_embedding(
            batch["tile_ids"]
        )

        copy_emb = self.copy_embedding(
            batch["copy_ids"]
        )

        player_emb = self.player_embedding(
            batch["player_ids"]
        )

        action_emb = self.action_type_embedding(
            batch["action_type_ids"]
        )

        position_emb = self.position_embedding(
            batch["positions"]
        )

        embeddings = (
            token_type_emb
            + tile_emb
            + copy_emb
            + player_emb
            + action_emb
            + position_emb
        )

        return embeddings