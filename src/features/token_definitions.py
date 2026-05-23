from dataclasses import dataclass, field
from typing import List, Optional


# ============================================================
# FOUNDATIONAL ENTITIES
# ============================================================

@dataclass
class TileInstance:
    """
    Represents one physical Mahjong tile instance.

    tile_type:
        Canonical semantic tile ID.
        Example:
            0-8   -> 1m-9m
            9-17  -> 1p-9p
            18-26 -> 1s-9s
            27-33 -> honors

    copy_index:
        Distinguishes duplicate copies of the same tile.

    is_red:
        Whether tile is aka-dora (red five).
    """

    tile_type: int
    copy_index: int
    is_red: bool = False


# ============================================================
# BASE TOKEN CLASS
# ============================================================

@dataclass
class BaseToken:
    """
    Base semantic token class.
    """

    token_type: str


# ============================================================
# HAND TOKENS
# ============================================================

@dataclass
class HandToken(BaseToken):
    """
    Represents one concealed hand tile.
    """

    tile: TileInstance


# ============================================================
# DISCARD TOKENS
# ============================================================

@dataclass
class DiscardToken(BaseToken):
    """
    Represents one public discard event.
    """

    tile: TileInstance

    player: int

    is_tsumogiri: bool

    is_riichi_declaration: bool

    global_order: int

    local_order: int


# ============================================================
# MELD TOKENS
# ============================================================

@dataclass
class MeldToken(BaseToken):
    """
    Represents one meld/call event.
    """

    player: int

    meld_type: str

    tiles: List[TileInstance]

    source_players: List[int]

    global_order: int


# ============================================================
# ACTION TOKENS
# ============================================================

@dataclass
class ActionToken(BaseToken):
    """
    Represents one candidate legal action.
    """

    action_index: int

    action_type: str

    tiles: List[TileInstance]

    source_players: List[int]

    global_order: Optional[int] = None


# ============================================================
# PLAYER STATE TOKENS
# ============================================================

@dataclass
class PlayerStateToken(BaseToken):
    """
    Represents persistent player context/state.
    """

    player: int

    seat_wind: int

    score: int

    riichi_status: bool

    open_hand: bool

    placement: int


# ============================================================
# GAME STATE TOKEN
# ============================================================

@dataclass
class GameStateToken(BaseToken):
    """
    Represents persistent global game context.
    """

    round_wind: int

    honba_count: int

    riichi_sticks: int

    remaining_tiles: int

    dora_indicators: List[TileInstance]