function plot_elevation(file_path)

M = readmatrix(file_path);

X = reshape(M(:,1),1000,1000);

Y = reshape(M(:,2),1000,1000);

Z = reshape(M(:,4),1000,1000);

num = max(M(:,4))-min(M(:,4));

MyMap(:,1) = (1/255)*linspace(12,61,num);
MyMap(:,2) = (1/255)*linspace(51,254,num);
MyMap(:,3) = (1/255)*linspace(7,34,num);

colormap(MyMap)

s = surf(X,Y,Z);

x_label = xlabel('Longitude (East-West)');

y_label = ylabel('Latitude (North-South)');

set(x_label,'FontSize', 14,'Interpreter','latex')
set(y_label,'FontSize', 14,'Interpreter','latex')


s.EdgeColor = 'none';
