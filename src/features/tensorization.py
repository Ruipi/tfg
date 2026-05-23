import torch

from src.features.token_definitions import (
    GameStateToken,
    PlayerStateToken,
    HandToken,
    DiscardToken,
    MeldToken,
    ActionToken,
)

from src.utils.constants import (
    TOKEN_TYPES,
    ACTION_TYPE_IDS,
    MELD_TYPE_IDS,

    PAD_TILE_ID,
    PAD_COPY_ID,
    PAD_PLAYER_ID,
    PAD_ACTION_TYPE_ID,
)

class Tensorizer:

    def __init__(self):
        pass

    def tensorize(self, tokens):

        token_type_ids = []

        tile_ids = []

        copy_ids = []

        player_ids = []

        action_type_ids = []

        positions = []

        action_mask = []

        action_indices = []

        # ========================================================
        # Iterate through semantic tokens
        # ========================================================

        for position, token in enumerate(tokens):

            # ====================================================
            # TOKEN TYPE
            # ====================================================

            token_type_ids.append(
                TOKEN_TYPES[token.token_type]
            )

            positions.append(position)

            # ========================================================
            # DEFAULT VALUES
            # ========================================================

            tile_ids.append(PAD_TILE_ID)

            copy_ids.append(PAD_COPY_ID)

            player_ids.append(PAD_PLAYER_ID)

            action_type_ids.append(PAD_ACTION_TYPE_ID)

            action_mask.append(0)

            # ====================================================
            # HAND TOKENS
            # ====================================================

            if isinstance(token, HandToken):

                tile_ids[-1] = token.tile.tile_type

                copy_ids[-1] = token.tile.copy_index

            # ====================================================
            # DISCARD TOKENS
            # ====================================================

            elif isinstance(token, DiscardToken):

                tile_ids[-1] = token.tile.tile_type

                copy_ids[-1] = token.tile.copy_index

                player_ids[-1] = token.player

            # ====================================================
            # MELD TOKENS
            # ====================================================

            elif isinstance(token, MeldToken):

                player_ids[-1] = token.player

                action_type_ids[-1] = (
                    MELD_TYPE_IDS[token.meld_type]
                )

            # ====================================================
            # ACTION TOKENS
            # ====================================================

            elif isinstance(token, ActionToken):

                action_type_ids[-1] = (
                    ACTION_TYPE_IDS[token.action_type]
                )

                action_mask[-1] = 1

                action_indices.append(position)

                if len(token.tiles) > 0:

                    tile_ids[-1] = (
                        token.tiles[0].tile_type
                    )

                    copy_ids[-1] = (
                        token.tiles[0].copy_index
                    )

        # ========================================================
        # Convert to tensors
        # ========================================================

        return {
            "token_type_ids": torch.tensor(token_type_ids),

            "tile_ids": torch.tensor(tile_ids),

            "copy_ids": torch.tensor(copy_ids),

            "player_ids": torch.tensor(player_ids),

            "action_type_ids": torch.tensor(action_type_ids),

            "positions": torch.tensor(positions),

            "action_mask": torch.tensor(action_mask),

            "action_indices": torch.tensor(action_indices),
        }