# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 15:12:51 2019

@author: JS235785
"""
import numpy as np
import cv2
import os

class Bee(object):
    def __init__(self,firstframe,firstcenter):
        self.frame =[]
        self.frame.append(firstframe)
        self.center=[]
        self.center.append(firstcenter)
        self.pollen = 0
        self.varroa= -1 #0=absent, 1=present, -1=unknow
    def VarroaDetect(self):
        return
    def PollenDetect(self):
        return
    def AddCapture(self,newframe,newcenter):
        self.frame.append(newframe)
        self.center.append(newcenter)
        return
        
        
class Hive(object):
    def __init__(self):
        self.bees=[]
        self.pollen = 0
        self.varroa= -1 #0=absent, 1=present, -1=unknow
    def AddBee(self,Bee):
        self.bees.append(Bee)
        return
    def VarroaCounter(self):
        return
    def PollenCounter(self,newframe):
        return  
    def Save (self,repertoire):
        if not os.path.exists(repertoire):
            os.makedirs(repertoire)
        else:
            for filename in os.listdir(repertoire) :
                os.remove(repertoire + "/" + filename)
                
        for i in range(len(self.bees)):
            cv2.imwrite(repertoire+str(i+1)+".png", np.array(self.bees[i].frame[0]));
        
        return