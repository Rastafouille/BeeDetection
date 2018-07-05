# -*- coding: utf-8 -*-

#https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/
#https://github.com/srianant/kalman_filter_multi_object_tracking

#https://github.com/anandsinghkunwar/pedestrian-counter


import numpy as np
import cv2 as cv
DEBUG=0

def nothing(x):
    pass

camera = cv.VideoCapture("2018-06-27-151434.webm")

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
if DEBUG:
	cv.createTrackbar("binary1","detection",65,255,nothing)
	cv.createTrackbar("dilate iteration","detection",15,20,nothing)
	cv.createTrackbar("binary final","detection",150,254,nothing)
	cv.createTrackbar("dilate iteration 2","detection",8,20,nothing)
cv.imshow("detection", cropped)

gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)

if DEBUG: 
	binary = cv.threshold(gray,cv.getTrackbarPos("binary1", "detection"),255,cv.THRESH_BINARY_INV)[1]
else:
	binary = cv.threshold(gray,50,255,cv.THRESH_BINARY_INV)[1]

previousbinaryFrame = binary

k = cv.waitKey(10)

if DEBUG:
	cv.namedWindow("1gray", cv.WINDOW_NORMAL)
	cv.namedWindow("2binary", cv.WINDOW_NORMAL)
	cv.namedWindow("3addition", cv.WINDOW_NORMAL)
	cv.namedWindow("4gaussian", cv.WINDOW_NORMAL)
	cv.namedWindow("5dilate", cv.WINDOW_NORMAL)
	cv.namedWindow("6final", cv.WINDOW_NORMAL)
	cv.namedWindow("7dilate2", cv.WINDOW_NORMAL)

print('Press ESC to exit cleanly')
while camera.isOpened():
	ok, image=camera.read()
	cropped = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
	blank_image = np.zeros((cropped.shape[0],cropped.shape[1],3), np.uint8)

	if not ok:
		print('Failed to read video')
		exit()
		
	if DEBUG :
	    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY) 
	    binary = cv.threshold(gray,cv.getTrackbarPos("binary1", "detection"),255,cv.THRESH_BINARY)[1]
	    addition=cv.threshold(binary+previousbinaryFrame,127,255,cv.THRESH_BINARY_INV)[1]    
	    previousbinaryFrame = cv.threshold(binary,127,255,cv.THRESH_BINARY_INV)[1]
	    gaussian = cv.GaussianBlur(addition, (21,21), 0)
	    dilate = cv.dilate(gaussian, None, iterations=cv.getTrackbarPos("dilate iteration", "detection"))
	    final=cv.threshold(dilate,cv.getTrackbarPos("binary final", "detection"),255,cv.THRESH_BINARY)[1]
	    dilate2 = cv.dilate(final, None, iterations=cv.getTrackbarPos("dilate iteration 2", "detection"))
	else :
	    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY) 
	    binary = cv.threshold(gray,65,255,cv.THRESH_BINARY)[1]
	    addition=cv.threshold(binary+previousbinaryFrame,127,255,cv.THRESH_BINARY_INV)[1]    
	    previousbinaryFrame = cv.threshold(binary,127,255,cv.THRESH_BINARY_INV)[1]
	    gaussian = cv.GaussianBlur(addition, (21,21), 0)
	    dilate = cv.dilate(gaussian, None, iterations=15)
	    final=cv.threshold(dilate,150,255,cv.THRESH_BINARY)[1]
	    dilate2 = cv.dilate(final, None, iterations=8)
	
	img_contour, contours_new, hierarchy = cv.findContours(dilate2,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
	cv.drawContours(cropped, contours_new, -1, (0,0,255), 2)
    
#    contours_final=[]
	for i in range(len(contours_new)):
#        if cv.contourArea(contours_new[i])>10.0:
#         #   if contours_new[i] in contours_old == True:
#            contours_final.append(contours_new[i])
		x,y,w,h = cv.boundingRect(contours_new[i])
		cropped = cv.rectangle(cropped,(x,y),(x+w,y+h),(255,0,0),2)
#    contours_old=contours_new
        
#    horizontal_concat1 = np.concatenate((gray2, binary,addition), axis=1)
#    horizontal_concat2 = np.concatenate((gaussian,dilate,), axis=1)
#    horizontal_concat3 = np.concatenate((dilate, final), axis=1)
#    horizontal_concat4 = np.concatenate((dilate2, gray2), axis=1)
#    vertical_concat = np.concatenate((horizontal_concat1, horizontal_concat2,horizontal_concat3,horizontal_concat4), axis=0)

	cv.imshow("detection", cropped)
	
	if DEBUG: 
		cv.imshow("1gray", gray)
		cv.imshow("2binary", binary)
		cv.imshow("3addition", addition)
		cv.imshow("4gaussian", gaussian)
		cv.imshow("5dilate", dilate)
		cv.imshow("6final", final)
		cv.imshow("7dilate2", dilate2)

#Exit if ESC pressed.
	k = cv.waitKey(100);
	if k == 27:
		break;
cv.destroyAllWindows()
    
    
    
    
    
