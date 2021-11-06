close all
load Q_Whole.mat
load Q_Region1.mat
load Q_Region2.mat
load Q_Region3.mat
Domain = [200 700;200 740;380 620];
Domain_Region1 = [400 700;200 500;380 620];
Domain_Region2 = [350 650;350 650;380 620];
Domain_Region3 = [280 580;440 740;380 620];

start_w  = 1;
finish_w = start_w + lengt_t(1);
plot3(Q_whole(start_w:finish_w,1),Q_whole(start_w:finish_w,2),Q_whole(start_w:finish_w,3),'.r')
hold on
start_1  = 1;
finish_1 = start_1 + lengt_t_region1(1);
plot3(Q_region1(start_1:finish_1,1),Q_region1(start_1:finish_1,2),Q_region1(start_1:finish_1,3),'.b')
for i =2:240
    cla
    draw_cube(Domain_Region1,[0,0,1])
    start_w  = finish_w+1;
    finish_w = start_w + lengt_t(i);
    
    plot3(Q_whole(start_w:finish_w,1),Q_whole(start_w:finish_w,2),Q_whole(start_w:finish_w,3),'.r')
    
    
    start_1  = finish_1+1;
    finish_1 = start_1 + lengt_t_region1(i);
    plot3(Q_region1(start_1:finish_1,1),Q_region1(start_1:finish_1,2),Q_region1(start_1:finish_1,3),'.b')   
    grid on
    axis([Domain(1,:) Domain(2,:) Domain(3,:)])
    pause(0.125)
    
    
end
    
    finish_2 = 0;
for i =241:360
    cla
    draw_cube(Domain_Region1,[0,0,1])
    draw_cube(Domain_Region2,[0,1,0])
    start_w  = finish_w+1;
    finish_w = start_w + lengt_t(i);
    plot3(Q_whole(start_w:finish_w,1),Q_whole(start_w:finish_w,2),Q_whole(start_w:finish_w,3),'.r')
    
    start_2  = finish_2+1;
    finish_2 = start_2 + lengt_t_region2(i-240+1); 
    
    plot3(Q_region2(start_2:finish_2,1),Q_region2(start_2:finish_2,2),Q_region2(start_2:finish_2,3),'.g')   
    grid on
    axis([Domain(1,:) Domain(2,:) Domain(3,:)])
    pause(0.125)
    
    
end

finish_3 = 0;
for i =361:480
    cla
    draw_cube(Domain_Region1,[0,0,1])
    draw_cube(Domain_Region2,[0,1,0])
    draw_cube(Domain_Region3,[1,0,1])
    start_w  = finish_w+1;
    finish_w = start_w + lengt_t(i);
    plot3(Q_whole(start_w:finish_w,1),Q_whole(start_w:finish_w,2),Q_whole(start_w:finish_w,3),'.r')
    
    start_3  = finish_3+1;
    finish_3 = start_3 + lengt_t_region3(i-360+1); 
    
    plot3(Q_region3(start_3:finish_3,1),Q_region3(start_3:finish_3,2),Q_region3(start_3:finish_3,3),'.m')   
    grid on
    axis([Domain(1,:) Domain(2,:) Domain(3,:)])
    pause(0.125)
    
    
end

function draw_cube(domain, colour)

plot3([domain(1,1) domain(1,2) domain(1,2) domain(1,1) domain(1,1)],[domain(2,1) domain(2,1) domain(2,2) domain(2,2) domain(2,1)], [domain(3,1) domain(3,1) domain(3,1) domain(3,1) domain(3,1)], 'linewidth' , 2.0, 'Color',colour)
plot3([domain(1,1) domain(1,2) domain(1,2) domain(1,1) domain(1,1)],[domain(2,1) domain(2,1) domain(2,2) domain(2,2) domain(2,1)], [domain(3,2) domain(3,2) domain(3,2) domain(3,2) domain(3,2)], 'linewidth' , 2.0, 'Color',colour)

plot3([domain(1,1) domain(1,1) domain(1,1) domain(1,1) domain(1,1)],[domain(2,1) domain(2,2) domain(2,2) domain(2,1) domain(2,1)], [domain(3,1) domain(3,1) domain(3,2) domain(3,2) domain(3,1)], 'linewidth' , 2.0, 'Color',colour)
plot3([domain(1,2) domain(1,2) domain(1,2) domain(1,2) domain(1,2)],[domain(2,1) domain(2,2) domain(2,2) domain(2,1) domain(2,1)], [domain(3,1) domain(3,1) domain(3,2) domain(3,2) domain(3,1)], 'linewidth' , 2.0, 'Color',colour)
end