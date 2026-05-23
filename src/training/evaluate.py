import torch

from src.training.metrics import (
    compute_topk_accuracy
)

def evaluate_model(
    model,
    dataloader,
    criterion,
    device,
):

    model.eval()

    total_loss = 0

    total_correct = 0

    total_samples = 0

    total_top3 = 0

    total_top5 = 0

    with torch.no_grad():

        for batch in dataloader:

            # ========================================
            # Move batch to device
            # ========================================

            moved = {}

            for key, value in batch.items():

                if isinstance(value, list):

                    moved[key] = [
                        v.to(device)
                        for v in value
                    ]

                else:

                    moved[key] = value.to(device)

            batch = moved

            targets = batch["target"]

            logits_list = model(batch)

            batch_loss = 0

            correct = 0

            # ========================================
            # Top-k metrics
            # ========================================

            top3_acc = compute_topk_accuracy(
                logits_list,
                targets,
                k=3,
            )

            top5_acc = compute_topk_accuracy(
                logits_list,
                targets,
                k=5,
            )

            total_top3 += (
                top3_acc * len(logits_list)
            )

            total_top5 += (
                top5_acc * len(logits_list)
            )

            # ========================================
            # Per-sample losses
            # ========================================

            for i in range(len(logits_list)):

                logits = logits_list[i].unsqueeze(0)

                target = targets[i].unsqueeze(0)

                loss = criterion(
                    logits,
                    target,
                )

                batch_loss += loss.item()

                prediction = torch.argmax(
                    logits
                ).item()

                if prediction == target.item():

                    correct += 1

            batch_loss /= len(logits_list)

            total_loss += batch_loss

            total_correct += correct

            total_samples += len(logits_list)

    avg_loss = (
        total_loss / len(dataloader)
    )

    accuracy = (
        total_correct / total_samples
    )

    top3_accuracy = (
        total_top3 / total_samples
    )

    top5_accuracy = (
        total_top5 / total_samples
    )

    return (
        avg_loss,
        accuracy,
        top3_accuracy,
        top5_accuracy,
    )