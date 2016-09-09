#!/bin/bash
#SBATCH -p debug 
#SBATCH -N 1 
#SBATCH -t 00:10:00
#SBATCH -J subset-mpi
#SBATCH -e %j_10k.err
#SBATCH -o %j_10k.out
#SBATCH -L SCRATCH
cd $SLURM_SUBMIT_DIR
template=$SCRATCH/bosslover/scaling-test/ost72/10k_sep8.2.h5
cmd="srun -n 32 python-mpi ../scripts/subset_mpi.py "
filepath=" input-full-cori "
pmfquery=" pmf-list/large-scale/pmf10k-shuffle.csv "
fiber=$SLURM_JOB_ID"_nodes10k_fiber.txt "
catalog=$SLURM_JOB_ID"_nodes10k_catalog.txt "
opt1=" --mpi=yes"
opt2=" --template=yes"
opt3=" --fiber="
opt4=" --catalog="
run=$cmd$filepath$template$pmfquery$opt1$opt2$opt3$fiber$opt4$catalog
echo $run
$run
