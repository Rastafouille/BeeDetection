'''
    File name         : detectors.py
    File Description  : Detect objects in video frame
    Author            : Srini Ananthakrishnan
    Date created      : 07/14/2017
    Date last modified: 07/16/2017
    Python Version    : 2.7
'''

# Import python libraries
import numpy as np
import cv2

# set to 1 for pipeline images
debug = 0


class Detector1(object):
    """Detectors class to detect objects in video frame
    Attributes:
        None
    """
    def __init__(self):

        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20)) #structure ellipse de 3 par 3
        self.fgbg = cv2.createBackgroundSubtractorMOG2()

    def Detect(self, frame):

        #cropped=frame[(frame.shape[0]-1000):frame.shape[0],0:frame.shape[1]] 
        fgmask = self.fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)
        img_contour, contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    
        cv2.drawContours(frame, contours, -1, (0,0,255), 2)
        
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
                    cv2.circle(frame, centeroid, radius, (0, 255, 0), 2)
                    b = np.array([[x], [y]])
                    centers.append(np.round(b))
            except ZeroDivisionError:
                pass
        
        return centers
    
class Detector2(object):
    """Detectors class to detect objects in video frame
    Attributes:
        None
    """
#    def __init__(self):
#
#       

    def Detect(self, frame):
        blank_image = np.zeros((frame.shape[0],frame.shape[1],3), np.uint8)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) 
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
        cv.drawContours(resized, contours_new, -1, (0,0,255), 2)

        return centers

if __name__ == "__main__":

    cap = cv2.VideoCapture("2018-06-27-151434.webm")
    detector = Detector1()
    while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            cropped=frame[(frame.shape[0]-1000):frame.shape[0],0:frame.shape[1]] 
            # Detect and return centeroids of the objects in the frame
            centers = detector.Detect(cropped)
            resized=cv2.resize(cropped,(int((cropped.shape[1]/2)),int((cropped.shape[0]/2))),interpolation = cv2.INTER_AREA)
            cv2.imshow('resized',resized)
            k = cv2.waitKey(100) & 0xff
    cap.release()
    cv2.destroyAllWindows()
    
    
    
    
    
    
    