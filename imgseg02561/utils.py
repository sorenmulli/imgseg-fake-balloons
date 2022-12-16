from typing import List
from dataclasses import dataclass

from pelutils import log
import torch
from torch import nn
import numpy as np
import torchvision
from torch.optim.lr_scheduler import PolynomialLR
from torchmetrics import F1Score, JaccardIndex, Accuracy

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
    losses = []
    model.train()
    for i, (image, target) in enumerate(data_loader):
        image, target = image.to(DEVICE), target.to(DEVICE)
        output = model(image)["out"]

        loss = nn.functional.cross_entropy(output, target, ignore_index=255)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        lr_scheduler.step()

        losses.append(float(loss.item()))
        log.debug(f"Finished batch {i+1}/{len(data_loader)}, loss={loss.item():.3f}, lr={optimizer.param_groups[0]['lr']:.3f}")
    log(f"Avg loss: {np.mean(losses):.3f}")

@dataclass
class EvalResults:
    micro_accs: List[float]
    macro_accs: List[float]
    micro_ious: List[float]
    macro_ious: List[float]
    micro_f1s: List[float]
    macro_f1s: List[float]


    def __str__(self):
        return "\n".join([
            f"Micro Accuracy : {100 * np.mean(self.micro_accs):.1f}%",
            f"Macro Accuracy : {100 * np.mean(self.macro_accs):.1f}%",
            f"Micro IoU: {100 * np.mean(self.micro_ious):.1f}%",
            f"Macro IoU: {100 * np.mean(self.macro_ious):.1f}%",
            f"Micro F1 : {100 * np.mean(self.micro_f1s):.1f}%",
            f"Macro F1 : {100 * np.mean(self.macro_f1s):.1f}%",
        ])



def evaluate(model, data_loader, classes: int):
    model.eval()
    res = EvalResults([], [], [], [], [], [])
    args = dict(task="multiclass", num_classes=classes, ignore_index=255)
    mi_acc = Accuracy(**args, average="micro").to(DEVICE)
    ma_acc = Accuracy(**args, average="macro").to(DEVICE)
    mi_iou = JaccardIndex(**args, average="micro").to(DEVICE)
    ma_iou = JaccardIndex(**args, average="macro").to(DEVICE)
    mi_f1 = F1Score(**args, average="micro").to(DEVICE)
    ma_f1 = F1Score(**args, average="macro").to(DEVICE)
    with torch.inference_mode():
        for i, (image, target) in enumerate(data_loader):
            log.debug(f"Eval batch {i+1}/{len(data_loader)}")
            image, target = image.to(DEVICE), target.to(DEVICE)
            output = model(image)["out"]

            true = target.flatten()
            pred = output.argmax(1).flatten()
            res.micro_accs.append(float(mi_acc(pred, true).cpu().item()))
            res.macro_accs.append(float(ma_acc(pred, true).cpu().item()))
            res.micro_ious.append(float(mi_iou(pred, true).cpu().item()))
            res.macro_ious.append(float(ma_iou(pred, true).cpu().item()))
            res.micro_f1s.append(float(mi_f1(pred, true).cpu().item()))
            res.macro_f1s.append(float(ma_f1(pred, true).cpu().item()))
    log(res)


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
