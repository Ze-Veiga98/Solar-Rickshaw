#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 21:55:16 2021

@author: josé Veiga

#### SolarIrradiance.py
### This code was developed in the scope of my master thesis...
    Its main objective is to compute the irradiance on a sloped surfaces from the data 
    given on a horizontal surfaces
"""


import datetime
import pandas as pd
import numpy as np
import math


# Colecting data from PVGIS using the class PVGIS 
# Now if I want to check data from specific day of the year

def deg2rad(deg): return math.radians(deg)
def rad2deg(rad): return math.radians(rad)

def sliceday(GHI_total,n):
    GHI_day = GHI_total[1+(n-1)*24:n*24]
    return GHI_day
    

def declination(n):
    # n is the day of the year
    decl_deg = 23.45*np.sin(2*math.pi*(284 + n)/365)
    #print('The declination for that day was = ')
    return deg2rad(decl_deg)

"""
This function computes the Equation of time E(n) on day 'n' in hours.
Definition: It is the difference between the apparent (true) solar time and the mean solar time
"""

def EoT(n):
    B = 2*math.pi*(n-1)/365
    return 3.82*60*(0.000075+0.001868*np.cos(B)-0.032077*np.sin(B)-0.014615*np.cos(2*B)-0.04089*np.sin(2*B))
    # Note that in the textbook of Duffie. They use 229.2, which is equal to 3.82*60
    
"""
This function computes the hour angle of the Sun (in rad) a clock time 'tc' on day 'n' at a given longitude 'lon'
"""
def Solar_Time_Minus_Clock_Time(n, L_st, L_loc):
    return  4*(-L_st*15 + L_loc) + EoT(n)


def sunset_angle(n,lat):
    phi = deg2rad(lat)
    # Sunset hour angle
    ws = math.acos(-math.tan(phi)*math.tan(declination(n)))
    return ws

def sunrise_angle(n,lat): return -sunset_angle(n,lat)

def sunset_hour(n,lat):
    ts = 12 +  rad2deg(sunset_angle(n,lat))/15
    return ts

def sunrise_hour(n,lat):
    tsr = 12 + rad2deg(sunrise_angle(n,lat))/15
    return tsr
    
def Gon(n):
    Gsc = 1367 # w/m2
    return (Gsc*(1 + 0.003*math.cos(2*math.pi*n/365)))

    






