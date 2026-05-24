from mahjong.shanten import Shanten

from src.utils.tile_decoder import (
    tiles136_to_34_array
)

shanten_calculator = Shanten()

def calculate_shanten(tiles136):

    tiles34 = tiles136_to_34_array(
        tiles136
    )

    return shanten_calculator.calculate_shanten(
        tiles34
    )

def evaluate_discards(tiles136):

    results = []

    for i, tile in enumerate(tiles136):

        new_hand = tiles136.copy()

        removed_tile = new_hand.pop(i)

        shanten = calculate_shanten(new_hand)

        results.append({
            "discard": removed_tile,
            "shanten": shanten,
        })

    return results