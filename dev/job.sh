#!/bin/sh
#BSUB -q gpua100
#BSUB -R "select[gpu80gb]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -J "02561"
#BSUB -R "rusage[mem=100GB]"
#BSUB -n 8
#BSUB -W 10:00
#BSUB -N
#BSUB -u s183911@student.dtu.dk
#BSUB -eo /dev/null
#BSUB -oo /dev/null

source $HOME/.venv/bin/activate

echo "!!Training!!"
make train
echo "!!Done!!"
