# Many of the functions in utils.py use variables defined within FDS.ipynb,
#  so those function can only be used from within that notebook by running the following:
#  %run -i code/utils.py

import pandas as pd
import numpy as np
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time
import os.path

from PIL import Image
from mpl_toolkits import mplot3d
from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from os import path
from lsf import LSFMonitor
from slurm import SlurmMonitor


###################################################################################################
# Function that reads the elevation file

def read_elevation(name_of_file):
    Mst = pd.read_csv(name_of_file)
    Mst['x'] = Mst['x']-Mst['x'].min()
    Mst['y'] = Mst['y']-Mst['y'].min()
    Mst['Elevation'] = Mst['Elevation']-Mst['Elevation'].min()
    return Mst

# Writing the FDS file

def write_fds_file(T_begin, T_end, DT, PC, Nmx, Nmy, Nmz, Hrr, Child):
    global fds
    global job_log
    global foldername
    global filename
    global Dx
    global Nx
    global Dy
    global Ny
    global Dz
    global Nz
    global Dx
    global Nx
    global Rx
    global Ry
    global Rz
    
    NFRAMES  = int(2*(T_end-T_begin))

    # Output File
    Indice = Hrr.index
    Indice2 = [i for i in Mst.index if i not in Indice.values]

    if not path.exists(f"{PATH}/FDSFiles"):
            os.mkdir(f"{PATH}/FDSFiles")
    
    if not path.exists(f"{PATH}/FDSFiles/{foldername}"):
            os.mkdir(f"{PATH}/FDSFiles/{foldername}")

    fds_filename = f"{PATH}/FDSFiles/{foldername}/{filename}"
    fds     = open(fds_filename, 'w')

    ############################################################
    # Drawing the area of the region of interest and cropping ot
    draw_rectangle(Image_name,Min_x,Max_y,float(Max_x-Min_x),float(Max_y-Min_y), f"{PATH}/FDSFiles/{foldername}/BigRegion1.png",'w')
    
    # Cropping the region from the Big Region
    crop_rectangle(Image_name,Min_x,Max_x,Min_y,Max_y,f"{PATH}/FDSFiles/{foldername}/Region1.png")
    
    ############################################################
    DX  = (Max_x-Min_x)/Nmx
    DY  = (Max_y-Min_y)/Nmy
    DZ  = (Max_z-Min_z)/Nmz

    fds.write(f"&HEAD CHID='{Child}', TITLE='Simulation of Chimney Tops fire' /\n\n")
    Nx = math.ceil(DX/R)     # Number of cells in x-direction first mesh (Resolution)
    Ny = math.ceil(DY/R)     # Number of cells in y-direction first mesh (Resolution)
    Nz = math.ceil(DZ/R)     # Number of cells in z-direction first mesh (Resolution)
    
    Rx = DX/Nx
    Ry = DY/Ny 
    Rz = DZ/Nz

    fds.write(f"&MESH IJK={Nx},{Ny},{Nz}, XB={Min_x},{Min_x+DX},{Min_y},{Min_y+DY},{Min_z},{Min_z+DZ}, MULT_ID='mesh' / \n")
    fds.write(f"&MULT ID='mesh', DX={DX}, DY={DY}, DZ={DZ}, I_LOWER=0, I_UPPER={Nmx-1}, J_LOWER=0, J_UPPER={Nmy-1}, K_UPPER={Nmz-1} /  \n\n")
    fds.write("&MISC TMPA=30., TERRAIN_CASE=.TRUE., TERRAIN_IMAGE='Region1.png', VERBOSE=.TRUE., RESTART=.FALSE., PROJECTION=.TRUE.  /\n")
    
    fds.write(f"&TIME T_BEGIN = {T_begin}, T_END = {T_end} / \n\n")

    fds.write(f"&DUMP NFRAMES={NFRAMES}, DT_PART=100., CFL_FILE=.TRUE., DT_PL3D={int(T_end)}. /  \n")

    fds.write("&WIND DIRECTION=135., SPEED=5., SPONGE_CELLS=0, STRATIFICATION=.FALSE. /\n\n")

    for k in Hrr.index:
        fds.write(f"&SURF ID='FIRE{k}', HRRPUA={math.ceil(Hrr['hrr'][k])}., COLOR='ORANGE', RAMP_Q='fire' /\n")
    
    fds.write(f"\n")
    
    fds.write(f"&RAMP ID='fire', T= {int(T_begin)}., F=0. /\n")
    fds.write(f"&RAMP ID='fire', T= {int(T_begin+1)}., F=1. /\n")
    fds.write(f"&RAMP ID='fire', T= {int(T_begin+30)}., F=1. /\n")
    fds.write(f"&RAMP ID='fire', T= {int(T_begin+31)}., F=0. /\n\n")

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
    
    ###################################################################################################################################
    # Writing the obstacles
    Mst_fire    = Mst.loc[Hrr.index.values]                              # Obstacles on fire
    
    indice2 = [i for i in Mst.index.values if i not in Hrr.index.values] # Index of obstacles on fire 
    
    Mst_no_fire = Mst.loc[indice2]                                       # Obstacles with no fire
    
    # Writing the location of the fire
    for ind in Mst_fire.index:

        fds.write(f"&OBST XB={Mst_fire['x'][ind]},{Mst_fire['x'][ind]+Ro},{Mst_fire['y'][ind]},{Mst_fire['y'][ind]+Ro},{Min_z},{Mst_fire['Elevation'][ind]} SURF_IDS='FIRE{ind}','surf1' /\n")
        
    for ind in Mst_no_fire.index:

        fds.write(f"&OBST XB={Mst_no_fire['x'][ind]},{Mst_no_fire['x'][ind]+Ro},{Mst_no_fire['y'][ind]},{Mst_no_fire['y'][ind]+Ro},{Min_z},{Mst_no_fire['Elevation'][ind]} SURF_ID='surf1' /\n")        
    
