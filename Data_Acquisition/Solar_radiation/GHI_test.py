#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 22:09:17 2021

@author: jose98
"""
import math
import numpy as np
from GHI_process import *
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go



x = np.linspace(1, 365, num=365)

# calculate declination
n = 324
phi = 38.77 # latitude of the site
L_st = 0
L_loc = 9.18
decl = declination(n)

st = Solar_Time_Minus_Clock_Time(324,L_st,L_loc)
#print(decl,EoT,st)
#print(st/60 + 9.18)
sunset =  sunset_angle(n,phi)
sunrise =  sunrise_angle(n,phi)
#print(sunset,sunrise)

ts = sunset_hour(n,phi)
tsr = sunrise_hour(n,phi)

#print(ts,tsr)

Gon_vector = np.vectorize(Gon)

EoT_vector = np.vectorize(EoT)

plt.plot(x,Gon_vector(x), label='Irradiance at the top of atmosphere')
plt.xlabel('day of the year')
plt.ylabel(r'$G_{on}[W/m^2]$')
plt.legend()
plt.savefig('Gon.png',dpi=150)

GHI_day = [0.0, 0.0, 0.0, 0.0, 0.0, 39.18, 209.0, 374.0, 240.0, 476.0, 379.0, 619.0, 872.01, 664.0, 680.0, 434.0, 311.0, 313.0, 169.0, 20.88, 0.0, 0.0, 0.0, 0.0]
fig, ax = plt.subplots(figsize=(5,3.5))
plt.plot(GHI_day)
ax.grid(True)
ax.set(
    title="Global Horizontal Irradiance (GHI)\nin Rennes, on 2012-05-15, from PVGIS",
    xlabel="time (UTC hours)",
    ylabel="Irradiance (W/m²)",
)
fig.tight_layout()
plt.savefig('fff.png',dpi=150)








"""df = pd.read_csv('irradiance_data.csv')
data_ghi = go.Scatter(x=df['DateTime'], y=df['GHI'], name='GHI (W/m^2)')

layout = go.Layout(title='Weather conditions', xaxis=dict(title='Date & time'), yaxis=dict(title='Value'))
fig = go.Figure(data=[data_ghi], layout=layout)
py.plot(fig, filename='weather_data.html')
"""
df = pd.read_csv('irradiance_data.csv')

df['DateTime'] =  pd.to_datetime(df['DateTime'])
df['dates'] = df['DateTime'].dt.date
df['time'] = df['DateTime'].dt.time

data = df[['dates', 'time']].copy()
GHI = df['GHI']
td = df['DateTime'].dt.dayofyear
# yearly irradiance in Lisbon
fig, ax = plt.subplots(figsize=(7,3.5))
plt.plot(td, GHI)
ax.grid(True)
ax.set(
    title="Global Horizontal Irradiance (GHI)\nin Lisbon, in 2016, from PVGIS",
    xlabel="time (day)",
    xlim=(1,367),
    ylabel="Irradiance (W/m²)",
)
fig.tight_layout()
plt.savefig('yearly-day.png',dpi=150)


n1 = 200
tm = []
for tc in range(0,23):
    tm.append(tc)
    
GHI_day1 = sliceday(GHI,n1)

fig, ax = plt.subplots(figsize=(5,3.5))
plt.plot(tm,GHI_day1)
ax.grid(True)
ax.set(
    title="Global Horizontal Irradiance (GHI)\nin Lisbon, on day $n of $year, from PVGIS",
    xlabel="time (UTC hours)",
    ylabel="Irradiance (W/m²)",
)
fig.tight_layout()









