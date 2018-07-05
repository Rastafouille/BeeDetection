
import numpy as np
import cv2

# set to 1 for pipeline images
debug = 0


class Detector1(object):
    def __init__(self):
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20)) #structure ellipse de 3 par 3
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        self.blob_radius_thresh = 10

    def Detect(self, frame):
        #cropped=frame[(frame.shape[0]-1000):frame.shape[0],0:frame.shape[1]] 
        fgmask = self.fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)
        img_contour, contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    
        cv2.drawContours(frame, contours, -1, (0,0,255), 2)
        centers = []  # vector of object centroids in a frame
        # Find centroid for each valid contours
        for cnt in contours:
            try:
                # Calculate and draw circle
                (x, y), radius = cv2.minEnclosingCircle(cnt)
                centeroid = (int(x), int(y))
                radius = int(radius)
                if (radius > self.blob_radius_thresh):
                    cv2.circle(frame, centeroid, radius, (0, 255, 0), 2)
                    b = np.array([[x], [y]])
                    centers.append(np.round(b))
            except ZeroDivisionError:
                pass
        return centers
    
class Detector2(object):
    def __init__(self):
        self.blob_radius_thresh = 10
      

    def Detect(self, frame, previous_frame):
        previousgray=cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
        previousbinaryFrame = cv2.threshold(previousgray,127,255,cv2.THRESH_BINARY_INV)[1]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        binary = cv2.threshold(gray,50,255,cv2.THRESH_BINARY)[1]
        addition=cv2.threshold(binary+previousbinaryFrame,127,255,cv2.THRESH_BINARY_INV)[1]    
        gaussian = cv2.GaussianBlur(addition, (21, 21), 0)
        dilate = cv2.dilate(gaussian, None, iterations=4)
        final=cv2.threshold(dilate,60,255,cv2.THRESH_BINARY)[1]
        dilate2 = cv2.dilate(final, None, iterations=4)

        img_contour, contours, hierarchy = cv2.findContours(dilate2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    
        cv2.drawContours(frame, contours, -1, (0,0,255), 2)
        
        centers = []  # vector of object centroids in a frame
        # Find centroid for each valid contours
        for cnt in contours:
            try:
                # Calculate and draw circle
                (x, y), radius = cv2.minEnclosingCircle(cnt)
                centeroid = (int(x), int(y))
                radius = int(radius)
                if (radius > self.blob_radius_thresh):
                    cv2.circle(frame, centeroid, radius, (0, 255, 0), 2)
                    b = np.array([[x], [y]])
                    centers.append(np.round(b))
            except ZeroDivisionError:
                pass
            
        cv2.imshow("binary", binary)
        cv2.imshow("previousbinaryFrame", previousbinaryFrame)
        cv2.imshow("addition", addition)
        cv2.imshow("gaussian", gaussian)
        cv2.imshow("dilate", dilate)
        cv2.imshow("final", final)
        cv2.imshow("dilate2", dilate2)
        return centers

if __name__ == "__main__":

    cap = cv2.VideoCapture("2018-06-27-151434.webm")
    #detector = Detector1()
    detector = Detector2()
#pour detector2    
    previous_frame=cap.read()[1] 
    previous_cropped=previous_frame[(previous_frame.shape[0]-1000):previous_frame.shape[0],0:previous_frame.shape[1]] 
    while(True):
            # Capture frame-by-frame
            frame = cap.read()[1]
            cropped=frame[(frame.shape[0]-1000):frame.shape[0],0:frame.shape[1]] 
            # Detect and return centeroids of the objects in the frame
            #centers = detector.Detect(cropped)
            centers = detector.Detect(cropped,previous_cropped)
            
            resized=cv2.resize(cropped,(int((cropped.shape[1]/2)),int((cropped.shape[0]/2))),interpolation = cv2.INTER_AREA)
            
            previous_cropped=cropped  #pour detector2          
            cv2.imshow('resized',resized)
            k = cv2.waitKey(500) & 0xff
    cap.release()
    cv2.destroyAllWindows()
    
    
    
    
    
    
    
