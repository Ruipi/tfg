"""
Tile canonicalization and mapping utilities.

This module converts raw 136-tile Mahjong representations
into canonical semantic TileInstance objects used by the model.

This file is MODEL-FACING:
- canonical tile semantics
- copy indices
- red-five handling
- tensorization support

Human-readable decoding utilities should stay inside:
    tile_decoder.py
"""
import sys
from pathlib import Path

project_root = Path.cwd().parent

sys.path.append(str(project_root))

from src.features.token_definitions import TileInstance

from src.utils.tile_decoder import (
    tile34_to_string,
)


# ============================================================
# RED FIVE CONSTANTS
# ============================================================

# Standard Tenhou-style aka dora encoding
RED_FIVE_MAN = 16
RED_FIVE_PIN = 52
RED_FIVE_SOU = 88

RED_FIVE_IDS = {
    RED_FIVE_MAN,
    RED_FIVE_PIN,
    RED_FIVE_SOU,
}


# ============================================================
# CORE TILE CONVERSIONS
# ============================================================

def tile136_to_tile34(tile136: int) -> int:
    """
    Converts raw 136-tile encoding into semantic 34-tile ID.

    Examples:
        0-3   -> 0 (1m)
        4-7   -> 1 (2m)
        ...
        108-111 -> 27 (east)

    Returns:
        int: semantic tile ID in [0, 33]
    """

    return tile136 // 4


def tile136_to_copy_index(tile136: int) -> int:
    """
    Returns which physical copy of a tile this represents.

    Example:
        0 -> copy 0
        1 -> copy 1
        2 -> copy 2
        3 -> copy 3

    Returns:
        int: copy index in [0, 3]
    """

    return tile136 % 4


def is_red_five(tile136: int) -> bool:
    """
    Returns whether a tile is an aka dora (red five).

    Returns:
        bool
    """

    return tile136 in RED_FIVE_IDS


# ============================================================
# CANONICAL TILE INSTANCE
# ============================================================

def tile136_to_instance(tile136: int) -> TileInstance:
    """
    Converts raw 136-tile encoding into canonical TileInstance.

    Example:
        16 -> TileInstance(
            tile_type=4,
            copy_index=0,
            is_red=True
        )

    Returns:
        TileInstance
    """

    return TileInstance(
        tile_type=tile136_to_tile34(tile136),
        copy_index=tile136_to_copy_index(tile136),
        is_red=is_red_five(tile136),
    )


# ============================================================
# DEBUG / HUMAN-READABLE HELPERS
# ============================================================

def instance_to_string(tile: TileInstance) -> str:
    """
    Human-readable TileInstance representation.

    Example:
        red_5m_copy0
        east_copy2
    """

    tile_str = tile34_to_string(tile.tile_type)

    if tile.is_red:
        tile_str = f"red_{tile_str}"

    return f"{tile_str}_copy{tile.copy_index}"


def tiles_to_string(tiles: list[TileInstance]) -> list[str]:
    """
    Converts list of TileInstances into readable strings.
    """

    return [instance_to_string(tile) for tile in tiles]