# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 18:14:10 2021

@author: rastafouille
"""

#https://medium.com/dropout-analytics/opencv-cuda-for-videos-f3dcf346e398
#https://learnopencv.com/getting-started-opencv-cuda-module/

#https://haroonshakeel.medium.com/build-opencv-4-4-0-with-cuda-gpu-support-on-windows-10-without-tears-aa85d470bcd0

#1 https://opencv.org/releases/
#2 https://github.com/opencv/opencv_contrib/tree/master


import cv2 as cv
from detectors import Detector1,Detector2
from api import Bee,Hive
from tracker import Tracker
import numpy as np
import time

if __name__ == "__main__":


    #videopath="video/GOPR3332.MP4"
    #videoname="GOPR3332"
    videopath="../BeeDetectionData/video/VID_20191026_154626.mp4"
    videoname="VID_20191026_154626"
    
    beesimgpath='../BeeDetectionData/BeesImages/'+videoname+'/'
    paramsavepath='video/'+videoname+'.txt'
    
        
    cap = cv.VideoCapture(videopath)
    cap.set(cv.CAP_PROP_FPS, 30)
    #cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
    #cap.set(cv.CAP_PROP_FRAME_HEIGHT, 700)
    #variable de mise en pause sur touche "p"
    fps = cap.get(cv.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    
    print('fps = ' + str(np.round(fps,1)))
    print('number of frames = ' + str(frame_count))
    print('duration (S) = ' + str(np.round(duration,1))+' sec')
    
    font = cv.FONT_HERSHEY_COMPLEX_SMALL
    
    playVideo = True
    #Choix du type de detecteur
    
    cv.namedWindow("detection", cv.WINDOW_NORMAL)
    ok, frame = cap.read()
    #gpu_frame = cv.cuda_GpuMat()
    #gpu_frame.upload(frame)

    
    if not ok:
        print('Failed to read video')
        exit()
   
    
    start_time=time.time()
    start_time0=time.time()
    frame_number=0
    while(True):
       
        if playVideo:
            # Capture frame-by-frame
            ok,frame = cap.read()
            #gpu_frame = cv.cuda_GpuMat()
            #gpu_frame.upload(frame)
            frame_number+=1
           
            if not ok:
                print('Failed to read video')
                break
            
            # Display the resulting tracking frame
            cv.putText(frame, 'FPS:'+str(np.round(1/(time.time()-start_time),1)), (2,36), font, 0.8, (0, 255, 0), 1, 8)
            start_time=time.time()
            cv.putText(frame, str(np.round(frame_number/fps,1))+'/'+str(np.round(duration,1))+' sec', (2,24), font, 0.8, (0, 255, 0), 1, 8)
                  
            cv.imshow("detection",frame)
            
                                                                

        
        k = cv.waitKey(1);
        if k == 27: #ascii ESC
            break
        if k == 112: #ascii p
            playVideo = not playVideo
        if k == 115: #ascii s
            print('param well saved')
        
    print('fps global = ' + str( np.round(frame_count/(time.time()-start_time0),1) ) )  


    cap.release()
    cv.destroyAllWindows()
    
    
    