import os

from pelutils import JobDescription, LogLevels, log, set_seeds
from imgseg02561.coco import get_coco
from imgseg02561.transforms import get_transform

from imgseg02561.utils import (
    get_data_loader,
    get_optimizer,
    get_scheduler,
    train_one_epoch,
    get_model,
    evaluate,
)

COCO_CLASSES = 21


def downstream(model, args: JobDescription):
    optimizer = get_optimizer(model)
    dataset_train = get_coco(args.data_path, "train", get_transform(), data_limit=10)
    data_loader_train = get_data_loader(dataset_train, True, args.batch_size)
    scheduler = get_scheduler(optimizer, data_loader_train, args)
    for epoch in range(args.epochs):
        train_one_epoch(model, optimizer, data_loader_train, scheduler)


def mutate_for_downstream(model):
    old_state = model.state_dict()
    old_state = {n: p for n, p in old_state.items() if "classifier" not in n}
    new_model = get_model(COCO_CLASSES)
    missing_keys, unexpected_keys = new_model.load_state_dict(old_state, strict=False)
    assert not unexpected_keys and all("classifier" in k for k in missing_keys)
    return new_model


def run(args: JobDescription):
    set_seeds()

    model = get_model(args.classes)
    # pretrain(model, args)
    model = mutate_for_downstream(model)
    downstream(model, args)


if __name__ == "__main__":
    from pelutils import Parser, Option, Argument

    parser = Parser(
        Argument("data-path"),
        Option("classes", type=int, default=4),
        Option("epochs", type=int, default=10),
        Option("batch-size", type=int, default=32),
        multiple_jobs=True,
    )

    jobs = parser.parse_args()
    parser.document()
    for job in jobs:
        log.configure(
            os.path.join(job.location, f"training.log"), print_level=LogLevels.DEBUG
        )
        log.log_repo()
        log(f"Starting {job.name}")
        with log.log_errors:
            run(job)
