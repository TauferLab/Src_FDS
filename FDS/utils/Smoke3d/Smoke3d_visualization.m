% Reading the file with the smoke3d visualization

% Select the parameter to plot
% SOOT                   n = 1
% HRRPUV                 n = 2
% TEMPERATURE            n = 3
% CARBON DIOXITY DENSITY n = 4
clear all
load smoke3d_hrrpuv.mat
n = 2;

% Input the number of meshes

nm = 16;

% Path
hrr_region1 = '../../../simulations/Gatlinburg2/';

% Input the name of CHILD name:
child = 'Region1_cat_';

% for l =1 : nm
%     file = [hrr_region1,child,num2str(l,'%04d'),'_',num2str(n,'%04d'),'.dat'];
%     hrrpuv(:,l) = csvimport(file, 'columns', [1] ,'noHeader', true);
% end

Domain = [500 700;200 400;380 620];
Resolution = 2;

Nmx = 2;
Nmy = 2;
Nmz = 4;

Ncx = (Domain(1,2)- Domain(1,1))/(Resolution * Nmx);
Ncy = (Domain(2,2)- Domain(2,1))/(Resolution * Nmy);
Ncz = (Domain(3,2)- Domain(3,1))/(Resolution * Nmz);

l = 1;


