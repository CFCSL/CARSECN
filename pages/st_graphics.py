#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:07:15 2023

@author: namnguyen
"""

import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
import re
import base64
import io
import xlsxwriter

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

#%%+
def generate_points_on_circle( radius, num_points,X0=0,Y0=0):
    """
    Generates a list of (X, Y) tuples representing points on the radius of a circle.

    Args:
        radius (float): The radius of the circle.
        num_points (int): The number of points to generate.

    Returns:
        Dict of X, Y
    """
    
    points={}
    p=list(range(1, num_points+1))
    points_X = []
    points_Y = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        X = x0+radius * math.cos(angle)
        Y = y0+radius * math.sin(angle)
        points_X.append(X)
        points_Y.append(Y)
    points = {'punt': p,'X':points_X, 'Y':points_Y}
    #points = {'X':points_X, 'Y':points_Y}
    df_circle_points=pd.DataFrame(points)
    
    # Save the DataFrame to an Excel file in memory
    excel_file = io.BytesIO()
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df_circle_points.to_excel(writer, index=False)
    writer.close()
    excel_file.seek(0)
    
    # Create a download button for the Excel file
    st.download_button(label="Download excel df_circle_points",
                       data=excel_file,
                       file_name='df_circle_points.xlsx',
                       mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    
	
    # Create a download button for the dataframe
    csv = df_circle_points.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="df_circle_points.csv">Download CSV df_circle_points</a>'
    st.markdown(href, unsafe_allow_html=True)

        
    df=points.copy()
  
	
    
    df['X'].append(df['X'][0])
    df['Y'].append(df['Y'][0])
  

    
    # create a figure and axis
    fig, ax = plt.subplots(figsize=(4, 4))


    # plot the data
    ax.plot(df["X"], df["Y"])

    # set the axis labels
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # display the plot in Streamlit
    st.pyplot(fig)

#%%
def draw_poligon(df,input_points):
    # assume that we have a dataframe with three columns ['points','X','Y'], first we need to see which data in dataframe_:
    
    # Filter the dataframe to include only the desired points
    df = df[df['punt'].isin(input_points)]
    first_row = pd.DataFrame(df.iloc[0]).transpose()
    df_plot=pd.concat([df,first_row], axis=0)
    #df_plot.astype('float32')

    
    # create a figure and axis
    fig, ax = plt.subplots(figsize=(4, 4))


    # plot the data
    ax.plot(df_plot['X'], df_plot['Y'])

    # set the axis labels
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # display the plot in Streamlit
    st.pyplot(fig)
    

#%%

st.write('To draw a circle')

x0=st.number_input('input x0 of center point', value=float(0.00),min_value=float(-100))
y0=st.number_input('input y0 of center point', value=float(0.00),min_value=float(-100))
radius = st.number_input('Input radius of the circle', value=1.5, min_value=0.0)
num_points=st.number_input('input number of points to draw', value=int(25), min_value=1)

generate_points_on_circle( radius, num_points,x0,y0)



#%%
st.write('to draw an arbitrary polygon:')

#%%%%%%%%%%%%%%%%%%
st.subheader('Download Template')
with open("Input_files/df_template.xlsx", "rb") as fp:
	btn = st.download_button(label="Download Template",data=fp,file_name="df_template.xlsx",mime="application/xlsx")
#%%%%%%%%%%%%%%%%%%%	
# get df
st.subheader('Upload your own Excel file')
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
	st.write('Data preview')
	df=pd.read_excel(uploaded_file)
	df=st.experimental_data_editor(df)


# get input_points
input_points=st.text_input("Enter the desired points separated by spaces: ")
input_points = [int(i) for i in input_points.split()]
st.write(input_points)


# draw a polygon from input points
draw_poligon(df, input_points)













