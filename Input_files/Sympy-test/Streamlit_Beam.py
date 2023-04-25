#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:47:52 2023

@author: namnguyen
"""

import streamlit as st

from sympy.physics.continuum_mechanics.beam import Beam
from sympy import symbols

def beam_show(p):
  p.show() # gross hack to build the sympy plot, throws warning to console
  return st.pyplot(p._backend.fig)

# copied example from docs
R1, R2 = symbols("R1, R2")
E, I = symbols("E, I")
b = Beam(50, 20, 30)
b.apply_load(10, 2, -1)
b.apply_load(R1, 10, -1)
b.apply_load(R2, 30, -1)
b.apply_load(90, 5, 0, 23)
b.apply_load(10, 30, 1, 50)
b.apply_support(50, "pin")
b.apply_support(0, "fixed")
b.apply_support(20, "roller")
p = b.draw()

beam_show(p)