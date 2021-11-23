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
from tools import *


# Colecting data from PVGIS using the class PVGIS 
# Now if I want to check data from specific day of the year


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
    return  4*(L_st*15 - L_loc) + EoT(n)


def sunset_angle(n,lat):
    phi = math.radians(lat)
    # Sunset hour angle
    ws = math.acos(-math.tan(phi)*math.tan(declination(n)))
    return ws

def sunrise_angle(n,lat): return -sunset_angle(n,lat)

def sunset_hour(n,lat):
    ts = 12 +  math.degrees(sunset_angle(n,lat))/15
    return ts

def sunrise_hour(n,lat):
    tsr = 12 + rad2deg(sunrise_angle(n,lat))/15
    return tsr

def true_hour_angle(n,lat,tc):
    w = 15*tc -180
    if w > sunrise_angle(n,lat) and w < sunset_angle(n,lat):
        return w
    else:  # To develop more
        return 'NaN'
    

def get_extraterrestrial_normal(datetime_or_doy, method='simpler_or_complex', solar_constant=1367):
    if method == 'simpler':
        RoverR0sqrd = 1 + 0.033*np.cos(2*math.pi*datetime_or_doy/365)
        
    elif method == 'complex':
        B = 2*math.pi*(datetime_or_doy -1)/365
        RoverR0sqrd = (1.00011 + 0.034221 * np.cos(B) + 0.00128 * np.sin(B) +
                       0.000719 * np.cos(2 * B) + 7.7e-05 * np.sin(2 * B))
    else:
        raise ValueError('Invalid method: %s', method)
    
    Gon = solar_constant*RoverR0sqrd
    
    return Gon
     
   
def get_cosine_of_zenith_angle(n,lat,tc):
    """
    function that compute the solar zeinith 
    """
    res = np.cos(declination(n))*np.cos(lat)*np.cos(true_hour_angle(n,lat,tc)) + np.sin(lat)*np.sin(declination(n))
    
    return res

def get_terrestrial_irradiance(n,lat,tc, datetime_or_doy, method='simpler_or_complex', solar_constant=1367):
    res = get_extraterrestrial_normal(datetime_or_doy, method='simpler_or_complex', solar_constant=1367)* get_cosine_of_zenith_angle(n,lat,tc)
    
    return res



def beam_irradiance(n,lat,tc,dni):
    """
    Determine the direct irradiance 
    
    .. math::
        G_{b} = DNI \cos \theta_z
        
    Parameters
    ----------
    dni : numeric
       Direct normal irradiance on  a horizontal surface measured by pyranomerter in W/m2
       
    For computing the cosine of zenit please see the the above defined function
    """
    
    res = dni *  get_cosine_of_zenith_angle(n,lat,tc)
    return res



def isotropic_sky_model(surface_tilt,dhi):
    r"""
    Determine diffuse irradiance from the sky on a tilted surface using
    the isotropic sky model
    
    .. math::
        
        G_{d} = DHI \frac{ 1 + \cos\beta}{2}
        
    Hottel and Woertz's model treats the sky as a uniform source of
    diffuse irradiance. Thus the diffuse irradiance from the sky (ground
    reflected irradiance is not included in this algorithm) on a tilted surface
    can be found from the diffuse horizontal irradiance an the tilt angle
    of the surface.
    
    Parameters
    ---------
    surface_tilt : numeric
        Surface tilt angle in decimal degrees. Tilt must be >= 0 and <= 180
        The tilt angle is defined as degrees from horizontal (e.g. surface
        facing up  = 0, surface facing horizon = 90)
    
    dhi : numeric
        Diffuse horizontal irradiance in W/m^2. DHI must be >= 0.
        
    Returns
    -------
    diffuse : numeric 
        The sky diffuse component of the solar radiation

    """
    
    sky_diffuse = dhi * (1 + np.cos(surface_tilt))* 0.5
    
    return sky_diffuse


def perez_model(surface_tilt, surface_azimuth, dhi, dni, solar_zenith,
                solar_azimuth, airmass, return_components=False):
    """
    Determine diffuse irradiance from the sky on a tilted surafce using 
    Perez model.
    
    Perez model determines the diffuse irradiance from the sky on a tilted surface using
    the surface tilt angle, surface azimuth angle, diffuse horizontal irradiance, direct 
    normal irradiance, extraterrestrial irradiance, sun zenitha angle, sun azimuth, and air
    mass. 
    
    Parameters
    ----------
    surface : numeric
        Surface tilt angles in decimal degrees. surface_tilt must be >=0 and <= 180
        The tilt angle is defined as degrees from horizontal
        
    surface_Azimuth : numeric
        Surface azimuth angles ind decimal degrees. surface_azimuth must be >=0 and <= 360
        The azimuth convention is defined as degrees east of north (e.g., North = 0, South = 180
        East = 90, West = 270)
        
    dhi : numeric
        Diffuse horizontal irradiance in W/m^2. 
        
    dni : numeric
        Direct normal irradiance in W/m2
        
    dni_extra : numeric
        Extraterrestrial normal irradiance in W/m2
        
    solar_zenith : numeric
        apparent (refraction-corrected) zenith angles in decimal
        degrees. solar_zenith must be >=0 and <=180.
        
    solar_azimuth : numeric
        Sun azimuth angles in decimal degrees. solar_azimuth must be >=0
        and <=360. The azimuth convention is defined as degrees east of
        north (e.g. North = 0, East = 90, West = 270).
        
    airmass : numeric
        Relative (not pressure-corrected) airmass values. If AM is a
        DataFrame it must be of the same size as all other DataFrame
        inputs. AM must be >=0 (careful using the 1/sec(z) model of AM
        generation)

    """
    
    
    a = max(0,1.0)
    b = max(np.cos(85),get_cosine_of_zenith_angle(n,lat,tc))
    a_b = a/b
    
    
    
    
    
    
    return a_b
                
        




    





