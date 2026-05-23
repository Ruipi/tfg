"""
Meld decoding utilities for Riichi Mahjong.
"""

from src.utils.tile_decoder import (
    tile136_to_string
)

from src.utils.constants import ACTION_TYPES

# --------------------------------------------------
# SINGLE MELD DECODER
# --------------------------------------------------

def decode_meld(meld: dict) -> str:
    """
    Convert meld dictionary into readable string.
    """

    meld_type = MELD_TYPES.get(
        meld["type"],
        f"unknown({meld['type']})"
    )

    tiles = [
        t for t in meld["tiles"]
        if t != -1
    ]

    decoded_tiles = [
        tile136_to_string(t)
        for t in tiles
    ]

    return f"{meld_type}: {decoded_tiles}"


# --------------------------------------------------
# MULTIPLE MELDS
# --------------------------------------------------

def decode_melds(melds):
    """
    Decode list of melds.
    """

    return [
        decode_meld(m)
        for m in melds
    ]


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    sample = {
        'type': 2,
        'tiles': [92, 98, 103, -1],
        'who': [0, 0, 3, -1]
    }

    print(decode_meld(sample))