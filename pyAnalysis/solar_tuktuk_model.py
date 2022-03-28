#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 02:05:22 2022

@author: jose98
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
np.seterr(divide='ignore', invalid='ignore');


#sns.set(style='ticks', font_scale=2.0)
import math

#mass = 893
CdAf = 1.75
Cr = 0.012
Q = 44.4
g = 9.81
rho = 1.225
v = np.linspace(0,43,100)
mass = 829.4 + 21.2*3 + 300

def F_roll(mass, v, angle=0):
    Frol = mass*g*Cr*(1 + (v)/Q)
    return Frol

def F_aerodynamic(v):
    Fad = 0.5*CdAf*rho*(v)**2
    return Fad


Prol = F_roll(mass, v) 
Pad = F_aerodynamic(v) 
Ptot = Prol + Pad


fig, ax = plt.subplots(1, figsize=(7, 5))
plt.plot(v, Prol, label=r'$F_{roll}$', linewidth=2)
#plt.plot(v, Pad, label=r'$P_{aero}$', linewidth=2)
plt.plot(v, Ptot, color='orange',label=r'$F_{roll} + F_{aero}$', linewidth=2)
plt.ylabel('Force Required (N)', fontsize=15)
plt.xlabel('Velocity (km/h)', fontsize=15)       
plt.legend(prop={'size': 15})
#plt.xlim(xmin=0)
#plt.ylim(ymin=0)
plt.text(20, 1250, r'$C_D\; A_f = 1.75 m^2 $', fontsize=15)
plt.text(30, 275, r'$C_{rr} = 0.012 $', fontsize=15)
ax.tick_params(axis='both', which='major', labelsize=15)
ax.set_yticks(np.arange(0,2500,250))
ax.grid(b=True, which='major', axis='both', alpha=.5)
plt.grid(which='minor', axis='x', lw = 0.5)
plt.tight_layout()

fig.savefig('tuk1.pdf', format='pdf', dpi=300, bbox_inches='tight')
plt.show()


angle = np.linspace(0,10, 100)
vmax = 12
Fg = mass * g * np.sin(angle*math.pi/180)
Fa_max = 0.5*CdAf*rho*(vmax)**2
fig, ax = plt.subplots(1, figsize=(7, 5))
#plt.plot(angle, Fg, label=r'$F_{roll}$', linewidth=1.5)
plt.hlines(Fa_max,0,10, color = 'orange', label=r'$F_{aero, max}$', linewidth=2)
plt.plot(angle, Fg, label=r'$F_{g}$', linewidth=2)
plt.ylabel('Force Required (N)', fontsize=15)
plt.xlabel(r'Road Slope , $\alpha$($^\circ$) ', fontsize=15)       
plt.legend(prop={'size': 15})
#plt.text(30, 250, r'Traction', fontsize=15)
#plt.text(30, 250, r'Bracking', fontsize=15)
ax.tick_params(axis='both', which='major', labelsize=15)
#ax.set_yticks(np.arange(0,2500,250))
ax.grid(b=True, which='major', axis='both', alpha=.5)
plt.grid(which='minor', axis='x', lw = 0.5)
plt.tight_layout()

fig.savefig('tuk2.pdf', format='pdf', dpi=300, bbox_inches='tight')
plt.show() 
    

