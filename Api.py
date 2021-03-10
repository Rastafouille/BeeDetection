# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 15:12:51 2019

@author: JS235785
"""
import numpy as np
import cv2
import os
from kalman_filter import KalmanFilter
import cv2 as cv
import time

class Bee(object):
    def __init__(self,firstcenter,firstframe):
        self.frame=[]
        self.center=[]
        self.frame.append(np.copy(firstframe))
        self.center.append(np.copy(firstcenter))
        self.pollen = 0
        self.varroa= -1 #0=absent, 1=present, -1=unknow
        
    def varroa_detect(self):
        return
    
    def pollen_detect(self):
        return
    
    def add_capture(self,newcenter,newframe):
        self.frame.append(np.copy(newframe))
        self.center.append(np.copy(newcenter))
        return
    
    def sup_bord(self,img_height,img_width):
         sup=[]
         for i in range(len(self.frame)):
             if (self.center[i][0] + self.frame[i].shape[0] / 2 > img_height)  or (self.center[i][0] - self.frame[i].shape[0]/2 < 0)  or (self.center[i][1] + self.frame[i].shape[1]/2 > img_width) or (self.center[i][1] - self.frame[i].shape[1]/2 < 0) :
                     cv.imshow("sup", self.frame[i])
                     sup.append(i)
                     time.sleep(1)
                     
         for i in range(len(sup)):
             del self.frame[sup[len(sup)-i-1]]
             del self.center[sup[len(sup)-i-1]]
             print ('sup')
        
        
        #height = img.shape[0]
        #width = img.shape[1]
        
        
class Hive(object):
    def __init__(self):
        self.bees=[]
        self.pollen = 0
        self.varroa= -1 #0=absent, 1=present, -1=unknow
    def add_bee(self,Bee):
        self.bees.append(Bee)
        #cv.imshow("bee", Bee.frame[0])
        return
    def varroa_counter(self):
        return
    def pollen_counter(self,newframe):
        return  
    def save (self,repertoire):
        if not os.path.exists(repertoire):
            os.makedirs(repertoire)
        else:
            for filename in os.listdir(repertoire) :
                os.remove(repertoire + "/" + filename)
                
        for i in range(len(self.bees)):
            for j in range(len(self.bees[i].frame)):
                cv2.imwrite(repertoire+str(i+1)+"_"+str(j+1)+".png", self.bees[i].frame[j]);
        
        return