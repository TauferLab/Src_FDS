function  plotting_cube(X0,Xn,cl)

x0 = X0(1);
y0 = X0(2);
z0 = X0(3);

xn = Xn(1);
yn = Xn(2);
zn = Xn(3);

% Floor
X = [x0 xn xn x0 x0 ]; Y = [y0 y0 yn yn y0]; Z = [z0 z0 z0 z0 z0];

fill3(X, Y, Z,cl)
alpha(0.5);
xlabel('x','FontSize',12,'FontWeight','bold','Color','r')
ylabel('y','FontSize',12,'FontWeight','bold','Color','r')
zlabel('z','FontSize',12,'FontWeight','bold','Color','r')

hold on

% Ceiling
X = [x0 xn xn x0 x0 ]; Y = [y0 y0 yn yn y0]; Z = [zn zn zn zn zn];

fill3(X, Y, Z,cl)
alpha(0.5);
xlabel('x','FontSize',12,'FontWeight','bold','Color','r')
ylabel('y','FontSize',12,'FontWeight','bold','Color','r')
zlabel('z','FontSize',12,'FontWeight','bold','Color','r')

% left wall
X = [x0 x0 x0 x0 x0 ]; Y = [y0 yn yn y0 y0]; Z = [z0 z0 zn zn z0];

fill3(X, Y, Z,cl)
alpha(0.5);
xlabel('x','FontSize',12,'FontWeight','bold','Color','r')
ylabel('y','FontSize',12,'FontWeight','bold','Color','r')
zlabel('z','FontSize',12,'FontWeight','bold','Color','r')

% right wall
X = [xn xn xn xn xn ]; Y = [y0 yn yn y0 y0]; Z = [z0 z0 zn zn z0];

fill3(X, Y, Z,cl)
alpha(0.5);
xlabel('x','FontSize',12,'FontWeight','bold','Color','r')
ylabel('y','FontSize',12,'FontWeight','bold','Color','r')
zlabel('z','FontSize',12,'FontWeight','bold','Color','r')

% back wall
X = [x0 xn xn x0 x0 ]; Y = [yn yn yn yn yn]; Z = [z0 z0 zn zn z0];

fill3(X, Y, Z,cl)
alpha(0.5);
xlabel('x','FontSize',12,'FontWeight','bold','Color','r')
ylabel('y','FontSize',12,'FontWeight','bold','Color','r')
zlabel('z','FontSize',12,'FontWeight','bold','Color','r')


% front wall
X = [x0 xn xn x0 x0 ]; Y = [y0 y0 y0 y0 y0]; Z = [z0 z0 zn zn z0];

fill3(X, Y, Z,cl)
alpha(0.5);
xlabel('x','FontSize',12,'FontWeight','bold','Color','r')
ylabel('y','FontSize',12,'FontWeight','bold','Color','r')
zlabel('z','FontSize',12,'FontWeight','bold','Color','r')


view([-224.5520,12.6000])
