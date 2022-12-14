import os

from pelutils import JobDescription, log, set_seeds

from imgseg02561.utils import train_one_epoch, get_model, evaluate

def downstream(model, args: JobDescription):
    pass


def pretrain(model, args: JobDescription):
    pass


def run(args: JobDescription):
    set_seeds()

    model = get_model(args.classes)
    pretrain(model, args)
    # Convert model!
    downstream(model, args)


if __name__ == "__main__":
    from pelutils import Parser, Option

    parser = Parser(
        Option("classes", type=int, default=3),
        multiple_jobs=True,
    )

    jobs = parser.parse_args()
    parser.document()
    for job in jobs:
        log.configure(os.path.join(job.location, f"training.log"))
        log.log_repo()
        log(f"Starting {job.name}")
        with log.log_errors:
            run(job)
