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
cv.namedWindow("detection", cv.WINDOW_NORMAL)
cv.createTrackbar("binary1","detection",50,255,nothing)
cv.createTrackbar("gaussian","detection",21,100,nothing)
cv.createTrackbar("dilate iteration","detection",4,20,nothing)
cv.createTrackbar("binary final","detection",150,254,nothing)
cv.createTrackbar("dilate iteration 2","detection",4,20,nothing)

cv.imshow("detection", cropped)
#cropped=image[(image.shape[0]-1000):image.shape[0],0:image.shape[1]] 
#resized=cv.resize(cropped,(int((cropped.shape[1]/2)),int((cropped.shape[0]/2))),interpolation = cv.INTER_AREA)
#blank_image = np.zeros((cropped.shape[0],cropped.shape[1],3), np.uint8)
gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY) 
#gray = cv.GaussianBlur(gray, (21, 21), 0)
ret,binary = cv.threshold(gray,cv.getTrackbarPos("binary1", "detection"),255,cv.THRESH_BINARY_INV)
previousbinaryFrame = binary
#binary=cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY_INV,20,2)

#img_contour, contours_new, hierarchy = cv.findContours(binary,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)    
#cv.drawContours(cropped, contours_new, -1, (0,0,255), 2)

# suppression des petite surface
#contours_final=[]
#for i in range(0,len(contours_new)-1):
##    if cv.contourArea(contours_new[i])>10.0:
##        contours_final.append(contours_new[i])
#    x,y,w,h = cv.boundingRect(contours_new[i])
#    cropped = cv.rectangle(cropped,(x,y),(x+w,y+h),(255,0,0),2)
#    #print i,cv.contourArea(contours[i])
#    
#    
#cv.drawContours(cropped, contours_new, -1, (0,255,0), 2)   
k = cv.waitKey(200)

#contours_old=contours_new
cv.namedWindow("1gray", cv.WINDOW_NORMAL)
cv.namedWindow("2binary", cv.WINDOW_NORMAL)
cv.namedWindow("3addition", cv.WINDOW_NORMAL)
cv.namedWindow("4gaussian", cv.WINDOW_NORMAL)
cv.namedWindow("5dilate", cv.WINDOW_NORMAL)
cv.namedWindow("6final", cv.WINDOW_NORMAL)
cv.namedWindow("7dilate2", cv.WINDOW_NORMAL)




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
    
    binary = cv.threshold(gray,cv.getTrackbarPos("binary1", "detection"),255,cv.THRESH_BINARY)[1]
    addition=cv.threshold(binary+previousbinaryFrame,127,255,cv.THRESH_BINARY_INV)[1]    
    previousbinaryFrame = cv.threshold(binary,127,255,cv.THRESH_BINARY_INV)[1]
    gaussian = cv.GaussianBlur(addition, (cv.getTrackbarPos("gaussian", "detection"), cv.getTrackbarPos("gaussian", "detection")), 0)
    dilate = cv.dilate(gaussian, None, iterations=cv.getTrackbarPos("dilate iteration", "detection"))
    final=cv.threshold(dilate,cv.getTrackbarPos("binary final", "detection"),255,cv.THRESH_BINARY)[1]
    dilate2 = cv.dilate(final, None, iterations=cv.getTrackbarPos("dilate iteration 2", "detection"))
    
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
        

    
#    horizontal_concat1 = np.concatenate((gray2, binary,addition), axis=1)
#    horizontal_concat2 = np.concatenate((gaussian,dilate,), axis=1)
#    horizontal_concat3 = np.concatenate((dilate, final), axis=1)
#    horizontal_concat4 = np.concatenate((dilate2, gray2), axis=1)
#
#
#
#    vertical_concat = np.concatenate((horizontal_concat1, horizontal_concat2,horizontal_concat3,horizontal_concat4), axis=0)
#
#    
    cv.imshow("detection", cropped)
    cv.imshow("1gray", gray)
    cv.imshow("2binary", binary)
    cv.imshow("3addition", addition)
    cv.imshow("4gaussian", gaussian)
    cv.imshow("5dilate", dilate)
    cv.imshow("6final", final)
    cv.imshow("7dilate2", dilate2)
    #cv.imshow("dilate", dilate)
    #cv.imshow("blank", blank_image)    
    k = cv.waitKey(100000)
cv.destroyAllWindows()
    
    
    
    
    
