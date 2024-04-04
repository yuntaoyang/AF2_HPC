#!/bin/bash
#SBATCH -J job_name
#SBATCH -o job_name.o%j
#SBATCH -N num_nodes
#SBATCH -n num_tasks
#SBATCH -p normal # queue (partition)
#SBATCH -t 02:00:00 # run time (hh:mm:ss)
#SBATCH -A allocation_name # allocation name
#SBATCH --mail-type=all
#SBATCH --mail-user=email_address

module load launcher
export LAUNCHER_WORKDIR=./workdir/
export LAUNCHER_JOB_FILE=jobfile
${LAUNCHER_DIR}/paramrun