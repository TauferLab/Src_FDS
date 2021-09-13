load Devices.mat


plot(Wholedevc(:,1),Wholedevc(:,2),'linewidth',2.0)

grid on

xl = xlabel('{\bf Time}');
yl = ylabel('{\bf Mass lost Rate}');
tl = title('{\bf Device 1}');

% set(xl,'interpreter','latex','fontsize',14)
% set(yl,'interpreter','latex','fontsize',14)
% set(tl,'interpreter','latex','fontsize',16)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%figure()
hold on
plot(Region1devc(:,1), Region1devc(:,2),'linewidth',2.0)

grid on

xl = xlabel('{\bf Time}');
yl = ylabel('{\bf Velovity}');
%tl = title('{\bf Device 1 on Region 1}');
leg = legend('Whole Region', 'Region1');

set(xl,'interpreter','latex','fontsize',14)
set(yl,'interpreter','latex','fontsize',14)
set(tl,'interpreter','latex','fontsize',16)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


