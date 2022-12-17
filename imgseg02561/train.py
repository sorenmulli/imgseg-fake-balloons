import os

from pelutils import JobDescription, log, set_seeds
import torch

from imgseg02561.coco import get_coco
from imgseg02561.fake_balloons import FakeBalloons
from imgseg02561.transforms import get_transform

from imgseg02561.utils import (
    get_data_loader,
    get_optimizer,
    train_one_epoch,
    get_model,
    evaluate,
)

COCO_CLASSES = 21


def pretrain(model, args: JobDescription):
    optimizer = get_optimizer(model)
    full_dataset = FakeBalloons(args.fake_balloons_path, transforms=get_transform())
    split_idx = int(len(full_dataset) * 0.9)
    train_dataset = torch.utils.data.Subset(full_dataset, torch.arange(split_idx))
    val_dataset = torch.utils.data.Subset(full_dataset, torch.arange(split_idx, len(full_dataset)))

    data_loader_train = get_data_loader(train_dataset, True, args.batch_size)
    data_loader_val = get_data_loader(val_dataset, False, args.batch_size)

    evaluate(model, data_loader_val, args.classes)
    for epoch in range(args.pretrain_epochs):
        log(f"Epoch {epoch+1}/{args.pretrain_epochs}")
        train_one_epoch(model, optimizer, data_loader_train)
        evaluate(model, data_loader_val, args.classes)


def downstream(model, args: JobDescription):
    optimizer = get_optimizer(model)
    dataset_train = get_coco(
        args.coco_path, "train", get_transform(), data_limit=args.coco_limit or None
    )
    dataset_val = get_coco(args.coco_path, "val", get_transform(), data_limit=1000)

    data_loader_train = get_data_loader(dataset_train, True, args.batch_size)
    data_loader_val = get_data_loader(dataset_val, False, args.batch_size)

    evaluate(model, data_loader_val, COCO_CLASSES)
    for epoch in range(args.epochs):
        log(f"Epoch {epoch+1}/{args.epochs}")
        train_one_epoch(model, optimizer, data_loader_train)
        evaluate(model, data_loader_val, COCO_CLASSES)


def mutate_for_downstream(model):
    old_state = model.state_dict()
    old_state = {n: p for n, p in old_state.items() if "classifier.4" not in n}
    new_model = get_model(COCO_CLASSES)
    missing_keys, unexpected_keys = new_model.load_state_dict(old_state, strict=False)
    assert not unexpected_keys and all("classifier.4" in k for k in missing_keys)
    return new_model


def run(args: JobDescription):
    set_seeds()
    model = get_model(args.classes)
    if not args.skip_pretrain:
        pretrain(model, args)
    model = mutate_for_downstream(model)
    downstream(model, args)



if __name__ == "__main__":
    from pelutils import Parser, Option, Argument, Flag

    parser = Parser(
        Argument("fake-balloons-path"),
        Argument("coco-path"),
        Option("classes", type=int, default=4),
        Option("coco-limit", type=int, default=0),
        Option("pretrain-epochs", type=int, default=20),
        Option("epochs", type=int, default=10),
        Option("batch-size", type=int, default=32),
        Flag("skip-pretrain"),
        multiple_jobs=True,
    )

    jobs = parser.parse_args()
    parser.document()
    for job in jobs:
        log.configure(
            os.path.join(job.location, f"training.log"),
        )
        log.log_repo()
        log(f"Starting {job.name}")
        with log.log_errors:
            run(job)
