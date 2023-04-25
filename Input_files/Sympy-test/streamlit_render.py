#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 16:16:06 2023

@author: namnguyen
"""





from math import sqrt

from handcalcs import handcalc

import streamlit as st
import os
import pathlib
import sys
import streamlit.web.cli as stcli

#%%
@handcalc()

def quadratic(a,b,c):

    x_1 = (-b + sqrt(b**2 - 4*a*c)) / (2*a)

    x_2 = (-b - sqrt(b**2 - 4*a*c)) / (2*a)

 

a = st.slider("Value for a:", 1,5, 5)

b = st.slider("Value for b:", -10, 10, -5)

c = st.slider("Value for c:", -20,0, -5)

 

st.write("Quadratic equation in x:")

st.latex(f"{a}x^2 + {b}x + {c} = 0")

a=5

b=-5

c=-5

latex_code,roots= quadratic(a,b,c)

st.latex(latex_code)





#%%


