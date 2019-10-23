# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 15:06:30 2019

@author: JS235785
"""

#https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/
#https://github.com/srianant/kalman_filter_multi_object_tracking
#https://github.com/anandsinghkunwar/pedestrian-counter

import cv2 as cv
from detectors import Detector1,Detector2
from Api import Bee,Hive
from tracker import Tracker
import numpy as np

if __name__ == "__main__":

    MyHive=Hive()
    #videopath="video/GOPR3332.MP4"
    #videoname="GOPR3332"
    videopath="video/2018-06-27-151434.webm"
    videoname="2018-06-27-151434"
    
    beesimgpath='BeesImages/'+videoname+'/'
    paramsavepath='video/'+videoname+'.txt'
    cap = cv.VideoCapture(videopath)
    #variable de mise en pause sur touche "p"
    playVideo = True
    #Choix du type de detecteur
    num_detector =1
    #mode debug pour le détecteur 1, multi fenetre et reglage des paramètres
    DEBUG=1
    # Création de la fenetre de detection et prise 1ere image
    cv.namedWindow("detection", cv.WINDOW_NORMAL)
    ok, frame = cap.read()
    if not ok:
        print('Failed to read video')
        exit()
    # Select ROI
    r = cv.selectROI("detection",frame)
    # Crop image
    cropped = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

    # Create Object detector
    if num_detector==1:
        previous_frame=cropped
        detector = Detector1(DEBUG)
    else :
        detector = Detector2()
        
    # Create Object Tracker
    #(dist_thresh, max_frames_to_skip, max_trace_length,trackIdCount)
    #T tracker = Tracker(200, 1, 50, 1)
    #T cv.namedWindow("tracking", cv.WINDOW_NORMAL)
    
     # Variables initialization
    #T skip_frame_count = 0
#    #T track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
#                    (0, 255, 255), (255, 0, 255), (255, 127, 255),
#                    (127, 0, 255), (127, 0, 127)]
    

    while(True):
       
        if playVideo:
            # Capture frame-by-frame
            ok,frame = cap.read()
            if not ok:
                print('Failed to read video')
                break
            cropped=np.copy(frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])] )
            # Detect and return centeroids of the objects in the frame
            if num_detector==1:
                centers,frame2,rect = detector.Detect(cropped,previous_frame)
                #cv.imshow("bee", cropped)
                previous_frame=cropped    
                for i in range(len(centers)):
                    newbee=Bee(cropped[int(rect[i][1]):int(rect[i][1]+rect[i][3]),int(rect[i][0]):int(rect[i][0]+rect[i][2])],centers[i])
                    MyHive.AddBee(newbee)
            if num_detector==2:
                centers,frame2 = detector.Detect(cropped)
            
            cv.imshow("detection",frame2)
            #cv.destroyWindow("detection")
            
            # If centroids are detected then track them
#T            if (len(centers) > 0):
#    
#                # Track object using Kalman Filtser
#                tracker.Update(centers)
#                print (len(tracker.tracks))
#                # For identified object tracks draw tracking line
#                # Use various colors to indicate different track_id
#                for i in range(len(tracker.tracks)):               
#                    if (len(tracker.tracks[i].trace) > 1):
#                        for j in range(len(tracker.tracks[i].trace)-1):
#                            # Draw trace line
#                            x1 = tracker.tracks[i].trace[j][0][0]
#                            y1 = tracker.tracks[i].trace[j][1][0]
#                            x2 = tracker.tracks[i].trace[j+1][0][0]
#                            y2 = tracker.tracks[i].trace[j+1][1][0]
#                            clr = tracker.tracks[i].track_id % 9
#                            cv.line(frame, (int(x1), int(y1)), (int(x2), int(y2)),
#                                     track_colors[clr], 2)
#                            #cv.imwrite(str(i)+'-'+str(j)+'.jpg',frame[int(y1-100):int(y1+100), int(x1-100):int(x1+100)])
#    
#                # Display the resulting tracking frame
#                cv.imshow('tracking', frame)
#            else:
# T               cv.imshow('tracking', frame)
                    
             
        k = cv.waitKey(50);
        if k == 27: #ascii ESC
            print (len(MyHive.bees))
            MyHive.Save(beesimgpath)
            break
        if k == 112: #ascii p
            playVideo = not playVideo
        if k == 115: #ascii s
            detector.SaveParam(videopath,paramsavepath)
            print('param well saved')
        
    print (len(MyHive.bees))
    MyHive.Save(beesimgpath)
    cap.release()
    cv.destroyAllWindows()
    
    
    
    
    
    
    
