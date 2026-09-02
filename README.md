# Development of an AI to Play Riichi Mahjong

**Prediction and Strategic Evaluation of Riichi Mahjong Discards Using Transformers**

This final-year project studies discard prediction in Riichi Mahjong using a Transformer encoder trained through imitation learning on game states derived from Tenhou logs. Besides conventional top-k accuracy, it introduces a complementary evaluation based on **Shanten** and **Ukeire** to distinguish exact matches from alternative discards with similar offensive hand efficiency.

## Final results

Both checkpoints were evaluated on the same reserved set of 52,563 states:

| Checkpoint | Loss | Top-1 | Top-3 | Top-5 | Strategic accuracy |
|---|---:|---:|---:|---:|---:|
| 100k | 1.3533 | 55.81% | 83.37% | 91.25% | 88.97% |
| 500k | 0.9440 | 65.64% | 92.47% | 97.71% | 94.01% |

Strategic accuracy measures only the aspects represented by Shanten and Ukeire. It is not a complete measure of playing strength, defensive safety, hand value, or expected score.

## Repository structure

```text
.
├── src/          # Data processing, tokenisation, model, training and evaluation
├── notebooks/    # Exploratory work, training and final evaluation
├── reports/      # Generated CSV summaries and figures
├── memoria/      # Dissertation and annexes (Spanish)
├── environment.yml
└── README.md
```

The notebook sequence is described in [`notebooks/00_index.md`](notebooks/00_index.md). The definitive comparison is implemented in [`notebooks/11_independent_holdout_evaluation.ipynb`](notebooks/11_independent_holdout_evaluation.ipynb).

## Environment setup

The project uses Python 3.11 and PyTorch. Recreate the Conda environment from the repository root:

```bash
conda env create -f environment.yml
conda activate riichi-ai
jupyter lab
```

CUDA is used automatically when available; otherwise, the evaluation falls back to the CPU.

## Required data and checkpoints

Data and model weights are excluded from Git because of their size. To reproduce the final evaluation, place the following files at these exact paths:

```text
data/discard/strategic.db
checkpoints/strategic_100k/strategic_baseline.pt
checkpoints/strategic_500k/epoch_15.pt
```

`strategic.db` must contain 552,563 rows in its `Discard` table. The final 52,563 rows, beginning at offset 500,000, are reserved for evaluation.

The source dataset was created from Tenhou logs and distributed through Kaggle under the Apache 2.0 license. Its format and usage are described in the dataset author's [How to Use notebook](https://www.kaggle.com/code/hphphp123321/how-to-use).

## Reproducing the final evaluation

1. Activate the `riichi-ai` environment.
2. Start Jupyter Lab from the project root.
3. Open `notebooks/11_independent_holdout_evaluation.ipynb`.
4. Run all cells in order.

The notebook validates the database split, evaluates both checkpoints, calculates the strategic categories, and writes its outputs to:

```text
reports/holdout/
reports/figures/holdout/
```

On the development machine (Intel Core Ultra 7 255HX and NVIDIA GeForce RTX 5060 Laptop), inference for both checkpoints took 167 seconds. Shanten, Ukeire, and strategic categorisation took a further 481 seconds. These measurements are indicative and depend on the hardware and system load.

## Model overview

The implemented model uses:

- embedding dimension: 128;
- attention heads: 8;
- Transformer encoder layers: 4;
- feed-forward dimension: 512;
- dropout: 0.1;
- trainable parameters: 867,073.

Each token is tensorised through six identifiers: token type, tile type, tile copy, player, action type, and absolute sequence position. Some metadata retained by the intermediate representation—such as scores, Riichi status, Honba, Tsumogiri flags, and full meld details—is not passed to the evaluated checkpoints.

## Reproducibility limitations

- The processed dataset has no game identifier, so the split is independent at row level but cannot guarantee separation by complete games.
- The 100k checkpoint can be evaluated from its saved weights, but its original training run cannot be reconstructed completely because full optimiser, epoch, and execution metadata were not retained.
- Strategic evaluation focuses on offensive hand efficiency and does not model defensive risk or the complete match context.

For additional detail, see the dissertation and **Annex V: Reproducibility Manual** in [`memoria/`](memoria/).