########################################################################################################################################
    
    
    fds.close()
    
###############################################################################################################

def restart_fds_file(T_begin, T_end, DT, PC, Nmx, Nmy, Nmz, Hrr, Child):
    global fds
    global job_log
    global foldername
    global filename
    global Dx
    global Nx
    global Dy
    global Ny
    global Dz
    global Nz
    global Dx
    global Nx
    global Rx
    global Ry
    global Rz
    global rampa_time
                  
    NFRAMES  = int(2*(T_end-T_begin))

    # Output File
    Indice = Hrr.index
    Indice2 = [i for i in Mst.index if i not in Indice.values]

    if not path.exists(f"{PATH}/FDSFiles"):
            os.mkdir(f"{PATH}/FDSFiles")
    
    if not path.exists(f"{PATH}/FDSFiles/{foldername}"):
            os.mkdir(f"{PATH}/FDSFiles/{foldername}")

    fds_filename = f"{PATH}/FDSFiles/{foldername}/{filename}"
    fds     = open(fds_filename, 'w')

    ############################################################
    # Drawing the area of the region of interest and cropping it
    print(Min_x, Max_y)
    draw_rectangle(f"{PATH}/FDSFiles/{foldername}/BigRegion{num_region-1}.png",Min_x,Max_y,float(Max_x-Min_x),float(Max_y-Min_y), f"{PATH}/FDSFiles/{foldername}/Big{Child}.png",'w')
    
    # Cropping the region from the Big Region
    crop_rectangle(Image_name,Min_x,Max_x,Min_y,Max_y,f"{PATH}/FDSFiles/{foldername}/{Child}.png")
    

   
    DX  = (Max_x-Min_x)/Nmx
    DY  = (Max_y-Min_y)/Nmy
    DZ  = (Max_z-Min_z)/Nmz

    fds.write(f"&HEAD CHID='{Child}', TITLE='Simulation of Chimney Tops fire' /\n\n")
    Nx = math.ceil(DX/R)     # Number of cells in x-direction first mesh (Resolution)
    Ny = math.ceil(DY/R)     # Number of cells in y-direction first mesh (Resolution)
    Nz = math.ceil(DZ/R)     # Number of cells in z-direction first mesh (Resolution)

    fds.write(f"&MESH IJK={Nx},{Ny},{Nz}, XB={Min_x},{Min_x+DX},{Min_y},{Min_y+DY},{Min_z},{Min_z+DZ}, MULT_ID='mesh' / \n")
    fds.write(f"&MULT ID='mesh', DX={DX}, DY={DY}, DZ={DZ}, I_LOWER=0, I_UPPER={Nmx-1}, J_LOWER=0, J_UPPER={Nmy-1}, K_UPPER={Nmz-1} /  \n\n")
    fds.write(f"&MISC TMPA=30., TERRAIN_CASE=.TRUE., TERRAIN_IMAGE='{Child}.png', VERBOSE=.TRUE., RESTART=.FALSE., PROJECTION=.TRUE.  /\n")
    
    fds.write(f"&TIME T_BEGIN = {T_begin}, T_END = {T_end} / \n\n")

    fds.write(f"&DUMP NFRAMES={NFRAMES}, DT_PART=100., CFL_FILE=.TRUE., DT_PL3D={int(DTT)}. /  \n")

    fds.write("&WIND DIRECTION=135., SPEED=5., SPONGE_CELLS=0, STRATIFICATION=.FALSE. /\n\n")
    
    print(Hrr['hrr'].sum())   
    for ind in Hrr.index:
        x = Hrr['x'][ind]
        y = Hrr['y'][ind] 
        Rx = DX/Nx
        Ry = DY/Ny 
        Rz = DZ/Nz
        
        fds.write(f"&RADI KAPPA0=0 /\n")
        
        fds.write(f"&INIT XB={Hrr['x'][ind]},{Hrr['x'][ind]+Rx},{Hrr['y'][ind]},{Hrr['y'][ind]+Ry},{Hrr['z'][ind]},{Hrr['z'][ind]+Rz}, HRRPUV={Hrr['hrr'][ind]/(Rx*Ry*Rz)}, RAMP_Q='fire', RADIATIVE_FRACTION={rad_frac}/\n")

    
    fds.write(f"\n")
    
    fds.write(f"&RAMP ID='fire', T= {int(T_begin)}, F=1. /\n")
    fds.write(f"&RAMP ID='fire', T= {float(T_begin+rampa_time)}, F=0. /\n")
    #fds.write(f"&RAMP ID='fire', T= {int(T_begin+30)}, F=0. /\n\n")

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
    
    ###################################################################################################################################
    # Writing the obstacles
                                    # Obstacles with no fire
    for ind in Mst.index:

        fds.write(f"&OBST XB={Mst['x'][ind]},{Mst['x'][ind]+Ro},{Mst['y'][ind]},{Mst['y'][ind]+Ro},{Min_z},{Mst['Elevation'][ind]} SURF_ID='surf1' /\n")        
    
