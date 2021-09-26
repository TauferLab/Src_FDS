% This script reads the csv file containing the heat release vlues on
% a domain for each cell and plot them
close all
clear all

hrr_region1 = '../../../data/Initialization/region1_hrrpuv.csv';
hrr_region2 = '../../../data/Initialization/region2_hrrpuv.csv';

[x1,y1,z1,hrr1]=csvimport(hrr_region1, 'columns', {'x', 'y', 'z','hrr'});
[x2,y2,z2,hrr2]=csvimport(hrr_region2, 'columns', {'x', 'y', 'z','hrr'});



scatter3(x1,y1,z1,'r')

figure()

scatter3(x2,y2,z2,'r')


