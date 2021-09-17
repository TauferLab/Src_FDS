video = VideoWriter('velocity');
video.FrameRate = 4;
   
    
open(video); %open the file for writing
    
    for i=2:313
        name = ['../../../data/Devices_Outputs/Region2/VELOCITY/VELOCITY',num2str(i,'%04d'),'.png'];        
        I1 = imread(name); %read the next image
        imshow(I1)
        frame = getframe(gcf);
        
        writeVideo(video,frame); %write the image to file(name,'-dpng')
    end
close(video); %close the file