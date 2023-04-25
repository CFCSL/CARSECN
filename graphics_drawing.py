#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 13:55:38 2023

@author: namnguyen
"""

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
#%%
def generate_points_on_circle( radius, num_points,x0=0,y0=0):
    """
    Generates a list of (x, y) tuples representing points on the radius of a circle.

 

    Args:
        radius (float): The radius of the circle.
        num_points (int): The number of points to generate.

 

    Returns:
        Dict of x, y
    """
    
    points={}
    #points=list(range(1, num_points+1))
    points_x = []
    points_y = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = x0+radius * math.cos(angle)
        y = y0+radius * math.sin(angle)
        points_x.append(x)
        points_y.append(y)
    #points = {'points': points,'x':points_x, 'y':points_y}
    points = {'x':points_x, 'y':points_y}
    return points

#%%
def draw_poligonal(df):
    # assume that we have a dataframe with three columns ['points','X','Y'], first we need to see which data in dataframe_:
    print(df)

    # Prompt the user for input
    input_points = input("Enter the desired points separated by spaces: ")
    input_points = [int(i) for i in input_points.split()]

    # Filter the dataframe to include only the desired points
    df = df[df['points'].isin(input_points)]
    first_row = pd.DataFrame(df.iloc[0]).transpose()
    df_plot=pd.concat([df,first_row], axis=0)
    plt.plot(df_plot['X'], df_plot['Y'])
    plt.show()

#%%
# Example usage
points = generate_points_on_circle(1.5, 25,1,2)
points['x'].append(points['x'][0])
points['y'].append(points['y'][0])

# create a figure with size 8x6 inches
fig = plt.figure(figsize=(8, 8))
plt.plot(points['x'], points['y'])
plt.show()
df=pd.DataFrame(points)
df.to_excel('circle.xlsx', index=False)

#%%
df=pd.read_excel('Desktop/MASTER UCM/Modulo_11_Text Mining/Tarea_TM/points.xlsx') 
    
draw_poligonal(df)