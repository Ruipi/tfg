import pandas as pd

def categorize_mistake(row):
    if row["same_action"]:

        return "exact_match"

    if (
        row["expert_shanten"]
        ==
        row["model_shanten"]
    ) and (
        row["expert_ukeire"]
        ==
        row["model_ukeire"]
    ):

        return "equivalent"

    if (
        row["expert_shanten"]
        ==
        row["model_shanten"]
    ) and (
        abs(
            row["expert_ukeire"]
            -
            row["model_ukeire"]
        ) <= 2
    ):

        return "near_equivalent"

    if (
        row["expert_shanten"]
        ==
        row["model_shanten"]
    ) and (
        row["model_ukeire"]
        <
        row["expert_ukeire"]
    ):

        return "ukeire_loss"

    if (
        row["model_shanten"]
        ==
        row["expert_shanten"] + 1
    ):

        return "shanten_loss"

    return "catastrophic"