#!/usr/bin/env python
"""
Sample script that uses the plot_elevation module created using
MATLAB Compiler SDK.

Refer to the MATLAB Compiler SDK documentation for more information.
"""

from __future__ import print_function
import plot_elevation
import matlab

my_plot_elevation = plot_elevation.initialize()

file_pathIn = "/home/leobardo/Documents/Dr Taufer Lab/experiments/Src_FDS/PythonVersion/MoistureFile/MoistureAndElevationUTMTraslated201610.csv"
my_plot_elevation.plot_elevation(file_pathIn, nargout=0)

my_plot_elevation.terminate()
