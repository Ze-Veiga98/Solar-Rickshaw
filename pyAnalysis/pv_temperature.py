#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 19:03:25 2022

@author: jose98
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import datetime
import warnings
warnings.filterwarnings("ignore")
from matplotlib.dates import DateFormatter

#plt.style.use('seaborn')
import plotly.express as px
#import plotly.graph_objects as go
import plotly.offline as py
#import math

unit = '°C'
T_NOCT = 46
Ta_NOCT = 20
G_NOCT = 800
beta = -0.0045

TOKEN_ACCESS = 'pk.eyJ1Ijoiam9zZXZlaWdhOTgiLCJhIjoiY2tsZjY2bjhrMjZnMTJ2bGI2dm14c2VwZyJ9.D4PIa7AzNR-CTHdbkm3mEw'
        


class pv_temperature():
    
    def __init__(self, filename):
       
                
        self.raw_data = pd.read_excel(filename, skiprows = 5, header = None, index_col= False)
        self.raw_data = self.raw_data.iloc[0:3023,1:3]
        print('Data imported from '+filename+'.')
        
       
        self.raw_data.iloc[:, 1] = self.raw_data.iloc[:, 1].str.lstrip('+-').str.rstrip(unit).astype(float)
        
        
        self.raw_data1 = pd.read_excel(filename, skiprows = 5, header = None, index_col= False)
        self.raw_data1 = self.raw_data1.iloc[0:3023,1:3]
        print('Data imported from '+filename+'.')
        
       
        self.raw_data1.iloc[:, 1] = self.raw_data1.iloc[:, 1].str.lstrip('+-').str.rstrip(unit).astype(float)
         
    def irradiance(self):
        
        GT = (self.raw_data1.iloc[:, 1][29:890-120] - self.raw_data.iloc[:, 1][29:890])/(T_NOCT - Ta_NOCT) * G_NOCT
        
        return GT
    
    

class data_logger(object):
    def __init__(self, filename):
        
        column_types = {}
        for i in range(0,62):
            if i != 2:
                
                column_types[i] = np.float64
           
            else:
                column_types[i] = str
        
        self.raw_data = pd.read_csv(filename,  skiprows = 1, header = None, names = range(0,62), dtype = column_types, index_col= False)
       
        
        # Cleaning the rows only with nan values
        print(self.raw_data)
        self.data = self.raw_data.dropna()
        
        print('Data imported from '+filename+'.')
        
    def generate_map(self):
        
        px.scatter_polar()
        px.set_mapbox_access_token(TOKEN_ACCESS)
        
        fig = px.scatter_mapbox(self.data, lat='lat', lon=' lon',color=' alt',
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            size_max = 6, size=0.1*np.ones(len(self.data)), zoom=15,
                            width = 1600, height = 700,
                            
                            
                            ) #range_color = vlim
            
        fig.update_layout(font_size = 30)

        py.plot(fig, filename= './' + '.html')
        
    def I_V_curve(self):
        fig, ax = plt.subplots(figsize=(10,5))
        plt.plot(self.data.iloc[:, 2], self.data.iloc[:, 9].rolling(window=30, center=False).mean())
        ax.set_xlabel(r"$Time$ [Hour]", fontsize=15)
        ax.set_ylabel(r"Temperature [$^\circ C$]", fontsize=15)
        ax.legend(prop={'size': 15})
        formatter = DateFormatter('%H:%M')
        plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
        
        plt.show()
        
        
    
        
        
        
        
        
        

#filename = 'Temp _Amb.xlsx'
#filename1 = 'sonda_4.xlsx'
filename2 = 'log_23_2021_29_07__15_17.csv'

"""
df = pd.read_csv(filename2)

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

del df[' climb']

df = df.dropna()

df["alt"] = df["alt"].replace('yaw', 0.0).astype(np.float64)

df.to_csv('log_23_2021_29_07__15_17_new.csv', index = False)
"""


#PVT = pv_temperature(filename)
#df = PVT.raw_data
#
#PVT1 = pv_temperature(filename1)
#df1 = PVT1.raw_data1

# data logger
DL = data_logger('log_23_2021_29_07__15_17_new.csv')
df2 = DL.data



#DL.generate_map()
#DL.I_V_curve()


"""
fig, ax = plt.subplots(figsize=(10,5))
plt.plot(df.iloc[:,0][29:890], df.iloc[:,1][29:890].rolling(window=120).mean(),'.',markersize=3, label='Ambient Temperature')
plt.plot(df1.iloc[:,0][29:890], df1.iloc[:,1][29:890].rolling(window=120).mean(), '.',markersize=3,label='Cell Temperature')
ax.set_xlabel(r"$Time$ [Hour]", fontsize=15)
ax.set_ylabel(r"Temperature [$^\circ C$]", fontsize=15)
ax.grid(b=True, which='major', axis='both', alpha=.5)
ax.grid(which='minor', axis='x', lw =0.5)
ax.legend(prop={'size': 15},loc='upper right')
ax.tick_params(axis='both', which='major', labelsize=15)
formatter = DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.savefig('./pv_temperature_measured' + '.pdf', format='pdf', dpi=300, bbox_inches='tight') 
plt.show()


# Irradiance
GT = (df1.iloc[:, 1][29:890].rolling(60).mean() - df.iloc[:, 1][29:890].rolling(60).mean()) / (T_NOCT - Ta_NOCT) * G_NOCT


Pmax = ((3*220 * GT) / 1000) * (1 - beta*(df1.iloc[:, 1][29:890].rolling(60).mean() - df.iloc[:, 1][29:890].rolling(60).mean()))

eff = Pmax/(GT * 4.77875)


fig, ax1 = plt.subplots(figsize=(12,7))
p1 = plt.plot(df1.iloc[:,0][29:794], df1.iloc[:,1][29:794].rolling(window=60).mean(),'.', markersize=4, color='red', label='Panel Temperature Measured', alpha=0.9)
p2 = plt.plot(df.iloc[:,0][29:794], df.iloc[29:794].rolling(60).mean(),'.', markersize=4, color='blue', label='Ambient Temperature Measured', alpha=0.9)
ax1.set_xlabel(r"$Time$ [Hour]", fontsize=15)
ax1.set_ylabel(r"Temperature [$^\circ C$]", fontsize=15)
ax1.tick_params(axis='both', which='major', labelsize=15)
ax1.grid(b=True, which='major', axis='both', alpha=.5)
ax1.grid(which='minor', axis='x', lw =0.5)
formatter = DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)

plt.title('PV module Efficiency Estimation for 29 Jul, 2021 at IST', fontsize=15)

ax2 = ax1.twinx()
p3 = ax2.plot(df.iloc[:,0][29:794], eff[0:765]*100,'.', markersize=4, color='g',label='Panel Efficiency (Eq.3.17)', alpha=0.9)
formatter = DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
ax2.set_ylabel(r"Efficiency [$\%$]", fontsize=15)
ax2.tick_params(axis='both', which='major', labelsize=15)


# added these three lines
lns = p1+p2+p3
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, prop={'size': 15},loc='center left')
plt.show()

plt.savefig('./irradiance' + '.pdf', format='pdf', dpi=300, bbox_inches='tight') 

"""


