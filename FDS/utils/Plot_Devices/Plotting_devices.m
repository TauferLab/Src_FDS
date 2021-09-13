% Loading the values of the Devices for the Region1
load ../../../data/DevicesRegion1.mat
close all

x = 502:2:698;
x = x';
y = 202:2:398;
y = y';

[X,Y] = meshgrid(x,y);

X = X(:);
Y = Y(:);
Devices_Region1 = [X Y];

 for i = 3:123
     Devices_Region1(:,i) = A(i,:)'; 
 end
     
writematrix(Devices_Region1,'../../../data/devices_region1.csv')