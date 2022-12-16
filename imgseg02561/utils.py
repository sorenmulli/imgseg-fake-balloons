from typing import List

from pelutils import log
import torch
from torch import nn
import numpy as np
import torchvision
from torch.optim.lr_scheduler import PolynomialLR
from sklearn.metrics import jaccard_score, f1_score

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_model(classes: int):
    model = torchvision.models.segmentation.fcn_resnet50(
        weights=None,
        num_classes=classes,
    )
    return model.eval().to(DEVICE)


def get_optimizer(model):
    return torch.optim.SGD(
        model.parameters(), lr=0.02, momentum=0.09, weight_decay=1e-4
    )


def get_scheduler(optimizer, data_loader, args):
    return PolynomialLR(
        optimizer, total_iters=len(data_loader) * args.epochs, power=0.9
    )


def train_one_epoch(model, optimizer, data_loader, lr_scheduler) -> List[float]:
    log.debug("Starting epoch")
    losses = []
    model.train()
    for image, target in data_loader:
        log.debug("Starting batch")
        image, target = image.to(DEVICE), target.to(DEVICE)
        log.debug("Model forward pass")
        output = model(image)["out"]

        log.debug("Backward pass")
        loss = nn.functional.cross_entropy(output, target, ignore_index=255)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        lr_scheduler.step()

        losses.append(float(loss.item()))
        log.debug(f"loss={loss.item()}")
        log.debug(f"lr={optimizer.param_groups[0]['lr']}")
    log.debug("Finished epoch")
    log(f"Avg loss: {np.mean(losses):.3f}")


def evaluate(model, data_loader):
    targets, preds = [], []
    model.eval()
    with torch.inference_mode():
        for image, target in data_loader:
            log.debug("Eval batch")
            image, target = image.to(DEVICE), target.to(DEVICE)
            output = model(image)
            output = output["out"]

            targets.append(target.flatten().cpu().numpy())
            preds.append(output.argmax(1).flatten().cpu().numpy())
    report_results(targets, preds)


def report_results(targets: List[np.ndarray], preds: List[np.ndarray]):
    log(
        f"Accuracy : {100 * np.mean([(t == p).mean() for t, p in zip(targets, preds)]):.1f}%",
        f"Micro IoU: {100 * np.mean([jaccard_score(t, p, average='micro') for t, p in zip(targets, preds)]):.1f}%",
        f"Macro IoU: {100 * np.mean([jaccard_score(t, p, average='macro') for t, p in zip(targets, preds)]):.1f}%",
        f"Micro F1 : {100 * np.mean([f1_score(t, p, average='micro') for t, p in zip(targets, preds)]):.1f}%",
        f"Macro F1 : {100 * np.mean([f1_score(t, p, average='macro') for t, p in zip(targets, preds)]):.1f}%",
    )


def cat_list(images, fill_value=0):
    max_size = tuple(max(s) for s in zip(*[img.shape for img in images]))
    batch_shape = (len(images),) + max_size
    batched_imgs = images[0].new(*batch_shape).fill_(fill_value)
    for img, pad_img in zip(images, batched_imgs):
        pad_img[..., : img.shape[-2], : img.shape[-1]].copy_(img)
    return batched_imgs


def collate_fn(batch):
    images, targets = list(zip(*batch))
    batched_imgs = cat_list(images, fill_value=0)
    batched_targets = cat_list(targets, fill_value=255)
    return batched_imgs, batched_targets


def get_data_loader(dataset, train, batch_size: int):
    return torch.utils.data.DataLoader(
        dataset,
        batch_size=batch_size,
        sampler=torch.utils.data.RandomSampler(dataset)
        if train
        else torch.utils.data.SequentialSampler(dataset),
        collate_fn=collate_fn,
    )
