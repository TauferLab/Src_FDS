video = VideoWriter('regions');
video.FrameRate = 4;
   
    
open(video); %open the file for writing

% Images of Region1

    for i=0:120
        name = ['../../../simulations/chimney/Region1/Region1_',num2str(i,'%04d'),'.png'];        
        I1 = imread(name); %read the next image
        imshow(I1)
        frame = getframe(gcf);
        
        writeVideo(video,frame); %write the image to file(name,'-dpng')
    end
    
    % Images of Region2
    
    for i=0:80
        name = ['../../../simulations/chimney/Region2/Region2_cat_',num2str(i,'%04d'),'.png'];        
        I1 = imread(name); %read the next image
        imshow(I1)
        frame = getframe(gcf);
        
        writeVideo(video,frame); %write the image to file(name,'-dpng')
    end
    
    % Images of Region3
    
     for i=0:60
        name = ['../../../simulations/chimney/Region3/Region3_cat_',num2str(i,'%04d'),'.png'];        
        I1 = imread(name); %read the next image
        imshow(I1)
        frame = getframe(gcf);
        
        writeVideo(video,frame); %write the image to file(name,'-dpng')
     end
    
     % Images of Region4
    
     for i=0:60
        name = ['../../../simulations/chimney/Region4/Region4_cat_',num2str(i,'%04d'),'.png'];        
        I1 = imread(name); %read the next image
        imshow(I1)
        frame = getframe(gcf);
        
        writeVideo(video,frame); %write the image to file(name,'-dpng')
     end
    
    % Images of Region5
    
     for i=0:120
        name = ['../../../simulations/chimney/Region5/Region5_cat_',num2str(i,'%04d'),'.png'];        
        I1 = imread(name); %read the next image
        imshow(I1)
        frame = getframe(gcf);
        
        writeVideo(video,frame); %write the image to file(name,'-dpng')
     end
    
     % Images of Region6
    
     for i=0:160
        name = ['../../../simulations/chimney/Region6/Region6_cat_',num2str(i,'%04d'),'.png'];        
        I1 = imread(name); %read the next image
        imshow(I1)
        frame = getframe(gcf);
        
        writeVideo(video,frame); %write the image to file(name,'-dpng')
    end
    
    
close(video); %close the file