########################################################################################################################################
    
    
    fds.close()
    
###############################################################################################################

## Bash/system/OS interaction.

import sys
import os
import subprocess
from subprocess import Popen

def bash(argv):
    arg_seq = [str(arg) for arg in argv]
    #print(arg_seq)
    proc = Popen(arg_seq)#, shell=True)
    proc.wait() #... unless intentionally asynchronous

###############################################################################################################

def reading_hrr(Child, Number_of_meshes):
    filename_txt           = f"fds2ascii.txt"
    fds2ascii_filename = f"{PATH}/FDSFiles/{foldername}/{filename_txt}"
    f2a          = open(fds2ascii_filename, 'w')

    f2a.write(f"{Child} \n")
    f2a.write(f"1\n")
    f2a.write(f"1\n")
    f2a.write(f"n\n")
    for i in range(1,Number_of_meshes+1):
        f2a.write(f"{i}\n")
        f2a.write(f"{Child}_{i}.csv\n")
    f2a.write(f"0\n")
    f2a.close()
    os.chdir(PATH)
    os.chdir(FDS_FOLDER)
    os.system(f"{fds2ascii} < {filename_txt}")
    
##########################################################################
    
def remove_leading_space(file_name):
    # Open the file in read only mode
    Temp_file     = open(f'{file_name[0:-4]}_1.tmp', 'w')
    
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if '.q' in line:
                Temp_file.write(line.lstrip())
            else:
                Temp_file.write(line)
    
    Temp_file.close()
    os.system(f"rm {file_name}")
    os.system(f"mv {file_name[0:-4]}_1.tmp {file_name}")
    return 0    

##########################################################################

def create_job_script_lsf(Child, num_nodes, max_time, omp_threads):
    
    # Create the job submission file for specific region
    job_filename = f"job_{Child}.bsub"
    job_script = open(f"{PATH}/FDSFiles/{foldername}/{job_filename}", 'w')
    
    # Write the contents of the file
    job_script.write("#!/bin/bash\n\n")
    job_script.write(f"#BSUB -n {num_nodes}\n") # Number of compute nodes
    job_script.write(f"#BSUB -J {jobName}\n") # Job Name
    
    output_path = f'{PATH}/FDSFiles/{foldername}/{jobName}_%J'
    job_script.write(f"#BSUB -o {output_path}.out\n")  # Job output file
    job_script.write(f"#BSUB -e {output_path}.err\n")  # Job error file
    
    job_script.write(f"#BSUB -W {max_time}\n\n")       # Maximum time to run on compute node(s)
    
    job_script.write(f"export OMP_NUM_THREADS={omp_threads}\n")                 # Number of OpenMP threads per process
    job_script.write(f"mpiexec -n {number_of_process} {fds_bin} {filename}\n")  # Executes fds on input FDS file
    
    return 0

