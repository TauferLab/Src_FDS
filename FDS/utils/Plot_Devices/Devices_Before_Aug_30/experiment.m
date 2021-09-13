load devices
close all
var1 = Whole_dev(Whole_dev(:,1)<=12,:);
var2 = Region1_dev(Region1_dev(:,1)<=12,:);

plot(var1(:,1), var1(:,2),'linewidth',2.0)

hold on

plot(var2(:,1), var2(:,2),'linewidth',2.0)

grid on

xl = xlabel('{\bf Time}');
yl = ylabel('{\bf Mass lost Rate}');
tl = title('{\bf Device 1}');

set(xl,'interpreter','latex','fontsize',14)
set(yl,'interpreter','latex','fontsize',14)
set(tl,'interpreter','latex','fontsize',16)

 
leg = legend('Nist', 'Region 1 (2x2x4)');
set(leg,'interpreter','latex','Location','Best','fontsize',16)
