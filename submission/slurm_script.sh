#!/bin/bash

#SBATCH --job-name=FDS
#SBATCH --output=%x-%j.out                                  # %x = Job Name & %j = Job Id
#SBATCH --error=%x-%j.err
#SBATCH --nodes=1                                           # Total number of nodes
#SBATCH --ntasks=1                                          # Total number of MPI tasks
#SBATCH --time=1:00:00                                      # Run time (d-hh:mm:ss)
#SBATCH --partition=queue_name                              # Replace queue_name with appropriate partition name (ex. skx-normal)
#SBATCH --mail-user=username@tacc.utexas.edu                # Replace email with your preferred email
#SBATCH --mail-type=all                                     # Send email at start & end of job

export OMP_NUM_THREADS=4                                    # Controls OpenMP threads/processor

# ibrun is TACC's equivalent of mpiexec command 
ibrun ~/fds-6.7.5/Build/impi_intel_linux_64/fds_impi_intel_linux_64 inputFile.fds        # Replace input.fds with appropriate file           

### Run this script in the CLI by running the following command:
### sbatch slurm_script.sh