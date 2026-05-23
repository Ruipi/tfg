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
        
        tokens.extend(
            self._create_meld_tokens(state)
        )
        
        tokens.extend(
            self._create_discard_tokens(state)
        )
        
        tokens.extend(
            self._create_action_tokens(state)
        )
        
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

    def _create_discard_tokens(self, state):

        tokens = []

        players = state["players"]

        # ========================================================
        # Determine max discard length
        # ========================================================

        max_discards = max(
            len(player["discards"])
            for player in players.values()
        )

        global_order = 0

        # ========================================================
        # Reconstruct approximate global discard order
        # ========================================================

        for local_order in range(max_discards):

            for player_id in range(4):

                player = players[str(player_id)]

                # Skip if player has no discard at this index
                if local_order >= len(player["discards"]):
                    continue

                tile136 = player["discards"][local_order]

                tile = tile136_to_instance(tile136)

                tsumogiri = bool(
                    player["tsumo_giri"][local_order]
                )

                # =================================================
                # Riichi declaration detection
                # =================================================

                is_riichi_declaration = False

                # TODO:
                # improve later with precise replay timing

                token = DiscardToken(
                    token_type="DISCARD",

                    tile=tile,

                    player=player_id,

                    is_tsumogiri=tsumogiri,

                    is_riichi_declaration=is_riichi_declaration,

                    global_order=global_order,

                    local_order=local_order,
                )

                tokens.append(token)

                global_order += 1

        return tokens

    def _create_meld_tokens(self, state):

        tokens = []

        players = state["players"]

        global_order = 0

        # ========================================================
        # Approximate chronological reconstruction
        # ========================================================

        for player_id in range(4):

            player = players[str(player_id)]

            melds = player["melds"]

            for meld in melds:

                meld_type = ACTION_TYPES[meld["type"]]

                # =================================================
                # Remove placeholder entries
                # =================================================

                valid_tiles = [
                    t for t in meld["tiles"]
                    if t != -1
                ]

                valid_sources = [
                    w for w in meld["who"]
                    if w != -1
                ]

                # =================================================
                # Convert tiles into TileInstances
                # =================================================

                tile_instances = [
                    tile136_to_instance(t)
                    for t in valid_tiles
                ]

                token = MeldToken(
                    token_type="MELD",

                    player=player_id,

                    meld_type=meld_type,

                    tiles=tile_instances,

                    source_players=valid_sources,

                    global_order=global_order,
                )

                tokens.append(token)

                global_order += 1

        return tokens
    
    def _create_action_tokens(self, state):

        tokens = []

        valid_actions = state["valid_actions"]

        for action_index, action in enumerate(valid_actions):

            action_type = ACTION_TYPES[action["type"]]

            # ====================================================
            # Remove placeholder entries
            # ====================================================

            valid_tiles = [
                t for t in action["tiles"]
                if t != -1
            ]

            valid_sources = [
                w for w in action["who"]
                if w != -1
            ]

            # ====================================================
            # Convert tiles into TileInstances
            # ====================================================

            tile_instances = [
                tile136_to_instance(t)
                for t in valid_tiles
            ]

            token = ActionToken(
                token_type="ACTION",

                action_index=action_index,

                action_type=action_type,

                tiles=tile_instances,

                source_players=valid_sources,

                global_order=None,
            )

            tokens.append(token)

        return tokens