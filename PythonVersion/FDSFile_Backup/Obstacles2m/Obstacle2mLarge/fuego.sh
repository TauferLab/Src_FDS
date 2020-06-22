#!/bin/bash

export OMP_NUM_THREADS=4
mpiexec -n $1 fds FDSPROG_2m.fds
