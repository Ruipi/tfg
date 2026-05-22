"""
Tile decoding utilities for Riichi Mahjong.
"""

# --------------------------------------------------
# TILE NAMES
# --------------------------------------------------

TILE_NAMES = [
    # Manzu
    "1m", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "9m",

    # Pinzu
    "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p",

    # Souzu
    "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",

    # Honors
    "east", "south", "west", "north",
    "white", "green", "red"
]


# --------------------------------------------------
# CONVERSIONS
# --------------------------------------------------

def tile136_to_tile34(tile_id: int) -> int:
    """
    Convert 136-tile ID into 34-tile class.
    """
    return tile_id // 4


def tile34_to_string(tile34: int) -> str:
    """
    Convert 34-tile class into string.
    """
    return TILE_NAMES[tile34]


def tile136_to_string(tile136: int) -> str:
    """
    Convert 136-tile ID into string.
    """
    tile34 = tile136_to_tile34(tile136)
    return tile34_to_string(tile34)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def decode_tiles(tiles):
    """
    Decode list of tiles.
    """
    return [
        tile136_to_string(t)
        for t in tiles
    ]


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    sample_tiles = [0, 5, 33, 108, 133]

    print(decode_tiles(sample_tiles))