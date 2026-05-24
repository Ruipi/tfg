import torch

from src.utils.constants import (
    PAD_TOKEN_ID,
    PAD_TILE_ID,
    PAD_COPY_ID,
    PAD_PLAYER_ID,
    PAD_ACTION_TYPE_ID,
)

class MahjongCollator:

    def __init__(self):
        pass

    def collate(self, batch):

        max_len = max(
            sample["token_type_ids"].shape[0]
            for sample in batch
        )

        batched = {
            "token_type_ids": [],
            "tile_ids": [],
            "copy_ids": [],
            "player_ids": [],
            "action_type_ids": [],
            "positions": [],
            "attention_mask": [],
            "action_mask": [],
            "action_indices": [],
            "target": [],
        }

        # ========================================================
        # Pad each sample
        # ========================================================

        for sample in batch:

            seq_len = sample["token_type_ids"].shape[0]

            attention_mask = torch.ones(seq_len)

            # ====================================================
            # Pad fields
            # ====================================================

            batched["token_type_ids"].append(
                self._pad_1d_tensor(
                    sample["token_type_ids"],
                    max_len,
                    PAD_TOKEN_ID,
                )
            )

            batched["tile_ids"].append(
                self._pad_1d_tensor(
                    sample["tile_ids"],
                    max_len,
                    PAD_TILE_ID,
                )
            )

            batched["copy_ids"].append(
                self._pad_1d_tensor(
                    sample["copy_ids"],
                    max_len,
                    PAD_COPY_ID,
                )
            )

            batched["player_ids"].append(
                self._pad_1d_tensor(
                    sample["player_ids"],
                    max_len,
                    PAD_PLAYER_ID,
                )
            )

            batched["action_type_ids"].append(
                self._pad_1d_tensor(
                    sample["action_type_ids"],
                    max_len,
                    PAD_ACTION_TYPE_ID,
                )
            )

            batched["positions"].append(
                self._pad_1d_tensor(
                    sample["positions"],
                    max_len,
                    0,
                )
            )

            batched["action_mask"].append(
                self._pad_1d_tensor(
                    sample["action_mask"],
                    max_len,
                    0,
                )
            )

            batched["attention_mask"].append(
                self._pad_1d_tensor(
                    attention_mask,
                    max_len,
                    0,
                )
            )

            # ====================================================
            # Action indices remain variable-length for now
            # ====================================================

            batched["action_indices"].append(
                sample["action_indices"]
            )

            if "target" in sample:

                batched["target"].append(
                    sample["target"]
                )

        # ========================================================
        # Stack tensors
        # ========================================================

        for key in batched:

            if key in ["action_indices", "target"]:
                continue

            batched[key] = torch.stack(
                batched[key],
                dim=0,
            )

        if len(batched["target"]) > 0:
            batched["target"] = torch.tensor(
                batched["target"]
            )

        return batched
    
    def _pad_1d_tensor(
        self,
        tensor,
        target_length,
        pad_value,
    ):

        pad_size = target_length - tensor.shape[0]

        if pad_size <= 0:
            return tensor

        padding = torch.full(
            (pad_size,),
            pad_value,
            dtype=tensor.dtype,
        )

        return torch.cat([tensor, padding], dim=0)
