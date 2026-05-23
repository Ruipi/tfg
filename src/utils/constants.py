"""
Shared constants for Riichi Mahjong project.
"""

ACTION_TYPES = {
    0: "skip",
    1: "discard",
    2: "chi",
    3: "pon",
    4: "daiminkan",
    5: "shouminkan",
    6: "ankan",
    7: "riichi",
    8: "ron",
    9: "tsumo",
    10: "kyuushukyuuhai",
    11: "chankan"
}

# ============================================================
# TOKEN TYPE IDS
# ============================================================

TOKEN_TYPES = {
    "GAME_STATE": 0,
    "PLAYER_STATE": 1,
    "HAND": 2,
    "DISCARD": 3,
    "MELD": 4,
    "ACTION": 5,
    "PAD": 6,
}


# ============================================================
# ACTION TYPE IDS
# ============================================================

ACTION_TYPE_IDS = {
    "skip": 0,
    "discard": 1,
    "chi": 2,
    "pon": 3,
    "daiminkan": 4,
    "shouminkan": 5,
    "ankan": 6,
    "riichi": 7,
    "ron": 8,
    "tsumo": 9,
    "kyuushukyuuhai": 10,
    "chankan": 11,
}


# ============================================================
# MELD TYPE IDS
# ============================================================

MELD_TYPE_IDS = ACTION_TYPE_IDS.copy()