import sys
from pathlib import Path

project_root = Path.cwd().parent

sys.path.append(str(project_root))

from src.features.token_definitions import (
    GameStateToken,
    PlayerStateToken,
    HandToken,
    DiscardToken,
    MeldToken,
    ActionToken,
)

from src.utils.tile_mapping import (
    tile136_to_instance,
)

from src.utils.constants import ACTION_TYPES

class MahjongTokenizer:
    """
    Converts canonical Mahjong states into semantic token sequences.
    """

    def __init__(self):
        pass

    def tokenize(self, state: dict):

        tokens = []

        tokens.extend(
            self._create_game_state_tokens(state)
        )

        tokens.extend(
            self._create_player_state_tokens(state)
        )

        tokens.extend(
            self._create_hand_tokens(state)
        )
        """
        tokens.extend(
            self._create_meld_tokens(state)
        )

        tokens.extend(
            self._create_discard_tokens(state)
        )

        tokens.extend(
            self._create_action_tokens(state)
        )
        """
        return tokens

    def _create_game_state_tokens(self, state):

        dora_tiles = [
            tile136_to_instance(t)
            for t in state["dora_indicators"]
        ]

        token = GameStateToken(
            token_type="GAME_STATE",

            round_wind=state["round_wind"],

            honba_count=state["num_honba"],

            riichi_sticks=state["num_riichi"],

            remaining_tiles=state["remain_tiles"],

            dora_indicators=dora_tiles,
        )

        return [token]

    def _create_player_state_tokens(self, state):

        tokens = []

        for player_id, player_data in state["players"].items():

            placement = 0  # TODO later

            open_hand = len(player_data["melds"]) > 0

            token = PlayerStateToken(
                token_type="PLAYER_STATE",

                player=int(player_id),

                seat_wind=int(player_id),

                score=player_data["points"],

                riichi_status=player_data["riichi"],

                open_hand=open_hand,

                placement=placement,
            )

            tokens.append(token)

        return tokens

    def _create_hand_tokens(self, state):

        tokens = []

        sorted_tiles = sorted(state["hand_tiles"])

        for tile136 in sorted_tiles:

            tile = tile136_to_instance(tile136)

            token = HandToken(
                token_type="HAND",

                tile=tile,
            )

            tokens.append(token)

        return tokens