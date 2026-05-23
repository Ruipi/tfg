"""
Canonical Mahjong state extraction.
"""

from src.utils.tile_decoder import (
    tile136_to_tile34
)


# --------------------------------------------------
# TILE HELPERS
# --------------------------------------------------

def tiles136_to_34(tiles):
    """
    Convert list of 136-tile IDs
    into 34-tile classes.
    """

    return [
        tile136_to_tile34(t)
        for t in tiles
        if t != -1
    ]


# --------------------------------------------------
# PLAYER EXTRACTION
# --------------------------------------------------

def extract_player_state(player_data):
    """
    Extract canonical player state.
    """

    return {
        "points": player_data["points"],

        "riichi": player_data["riichi"],

        "discards": tiles136_to_34(
            player_data["discards"]
        ),

        "melds": player_data["melds"],

        "tsumo_giri": player_data["tsumo_giri"]
    }


# --------------------------------------------------
# ACTION EXTRACTION
# --------------------------------------------------

def extract_action(action):
    """
    Extract canonical action representation.
    """

    return {
        "type": action["type"],

        "tiles": tiles136_to_34(
            action["tiles"]
        ),

        "who": action["who"]
    }


# --------------------------------------------------
# MAIN STATE EXTRACTION
# --------------------------------------------------

def extract_state_features(sample):
    """
    Convert raw dataset sample
    into canonical structured state.
    """

    state = {

        # ------------------------------------------
        # Global features
        # ------------------------------------------

        "round_wind": sample["round_wind"],

        "num_honba": sample["num_honba"],

        "num_riichi": sample["num_riichi"],

        "player_wind": sample["player_wind"],

        "position": sample["position"],

        "remain_tiles": sample["remain_tiles"],

        # ------------------------------------------
        # Tile features
        # ------------------------------------------

        "dora_indicators": tiles136_to_34(
            sample["dora_indicators"]
        ),

        "hand_tiles": tiles136_to_34(
            sample["hand_tiles"]
        ),

        # ------------------------------------------
        # Players
        # ------------------------------------------

        "players": {

            pid: extract_player_state(
                sample[pid]
            )

            for pid in ["0", "1", "2", "3"]
        },

        # ------------------------------------------
        # Actions
        # ------------------------------------------

        "valid_actions": [

            extract_action(a)

            for a in sample["valid_actions"]
        ],

        "action_idx": sample["action_idx"]
    }

    return state