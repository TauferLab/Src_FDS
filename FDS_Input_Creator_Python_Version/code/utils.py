# Many of the functions in utils.py use variables defined within FDS.ipynb,
#  so those function can only be used from within that notebook by running the following:
#  %run -i code/utils.py

import pandas as pd
import numpy as np
import math
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import time
import os.path
from os import path
from time import time, strftime, gmtime, localtime

###################################################################################################
# Function that reads the elevation file

def read_elevation(name_of_file):
    Mst = pd.read_csv(name_of_file)
    Mst['x'] = Mst['x']-Mst['x'].min()
    Mst['y'] = Mst['y']-Mst['y'].min()
    Mst['Elevation'] = Mst['Elevation']-Mst['Elevation'].min()
    return Mst

# Writing the FDS file

def write_fds_file(T_begin, T_end, DT, PC, Nmx, Nmy, Nmz):
    NFRAMES  = int(2*(T_end-T_begin))
    #NFRAMES  = 40

    # Output File
    PC = 1       # Select to use Predictor-Corrector Strategy

    foldername = f"FDSPROG_{R}_Ro_{Ro}_[{Min_x},{Max_x}]x[{Min_y},{Max_y}]_PC_{PC}_T_{T_end}_DT_{DT}"
    filename = f"{foldername}.fds"
    logname = f"{foldername}.log"

    if not path.exists(f"FDSFiles/{foldername}"):
            os.mkdir(f"FDSFiles/{foldername}")
    log_name     = f"FDSFiles/{foldername}/{logname}"
    fds_filename = f"FDSFiles/{foldername}/{filename}"
    fds     = open(fds_filename, 'w')
    job_log = open(log_name, 'w')

    ############################################################
    Time = strftime("Experiment done: %Y/%m/%d/ at %H:%M:%S",localtime())
    job_log.write(f"{Time}\n\n")

    job_log.write(f"Terrain Domain  = [{Min_x}, {Max_x}] x [{Min_y}, {Max_y}]\n")
    job_log.write(f"Elevation Range = [{Min_z}, {Max_z}]\n\n")

    job_log.write(f"Resolution = {R} meters \n\n")
    DX  = (Max_x-Min_x)/Nmx
    DY  = (Max_y-Min_y)/Nmy
    DZ  = (Max_z-Min_z)/Nmz

    job_log.write(f"Number of Meshes = {Nmx*Nmy*Nmz} \n")
    fds.write(f"&HEAD CHID='Region_1_{R}m', TITLE='Simulation of Chimney Tops fire' /\n\n")
    Nx = math.ceil(DX/R)     # Number of cells in x-direction first mesh (Resolution)
    Ny = math.ceil(DY/R)     # Number of cells in y-direction first mesh (Resolution)
    Nz = math.ceil(DZ/R)     # Number of cells in z-direction first mesh (Resolution)

    job_log.write(f"Number of Cells = {Nx*Ny*Nz*Nmx*Nmy*Nmz} \n")
    job_log.write(f"Required Memory = {math.ceil(Nx*Ny*Nz*Nmx*Nmy*Nmz/1000000)} GB \n\n")
    fds.write(f"&MESH IJK={Nx},{Ny},{Nz}, XB={Min_x},{Min_x+DX},{Min_y},{Min_y+DY},{Min_z},{Min_z+DZ}, MULT_ID='mesh' / \n")
    fds.write(f"&MULT ID='mesh', DX={DX}, DY={DY}, DZ={DZ}, I_LOWER=0, I_UPPER={Nmx-1}, J_LOWER=0, J_UPPER={Nmy-1}, K_UPPER={Nmz-1} /  \n\n")
    fds.write("&MISC TMPA=30., TERRAIN_CASE=.TRUE., TERRAIN_IMAGE='Chimney_tops_aerial.png', VERBOSE=.TRUE., RESTART=.FALSE., PROJECTION=.TRUE.  /\n")

    if PC==0:
        fds.write(f"&TIME T_END = {T_end}, LOCK_TIME_STEP=.TRUE. /\n\n")
    else:
        fds.write(f"&TIME T_BEGIN = {T_begin}, T_END = {T_end} / \n\n")

    fds.write(f"&DUMP NFRAMES={NFRAMES}, DT_PART=100., CFL_FILE=.TRUE., DT_RESTART=60., DT_PL3D=60. /  \n")

    job_log.write(f"Simulation Time     = {T_end} \n")
    job_log.write(f"Time Step Size      = {DT} \n")
    job_log.write(f"Number of Frames    = {NFRAMES} \n\n")

    job_log.write(f"Predictor Corrector Strategy = {PC} \n\n")
    fds.write("&WIND DIRECTION=135., SPEED=5., SPONGE_CELLS=0, STRATIFICATION=.FALSE. /\n\n")

    fds.write(f"&SURF ID='FIRE', HRRPUA=1500., COLOR='ORANGE', RAMP_Q='fire' /\n")
    fds.write(f"&RAMP ID='fire', T= {int(T_begin)}., F=0. /\n")
    fds.write(f"&RAMP ID='fire', T= {int(T_begin+1)}., F=1. /\n")
    fds.write(f"&RAMP ID='fire', T= {int(T_begin+30)}., F=1. /\n")
    fds.write(f"&RAMP ID='fire', T= {int(T_begin+31)}., F=0. /\n\n")

    job_log.write(f"&RAMP ID='fire', T= 0., F=0. /\n")
    job_log.write(f"&RAMP ID='fire', T= 1., F=1. /\n")
    job_log.write(f"&RAMP ID='fire', T= 30., F=1. /\n")
    job_log.write(f"&RAMP ID='fire', T= 31., F=0. /\n\n")


    fds.write("&SLCF PBZ=1250., AGL_SLICE=1., QUANTITY='VELOCITY', VECTOR=.TRUE. /\n\n")

    fds.write("&VENT MB='XMIN', SURF_ID='OPEN' /  \n")
    fds.write("&VENT MB='XMAX', SURF_ID='OPEN' /  \n")
    fds.write("&VENT MB='YMIN', SURF_ID='OPEN' /  \n")
    fds.write("&VENT MB='YMAX', SURF_ID='OPEN' /  \n")
    fds.write("&VENT MB='ZMAX', SURF_ID='OPEN' /  \n\n")
    fds.write("&REAC FUEL='CELLULOSE', C=6, H=10, O=5, SOOT_YIELD=0.005 / \n\n")
    fds.write("&SPEC ID='WATER VAPOR' / \n\n")

    fds.write("&SURF ID                        = 'grass' \n")
    fds.write("      MATL_ID(1,1:2)            = 'GENERIC VEGETATION','MOISTURE'\n")
    fds.write("      MATL_MASS_FRACTION(1,1:2) = 0.937,0.063\n")
    fds.write("      THICKNESS                 = 0.0002\n")
    fds.write("      LENGTH                    = 0.21\n")
    fds.write("      HEAT_TRANSFER_COEFFICIENT = 30.\n")
    fds.write("      GEOMETRY                  = 'CYLINDRICAL' /\n\n")

    fds.write("&SURF ID                        = 'needles' \n")
    fds.write("      MATL_ID(1,1:2)            = 'GENERIC VEGETATION','MOISTURE'\n")
    fds.write("      MATL_MASS_FRACTION(1,1:2) = 0.95,0.05\n")
    fds.write("      THICKNESS                 = 0.02\n")
    fds.write("      LENGTH                    = 0.21\n")
    fds.write("      HEAT_TRANSFER_COEFFICIENT = 30.\n")
    fds.write("      GEOMETRY                  = 'CYLINDRICAL' /\n\n")

    fds.write("&MATL ID = 'GENERIC VEGETATION' \n")
    fds.write("      DENSITY = 500.\n")
    fds.write("      CONDUCTIVITY = 0.1\n")
    fds.write("      SPECIFIC_HEAT= 1.5\n")
    fds.write("      REFERENCE_TEMPERATURE = 200\n")
    fds.write("      PYROLYSIS_RANGE = 30.\n")
    fds.write("      NU_MATL = 0.2\n")
    fds.write("      NU_SPEC = 0.8 \n")
    fds.write("      SPEC_ID = 'CELLULOSE'\n")
    fds.write("      HEAT_OF_COMBUSTION = 15600.\n")
    fds.write("      HEAT_OF_REACTION = 418.\n")
    fds.write("      MATL_ID  = 'CHAR' /\n\n")

    fds.write("&MATL ID = 'MOISTURE' \n")
    fds.write("      DENSITY = 1000.\n")
    fds.write("      CONDUCTIVITY = 0.1\n")
    fds.write("      SPECIFIC_HEAT= 4.184\n")
    fds.write("      REFERENCE_TEMPERATURE = 100.\n")
    fds.write("      PYROLYSIS_RANGE = 10.\n")
    fds.write("      NU_SPEC = 1.0 \n")
    fds.write("      SPEC_ID = 'WATER VAPOR'\n")
    fds.write("      HEAT_OF_REACTION = 2500./\n\n")

    fds.write("&MATL ID = 'CHAR'\n")
    fds.write("      DENSITY  = 100.\n")
    fds.write("      CONDUCTIVITY = 0.1 \n")
    fds.write("      SPECIFIC_HEAT = 1.0 / \n\n")

    fds.write("&MATL ID='DIRT'\n")
    fds.write("      CONDUCTIVITY = 0.25\n")
    fds.write("      SPECIFIC_HEAT = 2.\n")
    fds.write("     DENSITY = 1300. /\n\n")

    fds.write("&PART ID='foliage', DRAG_COEFFICIENT=1.0, SURF_ID='needles', SAMPLING_FACTOR=5,\n")
    fds.write("      QUANTITIES='PARTICLE TEMPERATURE','PARTICLE MASS','PARTICLE DIAMETER', STATIC=.TRUE., COLOR='GREEN' / \n\n")

    fds.write("&PART ID='grass', DRAG_COEFFICIENT=1.0, SURF_ID='grass', SAMPLING_FACTOR=958,\n")
    fds.write("      QUANTITIES='PARTICLE TEMPERATURE','PARTICLE MASS','PARTICLE DIAMETER', STATIC=.TRUE., COLOR='BROWN' /\n\n")

    fds.write("&SURF ID = 'surf1', RGB = 122,117,48, MATL_ID='DIRT', THICKNESS=0.2, PART_ID='grass', PARTICLE_SURFACE_DENSITY=1.0 / \n")
    fds.write("&SURF ID = 'surf2', RGB = 0,100,0, MATL_ID='DIRT', THICKNESS=0.2 / \n\n")
    rows = Mst_o.shape[0]
    # Position of the ignition point
    Location = [500,100]
    # Locating that position in the Moisture File
    Indice = Mst_o[(Mst_o['x'] < Location[0]+5) & (Mst_o['x'] > Location[0]-5) & (Mst_o['y'] < Location[1]+5) & (Mst_o['y'] > Location[1]-5)].index
    Indice2 = [i for i in Mst_o.index if i not in Indice.values]

    job_log.write(f"Coordinates of the Fire   = {Location}")
    # Writing the location of the fire
    for ind in Indice.values:
        #min_obstacle = max([Min_z0, Mst_o['Elevation'][ind]-Ro])
        min_obstacle = Min_z
        fds.write(f"&OBST XB={Mst_o['x'][ind]},{Mst_o['x'][ind]+Ro},{Mst_o['y'][ind]},{Mst_o['y'][ind]+Ro},{min_obstacle},{Mst_o['Elevation'][ind]} SURF_IDS='FIRE','surf1' /\n")

    # Writing the obstacles  [x for x in xrange(100) if x != 50]

    for i in Indice2: 
        #min_obstacle = max([Min_z0, Mst_o['Elevation'][i]-Ro])
        min_obstacle = Min_z
        fds.write(f"&OBST XB={Mst_o['x'][i]},{Mst_o['x'][i]+Ro},{Mst_o['y'][i]},{Mst_o['y'][i]+Ro},{min_obstacle},{Mst_o['Elevation'][i]} SURF_ID='surf1'/\n")

    fds.write("\n&TAIL /")
    bsub_name     = f"FDSFiles/{foldername}/fds_testing.bsub"
    bsub          = open(bsub_name, 'w')

    bsub.write("#!/bin/bash\n")
    bsub.write("#BSUB -n 1\n")
    bsub.write("#BSUB -J mesh_\n")
    bsub.write("###BSUB -x\n")
    bsub.write('###BSUB -R "span[hosts=1]"\n')
    bsub.write("#BSUB -o /home/leobardovalera/experiments/mesh_%J.out\n")
    bsub.write("#BSUB -e /home/leobardovalera/experiments/mesh_%J.err\n")
    bsub.write("##BSUB -W 1:00\n\n")

    bsub.write("export OMP_NUM_THREADS=4\n")
    bsub.write(f"mpiexec -n {Nmx*Nmy*Nmz} ~/fds/Build/mpi_gnu_linux_64/fds_mpi_gnu_linux_64 {filename}")
    fds.close()
    job_log.close()
    bsub.close()
    

