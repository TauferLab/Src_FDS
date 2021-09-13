load Regiones2_Mediano.mat
close all
XT = [fourhrr(:,1); Region2620x2([11:end],1)];
X  = [fourhrr(:,2); Region2620x2([11:end],2)];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

YT = Mediano(:,1);
Y  = Mediano(:,2);

t0 = 0;
tn = 66;
[rmse,P,Mb] = correlation_rsme(XT,X,YT,Y, t0, tn);

xl = xlabel('{\bf Heat release rate on $Region_1$ and $Region_2$}');
yl = ylabel('\bf {Heat release rate on Hull($Region_1$, $Region_2$)}');

set(xl,'interpreter','latex','fontsize',16)
set(yl,'interpreter','latex','fontsize',16)

Data2 = [' $y =',num2str(Mb(1)),'x+',num2str(Mb(2)), '$'];

leg = legend('Data', Data2);
set(leg,'interpreter','latex','Location','Best','fontsize',16)
