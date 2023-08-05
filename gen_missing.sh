#!/usr/local_rwth/bin/zsh


### TIME 
#SBATCH --time=2:00:00

### ACCOUNT
###SBATCH --account=rwth0754

### JOBNAME
#SBATCH --job-name=find_min_max

### OUTPUT
#SBATCH --output=./output.txt

### your code goes here

### Insert this AFTER the #SLURM argument section of your job script
export CONDA_ROOT=$HOME/miniconda3
. $CONDA_ROOT/etc/profile.d/conda.sh
export PATH="$CONDA_ROOT/bin:$PATH"

### Now you can activate your configured conda environments
conda activate EMRI_env

date

python ./spectrograms/gen_others.py

date
