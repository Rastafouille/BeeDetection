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