# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as pl

from matplotlib.widgets import Slider


def alpha_out(alpha_0, alpha_in, n_0, n_1):
    return np.arcsin((n_0/n_1)*np.sin(alpha_in))

def back_projection(x, y, alpha_0, alpha_in, radius):
    yr = (radius*(np.sin(alpha_0)+np.cos(alpha_0)))
    xr = (radius*(np.cos(alpha_0)-np.sin(alpha_0)))

    yr = (x*np.sin(alpha_in)+y*np.cos(alpha_in))
    xr = (x*np.cos(alpha_in)-y*np.sin(alpha_in))
    
    mag = np.sqrt(yr**2+xr**2)
    yr = 1.25*radius*yr/mag
    xr = 1.25*radius*xr/mag
    
    x = x + xr
    y = y + yr
    return x, y
    

def propagate_to_floor(x, y, alpha_0, alpha_in, n_0, n_1):
    a_out = alpha_out(alpha_0, alpha_in, n_0, n_1) - np.pi/2

    m = np.tan(a_out + np.pi/2 + alpha_0)
    c = y-m*x
    x_floor = -c/m
    return x_floor

def propagate_to_second_surface(x, y, alpha_0, alpha_in, n_0, n_1, radius1, radius2):
    a_out = alpha_out(alpha_0, alpha_in, n_0, n_1) + np.pi/4
    
    l = (radius1 - radius2)
    
    beta = np.arcsin(np.sin(a_out)*l/radius2)
    alpha_2 =  alpha_0 + np.pi/2 - a_out - beta
    
    x_out = radius2*np.cos(alpha_2)
    y_out = radius2*np.sin(alpha_2)
    
    
    if y_out <= 0:
        return None, None
    return x_out, y_out


n_glass = 1.5 # (works for acrylic too since that has a refractive index of 1.49).
n_air = 1
radius1 = 1
radius2 = 0.5
search_radius = 2
points = 51
segments = 11


#figure setup.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])


alpha_ins = np.linspace(-np.pi/3,np.pi/3,segments)
#alpha_ins = np.linspace(0,0,segments)

#draw circle one.
alpha_0s = np.linspace(-np.pi/2,0,points) + np.pi/2
xs = np.cos(alpha_0s)*radius1
ys = np.sqrt(radius1**2-xs**2)
ax.plot(xs,ys, color = 'black')

#draw circle two.
xs = np.cos(alpha_0s)*radius2
ys = np.sqrt(radius2**2-xs**2)
ax.plot(xs,ys, color = 'black')



ax.set_ylim(0,radius1*search_radius*2)
ax.set_xlim(-radius1*search_radius,radius1*search_radius)
ax.axis('equal')

linewidth = 2

min_color = 0.1
max_color = 0.9
top = int(points*(alpha_0s[-1] + alpha_ins[-1]/2)/(2*np.pi))
colors1 = pl.cm.jet(np.linspace(min_color,max_color,top+1))
for alpha_0 in alpha_0s:
    #PLOT CLOURED CIRCLE
        for alpha_in in alpha_ins:
            x = np.cos(alpha_0)*radius1
            y = np.sin(alpha_0)*radius1
            
            strand_index = int(points*(alpha_0 + alpha_in/2)/(2*np.pi))
            
            x_surface, y_surface = back_projection(x, y, alpha_0, alpha_in, radius1)
            ax.plot([x_surface, x], [y_surface, y], color = colors1[strand_index], alpha = 0.3, linewidth = linewidth)
            
            
            # attempt to propagate to surface
            x_second, y_second = propagate_to_second_surface(x, y, alpha_0, alpha_in, n_air, n_glass, radius1, radius2)
            if x_second != None and y_second != None:
                ax.plot([x, x_second], [y, y_second], alpha = 0.3, linewidth = linewidth, color = colors1[strand_index])
            
            
                x_floor = propagate_to_floor(x_second, y_second, alpha_0, alpha_in, n_glass, n_air)
                if x_floor != None:
                    if x_floor > -radius1*search_radius and x_floor < radius1*search_radius:
                        ax.plot([x, x_floor], [y, 0], alpha = 0.65, linewidth = linewidth, color = colors1[strand_index])


#prep color circle
alpha_0sc = np.linspace((alpha_0s[0] + alpha_ins[0]/2)- np.pi/2, (alpha_0s[-1] + alpha_ins[-1]/2) - np.pi/2,1000) + np.pi/2
colors = pl.cm.jet(np.linspace(min_color,max_color,1000))
xs = np.cos(alpha_0sc)*radius1*2.25
ys = np.sin(alpha_0sc)*radius1*2.25
ax.scatter(xs, ys , color = colors)

ax.axhline(y=0,color='k')     
ax.axvline(x=0, color = 'k')           
ax.set_xlabel('Horizontal Position')
ax.set_ylabel('Vertical Position')


            
