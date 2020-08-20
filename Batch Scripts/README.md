# How to write job submission scripts for your cluster's job scheduler

## IBM's LSF

- This job scheduler is used on Tellico. Below is an example job submission script for running an FDS input file:

```
    #!/bin/bash
    #BSUB -n 1
    #BSUB -J mesh_
    #BSUB -o /home/userName/experiments/mesh_%J.out
    #BSUB -e /home/userName/experiments/mesh_%J.err
    #BSUB -W 1:00

    export OMP_NUM_THREADS=4
    mpiexec -n 8 ~/fds/Build/mpi_gnu_linux_64/fds_mpi_gnu_linux_64 inputFile.fds
```

> #BSUB -n 1       
- Specifies the number of nodes the user wants to use.

> #BSUB -J mesh_   
- Specifies the job name.

> #BSUB -o /home/userName/experiments/mesh_%J.out   
- Specifies job output file name. %J is the job number.

> #BSUB -e /home/userName/experiments/mesh_%J.err   
- Specifies job error file name. %J is the job number.

> #BSUB -W 1:00    
- Specifies time limit for job to complete in hours, in this case 1 hour.

> export OMP_NUM_THREADS=4   
- Specifies OpenMP threads to be assigned to each core used, in this case 4 OMP threads.

> mpiexec -n 8 ~/fds/Build/mpi_gnu_linux_64/fds_mpi_gnu_linux_64 inputFile.fds   
- Command to run FDS in parallel using MPI. In this case, we are running on 8 cores as denoted by "-n 8".


### Once done...

Once you are done writing your .bsub file, you will have to write the following command to run the job script: `bsub < bsubFileName.bsub'
