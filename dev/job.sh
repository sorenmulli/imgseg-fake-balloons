#!/bin/sh
#BSUB -q gpua100
#BSUB -R "select[gpu80gb]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -J "training"
#BSUB -R "rusage[mem=200GB]"
#BSUB -n 1
#BSUB -W 10:00
#BSUB -N
#BSUB -u s183911@student.dtu.dk
#BSUB -eo /dev/null
#BSUB -oo /dev/null

source $HOME/.venv/bin/activate

echo "!!Training!!"
make train
echo "!!Done!!"
