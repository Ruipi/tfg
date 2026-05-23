import torch

from src.training.evaluate import (
    evaluate_model
)

from src.training.checkpointing import (
    save_checkpoint
)

def train_model(
    model,
    train_loader,
    val_loader,
    optimizer,
    criterion,
    device,
    epochs=10,
    checkpoint_dir=None,
):

    train_losses = []

    train_accuracies = []

    val_losses = []

    val_accuracies = []

    val_top3s = []

    val_top5s = []

    for epoch in range(epochs):

        model.train()

        epoch_loss = 0

        epoch_correct = 0

        epoch_total = 0

        for batch in train_loader:

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

            optimizer.zero_grad()

            logits_list = model(batch)

            total_loss = 0

            correct = 0

            for i in range(len(logits_list)):

                logits = logits_list[i].unsqueeze(0)

                target = targets[i].unsqueeze(0)

                loss = criterion(
                    logits,
                    target,
                )

                total_loss += loss

                prediction = torch.argmax(
                    logits
                ).item()

                if prediction == target.item():

                    correct += 1

            total_loss = (
                total_loss / len(logits_list)
            )

            total_loss.backward()

            optimizer.step()

            epoch_loss += total_loss.item()

            epoch_correct += correct

            epoch_total += len(logits_list)

        epoch_loss /= len(train_loader)

        epoch_accuracy = (
            epoch_correct / epoch_total
        )

        train_losses.append(epoch_loss)

        train_accuracies.append(
            epoch_accuracy
        )

        (
            val_loss,
            val_accuracy,
            val_top3,
            val_top5,
        ) = evaluate_model(
            model,
            val_loader,
            criterion,
            device,
        )

        val_losses.append(val_loss)

        val_accuracies.append(
            val_accuracy
        )

        val_top3s.append(val_top3)

        val_top5s.append(val_top5)

        print(f"\nEpoch {epoch+1}")

        print(
            f"Train Loss: {epoch_loss:.4f}"
        )

        print(
            f"Train Accuracy: {epoch_accuracy:.4f}"
        )

        print(
            f"Val Loss: {val_loss:.4f}"
        )

        print(
            f"Val Accuracy: {val_accuracy:.4f}"
        )

        print(
            f"Val Top-3: {val_top3:.4f}"
        )

        print(
            f"Val Top-5: {val_top5:.4f}"
        )

        if checkpoint_dir is not None:

            save_checkpoint(
                model,
                optimizer,
                epoch,

                f"{checkpoint_dir}/epoch_{epoch+1}.pt"
            )

    return {
        "train_losses": train_losses,
        "train_accuracies": train_accuracies,
        "val_losses": val_losses,
        "val_accuracies": val_accuracies,
        "val_top3s": val_top3s,
        "val_top5s": val_top5s,
    }