% Reading the file with the smoke3d visualization

% Select the parameter to plot
% SOOT                   n = 1
% HRRPUV                 n = 2
% TEMPERATURE            n = 3
% CARBON DIOXITY DENSITY n = 4
clear all
close all
%load smoke3d_hrrpuv.mat
n = 2;

% Input the number of meshes

nm = 16;

% Path
hrr_region1 = '../../../simulations/Gatlinburg3/Whole1/';
% Input the name of CHILD name:
child = 'Whole1_cat_';


hrr_file = [hrr_region1,child,'hrr.csv'];

Time = csvimport(hrr_file, 'columns', 'Time' );

 for l =1 : nm
     file = [hrr_region1,child,num2str(l,'%04d'),'_',num2str(n,'%04d'),'.dat'];
     %hrrpuv(:,l) = csvimport(file, 'columns', [1] ,'noHeader', true);
     hrrpuv_whole(:,l) = load(file);
     hrrpuv_whole = sparse(hrrpuv_whole);
 end
 %hrrpuv_whole = sparse(hrrpuv_whole);

Domain = [200 700;200 700;380 620];
Resolution = 4;

Nmx = 2;
Nmy = 2;
Nmz = 4;
number_of_meshes = Nmx*Nmy*Nmz;

Ncx = 63; %(Domain(1,2)- Domain(1,1))/(Resolution * Nmx);
Ncy = 63; %(Domain(2,2)- Domain(2,1))/(Resolution * Nmy);
Ncz = 15; %(Domain(3,2)- Domain(3,1))/(Resolution * Nmz);

indice = 1;
for k = 0:Ncz+1
    for j = 0:Ncy+1
        for i=0:Ncx+1
            INDEX(indice,1) = i*Resolution;
            INDEX(indice,2) = j*Resolution;
            INDEX(indice,3) = k*Resolution;
            indice = indice + 1; 
        end
    end
end

% Corner of the meshes
DX = (Domain(1,2)- Domain(1,1))/Nmx;
DY = (Domain(2,2)- Domain(2,1))/Nmy;
DZ = (Domain(3,2)- Domain(3,1))/Nmz;

mesh_index = 1;
for k =1:Nmz
    for j=1:Nmy
        for i =1:Nmx
        Meshes(mesh_index,1) =   Domain(1,1) + (i-1)*DX;
        Meshes(mesh_index,2) =   Domain(2,1) + (j-1)*DY;
        Meshes(mesh_index,3) =   Domain(3,1) + (k-1)*DZ;
        mesh_index = mesh_index+1;
        end
    end
end

% Plotting for each value of t
Number_of_cells = (Ncz+2)*(Ncy+2)*(Ncx+2);


for t = 1:length(Time)
   Q_whole = [];
   for j=1:number_of_meshes
    temp = [INDEX(:,1)+ Meshes(j,1) INDEX(:,2)+ Meshes(j,2) INDEX(:,3)+ Meshes(j,3) hrrpuv_whole((t-1)*Number_of_cells+1:t*Number_of_cells,j)];
    temp = temp(temp(:,4)>0,:);
    Q_whole = [Q_whole;temp];
   end
   cla
   plot3(Q_whole(:,1),Q_whole(:,2),Q_whole(:,3),'.','Color',[1,0,0])
   grid on
   axis([Domain(1,:) Domain(2,:) Domain(3,:)])
   pause(.125)
 
end

            