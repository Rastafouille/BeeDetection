# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv

cv.namedWindow("tracking")
camera = cv.VideoCapture("2018-06-27-151049.webm")

while camera.isOpened():
    ok, image=camera.read()
    if not ok:
        print('Failed to read video')
        exit()

    cropped=image[(image.shape[0]-200):image.shape[0],0:image.shape[1]] 
    resized=cv.resize(cropped,((cropped.shape[1]/2),(cropped.shape[0]/2)),interpolation = cv.INTER_AREA)
    gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)  
    ret,binary = cv.threshold(gray,127,255,cv.THRESH_BINARY)
    cv.imshow("tracking", resized)
    cv.imshow("tracking2", gray)
    cv.imshow("tracking3", binary)    
    k = cv.waitKey(100)
    
    
#    lower_color = np.array([30,150,50])
#    upper_color = np.array([255,255,180])
#    
#    mask = cv2.inRange(hsv, lower_red, upper_red)
#    res = cv2.bitwise_and(frame,frame, mask= mask)
#
#    cv2.imshow('frame',frame)
#    cv2.imshow('mask',mask)
#    cv2.imshow('res',res)