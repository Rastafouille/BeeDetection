#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import cv2

cap = cv2.VideoCapture("2018-06-27-151434.webm")

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)) #structure ellipse de 3 par 3
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG() 

while(1):
    ret, frame = cap.read()
    cropped=frame[(frame.shape[0]-1000):frame.shape[0],0:frame.shape[1]] 
    fgmask = fgbg.apply(cropped)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    
    img_contour, contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    
    cv2.drawContours(cropped, contours, -1, (0,0,255), 2)
    
    centers = []  # vector of object centroids in a frame
    # we only care about centroids with size of bees in this example
    # recommended to be tunned based on expected object size for
    # improved performance
    blob_radius_thresh = 10
    # Find centroid for each valid contours
    for cnt in contours:
        try:
            # Calculate and draw circle
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            centeroid = (int(x), int(y))
            radius = int(radius)
            if (radius > blob_radius_thresh):
                cv2.circle(cropped, centeroid, radius, (0, 255, 0), 2)
                b = np.array([[x], [y]])
                centers.append(np.round(b))
        except ZeroDivisionError:
            pass
    
    resized=cv2.resize(cropped,(int((cropped.shape[1]/2)),int((cropped.shape[0]/2))),interpolation = cv2.INTER_AREA)

    cv2.imshow('resized',resized)
    cv2.imshow('fgmask',fgmask)

    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()