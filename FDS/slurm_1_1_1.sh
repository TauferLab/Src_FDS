#!/bin/bash

#SBATCH --job-name=FDS
#SBATCH --output=%x-%j.out                          # %x = Job Name & %j = Job Id
#SBATCH --error=%x-%j.err                          
#SBATCH --nodes=1                                   # Total number of nodes
#SBATCH --ntasks=8                                  # Total number of MPI tasks
#SBATCH --time=2:00:00                              # Run time (d-hh:mm:ss)
#SBATCH --partition=development                            # Replace queue_name with appropriate partition name (ex. skx-normal)
#SBATCH --mail-user=leobardovalera@gmail.com        # Replace email with your preferred email
#SBATCH --mail-type=all                             # Send email at start & end of job
#SBATCH -A ASC21014                                 # Allocation name (req'd if you have more than 1

# ibrun is TACC's equivalent of mpiexec command 
ibrun fds Whole_Nist.fds
### Run this script in the CLI by running the following command:
### sbatch slurm_script.sh
