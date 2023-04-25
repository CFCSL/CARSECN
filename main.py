#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 10:16:07 2022

@author: namnguyen
"""



import streamlit as st
import webbrowser
import base64


st.write("***THIS IS THE MAIN PAGE***")
st.markdown("It is recommended to open this page in Firefox. Otherwise, if you use other webbrowser please click the following link to preview PDF.")
st.markdown("**Preview PDF:** [Manual CARSECN](https://github.com/NamNguyen2015/CARSECN_APPLICATIONS/blob/main/Input_files/carsecn.pdf)")

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1000" height="1000" type="application/pdf"></iframe>'
    
    st.markdown(pdf_display, unsafe_allow_html=True)
    
    st.write("The original pdf")

show_pdf("Input_files/carsecn.pdf")


