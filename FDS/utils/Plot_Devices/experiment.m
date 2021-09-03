load Devices.mat
close all
XT = Wholedevc(Wholedevc(:,1)<=120,1);
X  = Wholedevc(Wholedevc(:,1)<=120,6);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

YT = Region1devc(:,1);
Y  = Region1devc(:,6);

t0 = 0;
tn = 120;
[rmse,P,Mb] = correlation_rsme(XT,X,YT,Y, t0, tn);

xl = xlabel('{\bf Velocity on Whole Region}');
yl = ylabel('\bf {Velocity on Region1}');

set(xl,'interpreter','latex','fontsize',16)
set(yl,'interpreter','latex','fontsize',16)

Data2 = [' $y =',num2str(Mb(1)),'x+',num2str(Mb(2)), '$'];

leg = legend('Data', Data2);
set(leg,'interpreter','latex','Location','Best','fontsize',16)
