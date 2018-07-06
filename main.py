import cv2 as cv
from detectors import Detector1,Detector2
from tracker import Tracker


###### pas fonctionnel ######

if __name__ == "__main__":

    cap = cv.VideoCapture("2018-06-27-151434.webm")
    #Choix du type de detecteur
    num_detector =1
    #mode debug pour le détecteur 1, multi fenetre et reglage des paramètres
    DEBUG=0
    # Création de la fenetre de detection et prise 1ere image
    cv.namedWindow("detection", cv.WINDOW_NORMAL)
    ok, frame = cap.read()
    if not ok:
        print('Failed to read video')
        exit()
    # Select ROI
    r = cv.selectROI("detection",frame)
    # Crop image
    cropped = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

    # Create Object detector
    if num_detector==1:
        previous_frame=cropped
        detector = Detector1(DEBUG)
    else :
        detector = Detector2()
        
    # Create Object Tracker
    #(dist_thresh, max_frames_to_skip, max_trace_length,trackIdCount)
    tracker = Tracker(300, 1, 5, 100)
    cv.namedWindow("tracking", cv.WINDOW_NORMAL)
    
     # Variables initialization
    skip_frame_count = 0
    track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                    (0, 255, 255), (255, 0, 255), (255, 127, 255),
                    (127, 0, 255), (127, 0, 127)]
    
    while(True):
        # Capture frame-by-frame
        ok,frame = cap.read()
        if not ok:
            print('Failed to read video')
            exit()
        cropped=frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])] 
        # Detect and return centeroids of the objects in the frame
        if num_detector==1:
            centers,frame = detector.Detect(cropped,previous_frame)
            previous_frame=cropped             
        if num_detector==2:
            centers,frame = detector.Detect(cropped)
        
        #cv.imshow("detection",frame)
        cv.destroyWindow("detection")
        
        # If centroids are detected then track them
        if (len(centers) > 0):

            # Track object using Kalman Filter
            tracker.Update(centers)

            # For identified object tracks draw tracking line
            # Use various colors to indicate different track_id
            for i in range(len(tracker.tracks)):
                if (len(tracker.tracks[i].trace) > 1):
                    for j in range(len(tracker.tracks[i].trace)-1):
                        # Draw trace line
                        x1 = tracker.tracks[i].trace[j][0][0]
                        y1 = tracker.tracks[i].trace[j][1][0]
                        x2 = tracker.tracks[i].trace[j+1][0][0]
                        y2 = tracker.tracks[i].trace[j+1][1][0]
                        clr = tracker.tracks[i].track_id % 9
                        cv.line(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                                 track_colors[clr], 2)

            # Display the resulting tracking frame
            cv.imshow('tracking', frame)
        
        #Exit if ESC pressed.
        k = cv.waitKey(10000);
        if k == 27:
            break;
        
    cap.release()
    cv.destroyAllWindows()
    
    
    
    
    
    
    
