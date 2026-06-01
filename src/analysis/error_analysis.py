import pandas as pd

def categorize_mistake(row):

    # ==========================================
    # EXACT MATCH
    # ==========================================

    if row["same_action"]:

        return "exact_match"

    # ==========================================
    # MODEL IMPROVES SHANTEN
    # ==========================================

    if (
        row["model_shanten"]
        <
        row["expert_shanten"]
    ):

        return "better_shanten"

    # ==========================================
    # MODEL LOSES SHANTEN
    # ==========================================

    if (
        row["model_shanten"]
        >
        row["expert_shanten"]
    ):

        return "shanten_loss"

    # ==========================================
    # FROM HERE:
    # SAME SHANTEN
    # ==========================================

    ukeire_diff = (

        row["expert_ukeire"]
        -
        row["model_ukeire"]
    )

    # ==========================================
    # IDENTICAL EFFICIENCY
    # ==========================================

    if ukeire_diff == 0:

        return "equivalent"

    # ==========================================
    # MODEL BETTER UKEIRE
    # ==========================================

    if ukeire_diff < 0:

        # model has more ukeire

        if abs(ukeire_diff) <= 2:

            return "near_equivalent"

        return "better_ukeire"

    # ==========================================
    # MODEL WORSE UKEIRE
    # ==========================================

    if ukeire_diff > 0:

        if ukeire_diff <= 2:

            return "near_equivalent"

        return "ukeire_loss"

    # ==========================================
    # SHOULD NEVER HAPPEN
    # ==========================================

    return "unknown"