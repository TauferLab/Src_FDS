load devices2.mat

plot(Time, DEV_1,'linewidth',2.0)

grid on

xl = xlabel('{\bf Time}');
yl = ylabel('{\bf Mass lost Rate}');
tl = title('{\bf Device 1}');

set(xl,'interpreter','latex','fontsize',14)
set(yl,'interpreter','latex','fontsize',14)
set(tl,'interpreter','latex','fontsize',16)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure()
plot(Time, DEV_5V,'linewidth',2.0)

grid on

xl = xlabel('{\bf Time}');
yl = ylabel('{\bf Velovity}');
tl = title('{\bf Device 5}');

set(xl,'interpreter','latex','fontsize',14)
set(yl,'interpreter','latex','fontsize',14)
set(tl,'interpreter','latex','fontsize',16)
