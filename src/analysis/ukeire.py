from src.analysis.shanten import (
    calculate_shanten
)

from src.utils.tile_decoder import (
    tile136_to_tile34
)

def calculate_ukeire(tiles136):

    current_shanten = calculate_shanten(
        tiles136
    )

    improving_tiles = []

    for tile34 in range(34):

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

    return {
        "ukeire": len(improving_tiles),

        "improving_tiles":
            improving_tiles,
    }

def evaluate_discards_ukeire(
    tiles136
):

    results = []

    for i, tile in enumerate(tiles136):

        new_hand = tiles136.copy()

        removed_tile = new_hand.pop(i)

        shanten = calculate_shanten(new_hand)

        ukeire_result = calculate_ukeire(new_hand)

        results.append({
            "discard": removed_tile,
            "shanten": shanten,
            "ukeire": ukeire_result["ukeire"],
            "improving_tiles": ukeire_result["improving_tiles"],
        })

    return results