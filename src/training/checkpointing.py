import torch

def save_checkpoint(
    model,
    optimizer,
    epoch,
    path,
):

    checkpoint = {
        "epoch": epoch,

        "model_state_dict":
            model.state_dict(),

        "optimizer_state_dict":
            optimizer.state_dict(),
    }

    torch.save(
        checkpoint,
        path,
    )

    print(
        f"Checkpoint saved to {path}"
    )