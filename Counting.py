# -*- coding: utf-8 -*-

#https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/
#https://github.com/srianant/kalman_filter_multi_object_tracking

#https://github.com/anandsinghkunwar/pedestrian-counter


import numpy as np
import cv2 as cv

def nothing(x):
    pass

camera = cv.VideoCapture("2018-06-27-151434.webm")
#cv.namedWindow("1")        # Create a named window
#cv.moveWindow("1", 0,0)  # Move it to (40,30)
#cv.namedWindow("2")        # Create a named window
#cv.moveWindow("2", 0,250)  # Move it to (40,30)
#cv.namedWindow("3")        # Create a named window
#cv.moveWindow("3", 0,500)  # Move it to (40,30)

ok, image=camera.read()

if not ok:
    print('Failed to read video')
    exit()
cv.namedWindow("image", cv.WINDOW_NORMAL)




# Select ROI
r = cv.selectROI("image",image)
cv.destroyWindow("image")
 # Crop image
cropped = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
cv.namedWindow("1cropped", cv.WINDOW_NORMAL)
cv.createTrackbar("binary1","1cropped",127,254,nothing)
cv.imshow("1cropped", cropped)
#cropped=image[(image.shape[0]-1000):image.shape[0],0:image.shape[1]] 
#resized=cv.resize(cropped,(int((cropped.shape[1]/2)),int((cropped.shape[0]/2))),interpolation = cv.INTER_AREA)
blank_image = np.zeros((cropped.shape[0],cropped.shape[1],3), np.uint8)
gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY) 
#gray = cv.GaussianBlur(gray, (21, 21), 0)
ret,binary = cv.threshold(gray,120,255,cv.THRESH_BINARY_INV)
previousbinaryFrame = binary
#binary=cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY_INV,20,2)

img_contour, contours_new, hierarchy = cv.findContours(binary,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)    
cv.drawContours(cropped, contours_new, -1, (0,0,255), 2)

# suppression des petite surface
#contours_final=[]
for i in range(0,len(contours_new)-1):
#    if cv.contourArea(contours_new[i])>10.0:
#        contours_final.append(contours_new[i])
    x,y,w,h = cv.boundingRect(contours_new[i])
    cropped = cv.rectangle(cropped,(x,y),(x+w,y+h),(255,0,0),2)
    #print i,cv.contourArea(contours[i])
    
    
cv.drawContours(cropped, contours_new, -1, (0,255,0), 2)   
k = cv.waitKey(200)

contours_old=contours_new

while camera.isOpened():
    ok, image=camera.read()
    cropped = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    blank_image = np.zeros((cropped.shape[0],cropped.shape[1],3), np.uint8)
    if not ok:
        print('Failed to read video')
        exit()
    #cropped=image[(image.shape[0]-1000):image.shape[0],0:image.shape[1]] 
    #resized=cv.resize(cropped,(int((cropped.shape[1]/2)),int((cropped.shape[0]/2))),interpolation = cv.INTER_AREA)
    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY) 
    #gray = cv.GaussianBlur(gray, (21, 21), 0)
    #frameDelta = cv.subtract(firstFrame, gray)
    #firstFrame = gray
    
    binary = cv.threshold(gray,50,255,cv.THRESH_BINARY)[1]
    addition=cv.threshold(binary+previousbinaryFrame,127,255,cv.THRESH_BINARY_INV)[1]    
    previousbinaryFrame = cv.threshold(binary,127,255,cv.THRESH_BINARY_INV)[1]
    gaussian = cv.GaussianBlur(addition, (21, 21), 0)
    dilate = cv.dilate(gaussian, None, iterations=4)
    final=cv.threshold(dilate,60,255,cv.THRESH_BINARY)[1]
    dilate2 = cv.dilate(final, None, iterations=4)
    
    #erode=cv.dilate(addition, None, iterations=2)
    #dilate = cv.dilate(final, None, iterations=2)
    #binary=cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY_INV,20,2)
    
    img_contour, contours_new, hierarchy = cv.findContours(dilate2,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)    
    cv.drawContours(cropped, contours_new, -1, (0,0,255), 2)
    
#    contours_final=[]
    for i in range(len(contours_new)):
#        if cv.contourArea(contours_new[i])>10.0:
#         #   if contours_new[i] in contours_old == True:
#            contours_final.append(contours_new[i])
        x,y,w,h = cv.boundingRect(contours_new[i])
        cropped = cv.rectangle(cropped,(x,y),(x+w,y+h),(255,0,0),2)
#                #print i,cv.contourArea(contours[i])
#    contours_old=contours_new
        
    #cv.drawContours(blank_image, contours_final, -1, (0,255,0), 2)
    #cv.imshow("resized", resized)
    cv.imshow("1cropped", cropped)
    cv.imshow("2binary", binary)
    cv.imshow("3addition", addition)
    cv.imshow("4gaussian", gaussian)
    cv.imshow("5dilate", dilate)
    cv.imshow("6final", final)
    cv.imshow("7dilate2", dilate2)
    #cv.imshow("dilate", dilate)
    #cv.imshow("blank", blank_image)    
    k = cv.waitKey(100)
cv.destroyAllWindows()
    
    
    
    
    
