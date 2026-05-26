from collections import Counter

from src.analysis.shanten import (
    calculate_shanten
)

from src.utils.tile_decoder import (
    tile136_to_tile34
)

# ============================================
# VISIBLE TILE COUNTING
# ============================================

def count_visible_tiles(state):

    visible_tiles = []

    # ----------------------------------------
    # OWN HAND
    # ----------------------------------------

    visible_tiles.extend(
        state["hand_tiles"]
    )

    # ----------------------------------------
    # DORA INDICATORS
    # ----------------------------------------

    visible_tiles.extend(
        state["dora_indicators"]
    )

    # ----------------------------------------
    # PLAYERS
    # ----------------------------------------

    for player_data in state[
        "players"
    ].values():

        # discards

        visible_tiles.extend(
            player_data["discards"]
        )

        # melds

        for meld in player_data[
            "melds"
        ]:

            visible_tiles.extend(
                meld["tiles"]
            )

    # ----------------------------------------
    # CONVERT TO TILE34
    # ----------------------------------------

    visible_tile34 = [

        tile136_to_tile34(tile)

        for tile in visible_tiles
    ]

    return Counter(
        visible_tile34
    )

# ============================================
# EFFECTIVE UKEIRE
# ============================================

def calculate_ukeire(

    tiles136,

    visible_counts=None,
):

    current_shanten = calculate_shanten(
        tiles136
    )

    improving_tiles = []

    effective_ukeire = 0

    for tile34 in range(34):

        # ------------------------------------
        # SKIP EXHAUSTED TILES
        # ------------------------------------

        visible = 0

        if visible_counts is not None:

            visible = visible_counts[
                tile34
            ]

        remaining = 4 - visible

        if remaining <= 0:
            continue

        # ------------------------------------
        # TEST IMPROVEMENT
        # ------------------------------------

        fake_tile136 = tile34 * 4

        new_hand = tiles136.copy()

        new_hand.append(fake_tile136)

        new_shanten = calculate_shanten(
            new_hand
        )

        if new_shanten < current_shanten:

            improving_tiles.append(
                tile34
            )

            effective_ukeire += remaining

    return {

        "ukeire":
            effective_ukeire,

        "improving_tiles":
            improving_tiles,
    }

# ============================================
# DISCARD EVALUATION
# ============================================

def evaluate_discards_ukeire(

    state
):

    tiles136 = state["hand_tiles"]

    visible_counts = count_visible_tiles(
        state
    )

    results = []

    for i, tile in enumerate(tiles136):

        new_hand = tiles136.copy()

        removed_tile = new_hand.pop(i)

        shanten = calculate_shanten(
            new_hand
        )

        ukeire_result = calculate_ukeire(

            new_hand,

            visible_counts=visible_counts,
        )

        results.append({

            "discard":
                removed_tile,

            "shanten":
                shanten,

            "ukeire":
                ukeire_result[
                    "ukeire"
                ],

            "improving_tiles":
                ukeire_result[
                    "improving_tiles"
                ],
        })

    return results