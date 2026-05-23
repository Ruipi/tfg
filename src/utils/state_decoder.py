from src.utils.tile_decoder import decode_tiles
from src.utils.action_decoder import decode_actions
from src.utils.meld_decoder import decode_melds

def print_state(sample):
    """
    Pretty-print a Mahjong decision state.
    """

    print("=" * 50)
    print("GAME STATE")
    print("=" * 50)

    print(f"Round wind: {sample['round_wind']}")
    print(f"Player wind: {sample['player_wind']}")
    print(f"Honba: {sample['num_honba']}")
    print(f"Riichi sticks: {sample['num_riichi']}")
    print(f"Remaining tiles: {sample['remain_tiles']}")

    print("\nDora indicators:")
    print(decode_tiles(sample["dora_indicators"]))

    print("\nPlayer hand:")
    print(decode_tiles(sample["hand_tiles"]))

    print("\nPlayers:")

    for pid in ["0", "1", "2", "3"]:

        player = sample[pid]

        print(f"\nPlayer {pid}")
        print(f"Points: {player['points']}")
        print(f"Riichi: {player['riichi']}")

        print("Discards:")
        decoded_discards = []

        for tile, tsumo in zip(
            player["discards"],
            player["tsumo_giri"]
        ):

            tile_str = tile136_to_string(tile)

            if tsumo:
                tile_str += " (tsumo)"

            decoded_discards.append(tile_str)

        print(decoded_discards)
        print("Melds:")
        print(decode_melds(player["melds"]))

    print("\nValid actions:")

    decoded_actions = decode_actions(
        sample["valid_actions"]
    )

    for i, action in enumerate(decoded_actions):
        print(f"{i}: {action}")

    chosen_idx = sample["action_idx"]

    print("\nExpert chose:")
    print(decoded_actions[chosen_idx])

    print("=" * 50)