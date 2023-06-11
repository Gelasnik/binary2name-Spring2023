#!/bin/bash
#
#SBATCH --job-name=binary2name
#SBATCH --output=res.txt
#SBATCH --gres=gpu:1
#SBATCH -c 10
#SBATCH --nodelist=lambda3
srun -c 10 --gres=gpu:1 /bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate tf1
./run_pipeline_for_nero.sh
