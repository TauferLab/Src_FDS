% This script reads the csv file containing the heat release vlues on
% a domain for each cell and plot them
close all
clear all

hrr_region1 = '../../../simulations/Gatlinburg_R2/Region1/Region1_hrr.csv';


[x1,y1]=csvimport(hrr_region1, 'columns', {'Time', 'HRR'});




