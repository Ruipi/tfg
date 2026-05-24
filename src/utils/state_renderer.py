from src.utils.tile_decoder import (
    tile136_to_string
)

from src.utils.action_decoder import (
    decode_action
)

def render_tiles(tiles):

    decoded = [
        tile136_to_string(t)
        for t in tiles
    ]

    return " ".join(decoded)

def render_melds(melds):

    if len(melds) == 0:

        return "None"

    rendered = []

    for meld in melds:

        rendered.append(
            decode_action(meld)
        )

    return "\n".join(rendered)

def render_discards(
    discards,
    tsumogiri=None,
):

    rendered = []

    for i, tile in enumerate(discards):

        tile_str = tile136_to_string(tile)

        if tsumogiri is not None:

            if tsumogiri[i]:

                tile_str += "*"

        rendered.append(tile_str)

    return " ".join(rendered)

def render_state(state):

    print()

    print("=" * 50)

    print("ROUND")

    print("=" * 50)

    print()

    print(
        f"Round Wind: {state['round_wind']}"
    )

    print(
        f"Honba: {state['num_honba']}"
    )

    print(
        f"Riichi Sticks: "
        f"{state['num_riichi']}"
    )

    print(
        f"Remaining Tiles: "
        f"{state['remain_tiles']}"
    )

    print()

    print(
        "Dora Indicators:",
        render_tiles(
            state["dora_indicators"]
        )
    )

    for player_id, player in (
        state["players"].items()
    ):

        print()

        print("=" * 50)

        print(
            f"PLAYER {player_id}"
        )

        print("=" * 50)

        print()

        print(
            f"Points: {player['points']}"
        )

        print(
            f"Riichi: {player['riichi']}"
        )

        if int(player_id) == (
            state["player_wind"]
        ):

            print()

            print("HAND:")

            print(
                render_tiles(
                    state["hand_tiles"]
                )
            )

            print()

        print("MELDS:")

        print(
            render_melds(
                player["melds"]
            )
        )

        print()

        print("DISCARDS:")

        print(
            render_discards(
                player["discards"],
                player["tsumo_giri"],
            )
        )

        