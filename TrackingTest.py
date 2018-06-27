# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv
import sys


cv.namedWindow("tracking")
camera = cv.VideoCapture("2018-06-27-151049.webm")
#camera = cv.VideoCapture("/dev/video0")

ok, image=camera.read()

tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
tracker_type = tracker_types[3] 

if not ok:
    print('Failed to read video')
    exit()

resized=cv.resize(image,(1024,778),interpolation = cv.INTER_AREA)
bbox = cv.selectROI("tracking", resized)
if tracker_type == 'BOOSTING':
    tracker = cv.TrackerBoosting_create()
if tracker_type == 'MIL':
    tracker = cv.TrackerMIL_create()
if tracker_type == 'KCF':
    tracker = cv.TrackerKCF_create()
if tracker_type == 'TLD':
    tracker = cv.TrackerTLD_create()
if tracker_type == 'MEDIANFLOW':
    tracker = cv.TrackerMedianFlow_create()
if tracker_type == 'GOTURN':
    tracker = cv.TrackerGOTURN_create()

init_once = False

while camera.isOpened():
    ok, image=camera.read()
    resized=cv.resize(image,(1024,778),interpolation = cv.INTER_AREA)
    #image.set(3,640)
    #image.set(4,480);
    if not ok:
        print 'no image to read'
        break

    if not init_once:
        ok = tracker.init(resized, bbox)
        init_once = True

    ok, newbox = tracker.update(resized)
    print ok, newbox

    if ok:
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv.rectangle(resized, p1, p2, (200,0,0))
       
    cv.imshow("tracking", resized)
    k = cv.waitKey(1) & 0xff
#if k == 27 : break # esc pressed

