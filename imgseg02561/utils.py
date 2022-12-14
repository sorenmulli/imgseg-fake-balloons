from typing import List

from pelutils import log
import torch
import torchvision

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_model(classes: int):
    model = torchvision.models.segmentation.fcn_resnet50(
        weights=None, num_classes=classes+1,
    )
    return model.eval().to(DEVICE)


def train_one_epoch(
    model, criterion, optimizer, data_loader, lr_scheduler, device
) -> List[float]:
    losses = []
    model.train()
    for image, target in data_loader:
        image, target = image.to(device), target.to(device)
        output = model(image)

        loss = criterion(output, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        lr_scheduler.step()

        losses.append(float(loss.item))
        log.debug(f"loss={loss.item()}")
        log.debug(f"lr={optimizer.param_groups[0]['lr']}")
    return losses


def evaluate(model, data_loader, device):
    model.eval()
    with torch.inference_mode():
        for image, target in data_loader:
            image, target = image.to(device), target.to(device)
            output = model(image)
            output = output["out"]

            target = target.flatten()
            pred = output.argmax(1).flatten()


def get_dataloader(dataset, train, batch_size: int):
    return torch.utils.data.DataLoader(
        dataset,
        batch_size=batch_size,
        sampler=torch.utils.data.RandomSampler(dataset)
        if train
        else torch.utils.data.SequentialSampler(dataset),
        collate_fn=utils.collate_fn,
    )
