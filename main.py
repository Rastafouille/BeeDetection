
import numpy as np
import cv2
from detectors import Detector1 Detector2
from tracker import Tracker


###### pas fonctionnel ######

if __name__ == "__main__":

    cap = cv2.VideoCapture("2018-06-27-151434.webm")
    detector =1
    
    if detector==1:
    	detector = Detector1()
    	previous_frame=cap.read()[1] 
    	previous_cropped=previous_frame[(previous_frame.shape[0]-1000):previous_frame.shape[0],0:previous_frame.shape[1]] 
    else :
    	detector = Detector2()
  
    
    while(True):
            # Capture frame-by-frame
            frame = cap.read()[1]
            cropped=frame[(frame.shape[0]-1000):frame.shape[0],0:frame.shape[1]] 
            # Detect and return centeroids of the objects in the frame
            if detector==1:
            	centers = detector.Detect(cropped)
            else :
            	centers = detector.Detect(cropped,previous_cropped)
            
            resized=cv2.resize(cropped,(int((cropped.shape[1]/2)),int((cropped.shape[0]/2))),interpolation = cv2.INTER_AREA)
            
            previous_cropped=cropped  #pour detector2          
            cv2.imshow('resized',resized)
            k = cv2.waitKey(500) & 0xff
    cap.release()
    cv2.destroyAllWindows()
    
    
    
    
    
    
    
