"""
Action decoding utilities for Riichi Mahjong.
"""

from src.utils.tile_decoder import tile136_to_string


# --------------------------------------------------
# ACTION TYPE MAPPING
# --------------------------------------------------

ACTION_TYPES = {
    0: "skip",
    1: "discard",
    2: "chi",
    3: "pon",
    4: "daiminkan",
    5: "shouminkan",
    6: "ankan",
    7: "riichi"
}


# --------------------------------------------------
# SINGLE ACTION DECODER
# --------------------------------------------------

def decode_action(action: dict) -> str:
    """
    Convert action dictionary into readable text.
    """

    action_type = ACTION_TYPES.get(
        action["type"],
        f"unknown({action['type']})"
    )

    tiles = [
        t for t in action["tiles"]
        if t != -1
    ]

    decoded_tiles = [
        tile136_to_string(t)
        for t in tiles
    ]

    return f"{action_type}: {decoded_tiles}"


# --------------------------------------------------
# MULTIPLE ACTIONS
# --------------------------------------------------

def decode_actions(actions):
    """
    Decode list of actions.
    """

    return [
        decode_action(a)
        for a in actions
    ]


# --------------------------------------------------
# DEBUG / TEST
# --------------------------------------------------

if __name__ == "__main__":

    sample_action = {
        "tiles": [108, -1, -1, -1],
        "type": 1,
        "who": [1, -1, -1, -1]
    }

    print(decode_action(sample_action))
    