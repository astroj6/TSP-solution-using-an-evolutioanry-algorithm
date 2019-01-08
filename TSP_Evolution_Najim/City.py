# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 09:08:07 2018

@author: jforr
"""
import math
# city class description where we will hold information about each city
destinations = []
class City:
    def __init__(self,x,y,name,num):
        self.x=x #coordinates
        self.y=y 
        self.name=name
        self.num = num
    def getDistance(self , city):
        difX = self.x-city.x
        difY = self.y-city.y
        distance = math.sqrt(math.pow(difX,2)+math.pow(difY,2))
        return distance
    
