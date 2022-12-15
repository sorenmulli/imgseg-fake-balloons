from typing import List

from pelutils import log
import torch
from torch import nn
import torchvision
from torch.optim.lr_scheduler import PolynomialLR
from torchvision.datasets.coco import CocoDetection

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_model(classes: int):
    model = torchvision.models.segmentation.fcn_resnet50(
        weights=None, num_classes=classes,
    )
    return model.eval().to(DEVICE)

def get_optimizer(model):
    return torch.optim.SGD(model.parameters(), lr=0.02, momentum=0.09, weight_decay=1e-4)

def get_scheduler(optimizer, data_loader, args):
    return PolynomialLR(
        optimizer, total_iters=len(data_loader) * args.epochs, power=0.9
    )

def train_one_epoch(
    model,  optimizer, data_loader, lr_scheduler
) -> List[float]:
    losses = []
    model.train()
    for image, target in data_loader:
        image, target = image.to(DEVICE), target.to(DEVICE)
        output = model(image)

        #TODO: Ignore index?
        loss = nn.functional.cross_entropy(output, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        lr_scheduler.step()

        losses.append(float(loss.item()))
        log.debug(f"loss={loss.item()}")
        log.debug(f"lr={optimizer.param_groups[0]['lr']}")
    return losses


def evaluate(model, data_loader):
    model.eval()
    with torch.inference_mode():
        for image, target in data_loader:
            image, target = image.to(DEVICE), target.to(DEVICE)
            output = model(image)
            output = output["out"]

            target = target.flatten()
            pred = output.argmax(1).flatten()

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
