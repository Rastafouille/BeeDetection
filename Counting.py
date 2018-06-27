# -*- coding: utf-8 -*-

#https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/

import numpy as np
import cv2 as cv

cv.namedWindow("tracking")
camera = cv.VideoCapture("2018-06-27-151049.webm")
cv.namedWindow("tracking")        # Create a named window
cv.moveWindow("tracking", 0,0)  # Move it to (40,30)
cv.namedWindow("tracking2")        # Create a named window
cv.moveWindow("tracking2", 0,250)  # Move it to (40,30)
cv.namedWindow("tracking3")        # Create a named window
cv.moveWindow("tracking3", 0,300)  # Move it to (40,30)

while camera.isOpened():
    ok, image=camera.read()
    blank_image = np.zeros((400/2,image.shape[1]/2,3), np.uint8)
    if not ok:
        print('Failed to read video')
        exit()

    cropped=image[(image.shape[0]-400):image.shape[0],0:image.shape[1]] 
    resized=cv.resize(cropped,((cropped.shape[1]/2),(cropped.shape[0]/2)),interpolation = cv.INTER_AREA)
    gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)  
    ret,binary = cv.threshold(gray,127,255,cv.THRESH_BINARY)
    img_contour, contours, hierarchy = cv.findContours(binary,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)    
    cv.drawContours(blank_image, contours, -1, (0,0,255), 2)
  
    cv.imshow("tracking", resized)
    cv.imshow("tracking2", gray)
    cv.imshow("tracking3", blank_image)    
    k = cv.waitKey(200)
    
    
#    lower_color = np.array([30,150,50])
#    upper_color = np.array([255,255,180])
#    
#    mask = cv2.inRange(hsv, lower_red, upper_red)
#    res = cv2.bitwise_and(frame,frame, mask= mask)
#
#    cv2.imshow('frame',frame)
#    cv2.imshow('mask',mask)
#    cv2.imshow('res',res)