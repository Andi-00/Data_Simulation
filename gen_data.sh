#!/usr/local_rwth/bin/zsh

### ARRAY
#SBATCH --array=0-9

### TIME 
#SBATCH --time=10:00:00

### ACCOUNT
###SBATCH --account=rwth0754

### JOBNAME
#SBATCH --job-name=SimulateData

### OUTPUT
#SBATCH --output=./outputs/Job_SimulateData_%a.txt

### your code goes here

# Insert this AFTER the #SLURM argument section of your job script
export CONDA_ROOT=$HOME/miniconda3
. $CONDA_ROOT/etc/profile.d/conda.sh
export PATH="$CONDA_ROOT/bin:$PATH"

# Now you can activate your configured conda environments
conda activate EMRI_env

date

python ./spectrograms/gen_data.py -n=${SLURM_ARRAY_TASK_ID} -m=1000

date

