video =VideoWriter('fire.avi','Motion JPEG AVI');
video.FrameRate = 2;
   
    
open(video); %open the file for writing
    
    for i=0:120
        numero = sprintf('%0.4d',i);
        name = ['Chimney_tops_1m_',numero,'.png']
        I = imread(name); %read the next image
        writeVideo(video,I); %write the image to file(name,'-dpng')
    end
close(video); %close the file