##########################################################################

def create_job_script_slurm(Child, num_nodes, max_time, omp_threads):
    # Create the job submission file for specific region
    job_filename = f"job_{Child}.sh"
    job_script = open(f"{PATH}/FDSFiles/{foldername}/{job_filename}", 'w')
    
    # Write the contents of the file
    job_script.write("#!/bin/bash\n\n")
    job_script.write(f"#SBATCH --job-name={jobName}\n")         # Job Name 
    
    output_path = f'{PATH}/FDSFiles/{foldername}/{jobName}_%j'
    job_script.write(f"#SBATCH --output={output_path}.out\n")   # Job output file
    job_script.write(f"#SBATCH --error={output_path}.err\n")    # Job error file
    
    job_script.write(f"#SBATCH --nodes={num_nodes}\n")          # Number of compute nodes
    job_script.write(f"#SBATCH --ntasks={number_of_process}")   # Number of MPI processes
    job_script.write(f"#SBATCH --time={max_time}\n\n")          # Max time to run on compute node(s) - (d-hh:mm:ss)
    
    #SBATCH --partition={partition}                             # Specified partition on TACC's Stampede2
    
    job_script.write(f"#SBATCH --mail-user={email}")
    job_script.write(f"#SBATCH --mail-type=all")
    
    job_script.write(f"export OMP_NUM_THREADS={omp_threads}\n") # Number of OpenMP threads per process
    job_script.write(f"ibrun {fds_bin} {filename}\n")           # Executes fds on input FDS file
    
    return 0
    
##########################################################################

def wait_on_lsf():
    monitor = LSFMonitor(USER, jobs) 
    monitor.wait_on_job(jobs[0])  # Waits for the job specified by the user to finish to run the rest of the notebook
    return 0

##########################################################################

def wait_on_slurm():
    monitor = SlurmMonitor(USER, jobs)
    monitor.wait_on_job(jobs[0])  # Waits for the job specified by the user to finish to run the rest of the notebook
    return 0

#############################################################################

def Get_job_id(argv):
    arg_seq = [str(arg) for arg in argv]
    outfile = open('temp.csv', 'w');
    proc = Popen(arg_seq, bufsize=0, stdout=outfile)
    outfile.close()
    proc.wait() #... unless intentionally 
    
    # Using readlines() 
    file1 = open('temp.csv', 'r') 
    Lines = file1.readlines() 
    job_id = Lines[1].split()[0]
    return job_id
###############################################################################
def return_elevation(Mst, x, y):
    elevation = Mst[(Mst['x']==x) & (Mst['y']==y)]['Elevation']
    elevation = int(elevation)
    return elevation

def delete_under(Hrr):
    
    for ind in Hrr.index:
        x = Hrr['x'][ind]
        y = Hrr['y'][ind] 
        elevation = return_elevation(Mst, x, y)
        diferencia = elevation - Hrr['z'][ind]
        if (diferencia>0):
            Hrr = Hrr.drop([ind])
      
    return Hrr

########################################################################################

def draw_rectangle(image_in,xlb,yub,width0,height0,image_out,color):
    # Drawing a rectangle in a picture
    dpi = 80
    img = matplotlib.image.imread(image_in)
    height, width, nbands = img.shape
    
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)
    
    figure = plt.figure(figsize=figsize)
    ax = figure.add_axes([0, 0, 1, 1])
    # Hide spines, ticks, etc.
    ax.axis('off')
    rect = matplotlib.patches.Rectangle((xlb,1000-yub),width0,height0, edgecolor=color, facecolor="none")   
    ax.imshow(img)
    ax.add_patch(rect)
    figure.savefig(image_out,dpi=dpi,transparent=True)
    return 0

def crop_rectangle(image_in,xlb,xub,ylb,yub,image_out):
    # Cropping a rectangle from a picture
    im  = Image.open(image_in)
    box = (xlb,1000-yub,xub,1000-ylb)
    im.crop(box).save(image_out)