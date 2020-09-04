% Defining the the Domain
clc

% First Point
x0 = 450;
y0 = 450;
z0 = 1200;

% Last point
xn = 550;
yn = 550;
zn = 1350;

%Resolution
Nx = 100.0;
Ny = 100.0;
Nz = 100.0;


dx = (xn-x0)/Nx;
dy = (yn-y0)/Ny;
dz = (zn-z0)/Ny;

% Plotting the domain

%plotting_cube([x0,y0,z0],[xn,yn,zn],'blue')
%axis([450 550 450 550 1200 1350])
view([-36.6163, 7.2000])
hold on
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% How many meshes we have
Nmx = 2;
Nmy = 2;
Nmz = 2;

DX = (xn-x0)/Nmx;
DY = (yn-y0)/Nmy;
DZ = (zn-z0)/Nmz;

X0 = x0;
Y0 = y0;
Z0 = z0;

XN = X0+DX;
YN = Y0+DY;
ZN = Z0+DZ;

I_LOWER = 0;
I_UPPER = Nmx-1;

J_LOWER = 0;
J_UPPER = Nmy-1;

K_LOWER = 0;
K_UPPER = Nmz-1;

for k = K_LOWER:K_UPPER
    for j=J_LOWER:J_UPPER
        for i = I_LOWER:I_UPPER
          XBL = X0 + i*DX;
          XBU = XN + i*DX;
          
          YBL = Y0 + j*DY;
          YBU = YN + j*DY;
          
          ZBL = Z0 + k*DZ;
          ZBU = ZN + k*DZ;
          plotting_cube([XBL,YBL,ZBL],[XBU,YBU,ZBU],'blue')
        end
    end
end
          
          
          


          

