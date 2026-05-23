import torch

def compute_topk_accuracy(
    logits_list,
    targets,
    k,
):

    correct = 0

    total = len(logits_list)

    for i in range(total):

        logits = logits_list[i]

        target = targets[i].item()

        topk = torch.topk(
            logits,
            k=min(k, logits.shape[0])
        ).indices

        if target in topk:

            correct += 1

    return correct / total