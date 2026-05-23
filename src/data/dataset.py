import sqlite3
import gzip
import json

from torch.utils.data import Dataset

from src.data.tokenizer import MahjongTokenizer

from src.features.tensorization import Tensorizer

class MahjongDataset(Dataset):

    def __init__(
        self,
        db_path,
        table_name="Discard",
        limit=None,
        offset=0,
    ):

        self.db_path = db_path

        self.table_name = table_name

        self.tokenizer = MahjongTokenizer()

        self.tensorizer = Tensorizer()

        self.conn = sqlite3.connect(
            self.db_path
        )

        self.cursor = self.conn.cursor()

        count_query = f"""
        SELECT COUNT(*)
        FROM {self.table_name}
        """

        total_count = self.cursor.execute(
            count_query
        ).fetchone()[0]

        if limit is not None:

            self.length = min(
                limit,
                total_count - offset,
            )

        else:

            self.length = total_count - offset

        self.offset = offset

    def __len__(self):

        return self.length

    def __getitem__(self, idx):

        query = f"""
        SELECT Data
        FROM {self.table_name}
        LIMIT 1 OFFSET {idx + self.offset}
        """

        row = self.cursor.execute(
            query
        ).fetchone()

        blob = row[0]

        decoded = json.loads(
            gzip.decompress(blob)
        )

        canonical_state = {
            "round_wind": decoded["round_wind"],
            "num_honba": decoded["num_honba"],
            "num_riichi": decoded["num_riichi"],
            "player_wind": decoded["player_wind"],
            "position": decoded["position"],
            "remain_tiles": decoded["remain_tiles"],

            "dora_indicators": decoded["dora_indicators"],

            "hand_tiles": decoded["hand_tiles"],

            "players": {
                "0": decoded["0"],
                "1": decoded["1"],
                "2": decoded["2"],
                "3": decoded["3"],
            },

            "valid_actions": decoded["valid_actions"],

            "action_idx": decoded["action_idx"],
        }

        tokens = self.tokenizer.tokenize(
            canonical_state
        )

        tensor_dict = self.tensorizer.tensorize(
            tokens
        )

        tensor_dict["target"] = (
            canonical_state["action_idx"]
        )

        return tensor_dict