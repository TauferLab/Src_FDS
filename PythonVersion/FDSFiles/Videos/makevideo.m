video =VideoWriter('fire_1_[450,550]x[450,550].avi','Motion JPEG AVI');
video.FrameRate = 2;
   
    
open(video); %open the file for writing
    
    for i=0:20
        numero = sprintf('%0.4d',i);
        name1 = ['../FDSPROG_1_[450,550]x[450,550]_PC_0_Rampa31_0/Chimney_tops_1m_',numero,'.png'];
        name2 = ['../FDSPROG_1_[450,550]x[450,550]_PC_0_Rampa31_1/Chimney_tops_1m_',numero,'.png'];
        name3 = ['../FDSPROG_1_[450,550]x[450,550]_PC_1_Rampa31_0/Chimney_tops_1m_',numero,'.png'];
        name4 = ['../FDSPROG_1_[450,550]x[450,550]_PC_1_Rampa31_1/Chimney_tops_1m_',numero,'.png'];
        
        I1 = imread(name1); %read the next image
        I2 = imread(name2); %read the next image
        I3 = imread(name3); %read the next image
        I4 = imread(name4); %read the next image
        
        subplot(2,2,1)
        imshow(I1)
        t1 = title({'Predictor-Corrector = False'; 'Ramp 31 = 0'});
        set(t1,'interpreter','latex')
        
        subplot(2,2,2)
        imshow(I2)
        t2=title({'Predictor-Corrector = False'; 'Ramp 31 = 1'});
        set(t2,'interpreter','latex')
        
        subplot(2,2,3)
        imshow(I3)
        t3=title({'Predictor-Corrector = True'; 'Ramp 31 = 0'});
        set(t3,'interpreter','latex')
        
        subplot(2,2,4)
        imshow(I4)
        t4=title({'Predictor-Corrector = True'; 'Ramp 31 = 1'});
        set(t4,'interpreter','latex')
        
        
        frame = getframe(gcf);
        
        writeVideo(video,frame); %write the image to file(name,'-dpng')
    end
close(video); %close the file