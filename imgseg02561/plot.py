import os
from collections import defaultdict
from pelutils import Argument, JobDescription

import matplotlib.pyplot as plt

def read_logfile(path: str, offset=0):
    with open(path, "r") as f:
        L = [(i, l.split("  ")[-1].strip()) for i, l in enumerate(f.readlines()[offset:]) if "%" in l or "Epoch" in l]
    out1 = defaultdict(dict)
    out2 = None
    epoch_num = 0
    for idx, l in L:
        if "Epoch" in l:
            new_epoch_num = int(l.split()[-1].split("/")[0])
            if new_epoch_num < epoch_num:
                res2, _ = read_logfile(path, idx)
                out2 = {0: out1.pop(epoch_num), **res2}
            epoch_num = new_epoch_num
        else:
            name, val = l.split(":")
            out1[epoch_num][name.strip()] = float(val.replace("%", "").strip())
    return out1, out2

def run(args: JobDescription):
    results = []
    names = []
    for logpath in args.logfile_paths.split():
        res1, res2 = read_logfile(logpath)
        if args.pretrain:
            results.append(res1)
        else:
            results.append(res2 or res1)
        names.append(os.path.split(os.path.dirname(logpath))[-1])
    metrics = list(results[0][0].keys())
    for n in metrics:
        plt.figure(figsize=(4, 4))
        for name, res in zip(names, results):
            plt.plot([r[n] for r in res.values()], label=name)
        plt.xlabel("Training epochs")
        plt.ylim(0, 100)
        plt.ylabel(f"{n} [%]")
        plt.title("Validation performance")
        plt.grid()
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(args.location, f"{n}.png"))
        plt.clf()


if __name__ == "__main__":
    from pelutils import Parser, Flag
    args = Parser(
        Argument("logfile-paths"),
        Flag("pretrain"),
    ).parse_args()
    run(args)
