video =VideoWriter('fire_1_[450,550]x[450,550].avi','Motion JPEG AVI');
video.FrameRate = 4;
   
    
open(video); %open the file for writing
    
    for i=0:120
        numero = sprintf('%0.4d',i);
        name1 = ['Chimney_tops_1m_',numero,'.png'];
        
        I1 = imread(name1); %read the next image
      
        imshow(I1)
        t1 = title({'Predictor-Corrector = False'; 'Ramp 31 = 0'});
        set(t1,'interpreter','latex')
        
        frame = getframe(gcf);
        
        writeVideo(video,frame); %write the image to file(name,'-dpng')
    end
close(video); %close the file