# -*- coding: utf-8 -*-
import numpy as np
import cv2 as cv
import json
import datetime

def nothing(x):
    pass

class Detector1(object):
    def __init__(self,DEBUG):
        self.blob_radius_thresh = 10
        self.DEBUG=DEBUG
        if self.DEBUG:
            cv.namedWindow("1gray", cv.WINDOW_NORMAL)
            cv.namedWindow("2binary", cv.WINDOW_NORMAL)
            cv.namedWindow("3addition", cv.WINDOW_NORMAL)
            cv.namedWindow("4gaussian", cv.WINDOW_NORMAL)
            cv.namedWindow("5dilate", cv.WINDOW_NORMAL)
            cv.namedWindow("6final", cv.WINDOW_NORMAL)
            cv.namedWindow("7dilate2", cv.WINDOW_NORMAL)
            cv.createTrackbar("binary1","2binary",65,255,nothing)
            cv.createTrackbar("dilate iteration","5dilate",15,20,nothing)
            cv.createTrackbar("binary final","6final",150,254,nothing)
            cv.createTrackbar("dilate iteration 2","7dilate2",8,20,nothing)
        print('Press ESC to exit cleanly')
      

    def Detect(self, currentframe, previousframe):
        current=np.copy(currentframe)
        previous=np.copy(previousframe)
        previous_gray = cv.cvtColor(previous, cv.COLOR_BGR2GRAY)
        if self.DEBUG :
            previous_binary = cv.threshold(previous_gray,cv.getTrackbarPos("binary1", "2binary"),255,cv.THRESH_BINARY_INV)[1]
            gray = cv.cvtColor(current, cv.COLOR_BGR2GRAY) 
            binary = cv.threshold(gray,cv.getTrackbarPos("binary1", "2binary"),255,cv.THRESH_BINARY)[1]
            addition=cv.threshold(binary+previous_binary,127,255,cv.THRESH_BINARY_INV)[1]    
            gaussian = cv.GaussianBlur(addition, (21,21), 0)
            dilate = cv.dilate(gaussian, None, iterations=cv.getTrackbarPos("dilate iteration", "5dilate"))
            final=cv.threshold(dilate,cv.getTrackbarPos("binary final", "6final"),255,cv.THRESH_BINARY)[1]
            dilate2 = cv.dilate(final, None, iterations=cv.getTrackbarPos("dilate iteration 2", "7dilate2"))
        else :
            previous_binary = cv.threshold(previous_gray,65,255,cv.THRESH_BINARY_INV)[1]
            gray = cv.cvtColor(current, cv.COLOR_BGR2GRAY) 
            binary = cv.threshold(gray,65,255,cv.THRESH_BINARY)[1]
            addition=cv.threshold(binary+previous_binary,127,255,cv.THRESH_BINARY_INV)[1]    
            gaussian = cv.GaussianBlur(addition, (21,21), 0)
            dilate = cv.dilate(gaussian, None, iterations=15)
            final=cv.threshold(dilate,150,255,cv.THRESH_BINARY)[1]
            dilate2 = cv.dilate(final, None, iterations=8)
        
        img_contour, contours_new, hierarchy = cv.findContours(dilate2,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        frame_contours=current
        cv.drawContours(frame_contours, contours_new, -1, (0,0,255), 2)
    
#    contours_final=[]
        centers = []
        rect = []

        for i in range(len(contours_new)):
#        if cv.contourArea(contours_new[i])>10.0:
#         #   if contours_new[i] in contours_old == True:
#            contours_final.append(contours_new[i])
            x,y,w,h = cv.boundingRect(contours_new[i])
            a=np.array([[x],[y],[w],[h]])
            rect.append(np.round(a))
            frame_contours = cv.rectangle(frame_contours,(x,y),(x+w,y+h),(255,0,0),2)
            b = np.array([[x+h/2], [y+w/2]])
            centers.append(np.round(b))
#    contours_old=contours_new
        
        if self.DEBUG: 
            cv.imshow("1gray", gray)
            cv.imshow("2binary", binary)
            cv.imshow("3addition", addition)
            cv.imshow("4gaussian", gaussian)
            cv.imshow("5dilate", dilate)
            cv.imshow("6final", final)
            cv.imshow("7dilate2", dilate2)
        return (centers,frame_contours,rect)   
    
    def SaveParam(self,videopath,filename):
        param = json.dumps([videopath,str(datetime.datetime.now()),cv.getTrackbarPos("binary1", "2binary"),
                            cv.getTrackbarPos("dilate iteration", "5dilate"),
                            cv.getTrackbarPos("binary final", "6final"),
                            cv.getTrackbarPos("dilate iteration 2", "7dilate2")])
        f = open(filename,'a+')
        f.write(param+"\n")
        f.close
        return
    
class Detector2(object):
    def __init__(self):
        self.kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(20,20)) #structure ellipse de 3 par 3
        self.fgbg = cv.createBackgroundSubtractorMOG2()
        self.blob_radius_thresh = 10

    def Detect(self, current):
        #cropped=frame[(frame.shape[0]-1000):frame.shape[0],0:frame.shape[1]] 
        fgmask = self.fgbg.apply(current)
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, self.kernel)
        img_contour, contours, hierarchy = cv.findContours(fgmask,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)    
        frame_contours=current
        cv.drawContours(frame_contours, contours, -1, (0,0,255), 2)
        

        centers = []  # vector of object centroids in a frame
        # Find centroid for each valid contours
        for cnt in contours:
            try:
                # Calculate and draw circle
                (x, y), radius = cv.minEnclosingCircle(cnt)
                centeroid = (int(x), int(y))
                radius = int(radius)
                if (radius > self.blob_radius_thresh):
                    cv.circle(frame_contours, centeroid, radius, (0, 255, 0), 2)
                    b = np.array([[x], [y]])
                    centers.append(np.round(b))
            except ZeroDivisionError:
                pass
        print (centers)

        return (centers,frame_contours)
    
    
    
    
    
        

            
            

        
