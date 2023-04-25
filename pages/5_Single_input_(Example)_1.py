#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 18:16:21 2022

@author: namnguyen
"""


import streamlit as st
import json
import pandas as pd
import os
from collections import defaultdict
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import CARSEC as CS
import tempfile
import re

import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

path=os.getcwd()
print(path)
#st.subheader("Single Input")
#st.markdown("**We create this page with manual introductions for all input parameters. It also allows user click and download the template as an example.**")


DB = {}
#**********************************
st.write("En el fichero de datos está permitido hacer comentarios utilizando el símbolo “* ”. ")

st.write("\n")
st.write("-***Titulo de la sección.*** Es obligatorio y debe ser la primera línea.")
title=st.text_input('Type the title: ', 'CARSECN')

DB['titulo']=title


# 3-unid
st.write("\n")
st.write("-***“unid”*** unidad")
st.write("Indica las unidades de trabajo. Las opciones son \n")
st.markdown("tm	Toneladas y metros")
st.write("     " "knm	Kilonewtons y metros")
st.write("     ""kift	Kilolibras y pies")
st.write("Los resultados se darán en las unidades definidas en este campo.")


unid=st.selectbox('"unid"' , options=['tm','knm','lbin'])
DB['unid']=unid

# 4-norm
st.write("\n")
st.write("-***“norm”*** normativa")

st.write("Indica la normativa a emplear en el cálculo. Las opciones son")

st.write("ehe	EHE-08")
st.write("aashto	AASHTO")


norm= st.selectbox('"norm"', options=['ehe','aashto'])
DB['norm']=norm

# 2-secc_horm
st.write("\n")
st.write("-***“secc horm”*** [módulo de elasticidad] (por defecto toma 3000000 t/m2)")
secc_horm= st.selectbox('"secc horm"', options=['horm'])
modulo_elasticidad=st.text_input('E', 3000000)

DB['secc_horm']=secc_horm




# 5-coef horm/ arma/ pret
st.write("\n")
st.write("-[***“coef”*** [“horm” ghorm] [“arma” garma] [“pret” gpret]].") 
st.write("Establece los coeficientes de minoración de los materiales. No es obligatorio poner esta línea. Si se ha definido como normativa la EHE-08 los coeficientes por defecto son 1,50 para el hormigón y 1,15 para los aceros. En el caso de la AASHTO todos los coeficientes valen por defecto la unidad.")

coef_horm=st.number_input('coef_horm', 1.5)
coef_arma=st.number_input('coef_arma', 1.15)
coef_pret=st.number_input('coef_pret', 1.15)



DB['coef']={'coef_horm': coef_horm,'coef_arma': coef_arma,'coef_pret': coef_pret}



st.markdown('**phi**')



phi_compression=st.text_input('phi_compression', 0.75)

phi_traction=st.text_input('phi_traction', 0.90)


DB['phi']={'phi_compression': phi_compression,'phi_traction': phi_traction}



#*******************
st.write("\n")
st.write("-[***“phi”*** compr tracc]")

st.write("Establece los coeficientes reductores que emplea la AASHTO. No es obligatorio poner esta línea. Los coeficientes por defecto son para una sección trabajando a compresión 0,75 y 0,90 en el caso de tracción. El programa calcula los coeficientes reductores en función de la deformación máxima de las armaduras.")


# *************************
#* Punto del contorno
st.write("-***“punt”*** [“[ “ unidad longitud “ ]”]")
st.write("Indica que comienza la definición de las coordenadas de los puntos de la sección. Se puede definir la unidad en la que están dados los datos (m, cm, mm, in, ft)")

st.write("-punto   coordenada X    coordenada Y")

st.write("Definición de cada uno de los puntos")


# always check if the key exist in session state:

if 'df_punt' not in st.session_state:
	_df = {'punt': list(range(1,8)), 'X': [0,2,2,0,1,0.05,1.95],'Y':[0,0,2,2,1,0.05,0.05]}
	st.session_state.df_punt= pd.DataFrame(_df,columns=['punt', 'X', 'Y'])

st.markdown('**Punto del contorno**')

if st.button("Clear table"):
    # update dataframe state
	st.session_state.df_punt= pd.DataFrame('',index=range(7), columns=['punt', 'X', 'Y'])

if st.button("Add rows"):
    # update dataframe state
	additional_rows= pd.DataFrame('',index=range(5), columns=['punt', 'X', 'Y'])
	st.session_state.df_punt=pd.concat([st.session_state.df_punt,additional_rows])
	
_df=st.session_state.df_punt.copy()
  
with st.form('test') as f:
	response = AgGrid(_df, editable=True, fit_columns_on_grid_load=True,data_return_mode=DataReturnMode.AS_INPUT,update_mode=GridUpdateMode.MODEL_CHANGED,reload_data=False,
    wrap_text=True,resizeable=True)
	st.form_submit_button('Confirm')


st.session_state.df_punt=response['data'].dropna(axis='rows', how='any')
st.write(st.session_state.df_punt)

DB['puntos'] = response['data'].dropna(axis='rows', how='any').to_dict('records')

## Generate Graphic

x=response['data']['X'].values.tolist()[0:4]
y=response['data']['Y'].values.tolist()[0:4]

# =============================================================================
# CS.polygonal_graphics(x, y,path="Output_files/graph")
# st.image("Output_files/graph.png")
# 
# =============================================================================
# *************************hormigon
st.write("\n")
st.write("-***“horm”*** fck [“[ “ unidad tensión “ ]”]")

st.write("Indica las características del hormigón para el contorno que se define. Se pueden poner varios tipo de hormigones. Dentro de esta sección se definen el contorno cerrado y los huecos poligonales y/o circulares.")
st.write("Se puede definir las unidades en las que está dada la resistencia del hormigón (tm2, kcm2, mpa, ksi,ksf, knm2).")

fck=st.text_input('"horm"', 3500)

st.write("\n")
st.write("-***“Contorno”*** puntos que definen el contorno ")
st.markdown('**Contorno**')

collect_numbers = lambda x : [str(int(i)) for i in re.split("[^0-9]", x)  if i != "" ]

_list_puntos=list()
numbers1 = st.text_input("Enter la lista de los puntos (section_1):")
_list_puntos.append(collect_numbers(numbers1))
numbers2 = st.text_input("OPTIONAL: Enter la lista de los puntos (section_2):")
_list_puntos.append(collect_numbers(numbers2))
puntos_contorno=_list_puntos 
st.write(puntos_contorno)



DB['horm']={'E': modulo_elasticidad,'fck':fck,'puntos_contorno':puntos_contorno} # 'puntos_contorno' is hp




# *************************
# Contorno Poligonal (hp)
st.write("\n")
st.write("-***“hp”*** puntos que definen el contorno poligonal")
st.markdown('**Contorno Poligonal**')



#numbers_hp = st.text_input("Enter la lista de los puntos hp:")
list_puntos_hp=list()
numbers_hp1 = st.text_input("Enter la lista de los puntos hp (section_1):")
list_puntos_hp.append(collect_numbers(numbers_hp1))
numbers_hp2 = st.text_input("OPTIONAL: Enter la lista de los puntos hp (section_2):")
list_puntos_hp.append(collect_numbers(numbers_hp2))
hp=list_puntos_hp 
st.write(hp)


DB['hp']= hp



# *************************


# always check if the key exist in session state:

if 'df_hc' not in st.session_state:
	_df = { 'Punto_Central': [5],'Radio':[0.05]}
	st.session_state.df_hc= pd.DataFrame(_df,columns=['Punto_Central', 'Radio'])

st.markdown('**hc**')

if st.button("Clear table", key="clear"):
    # update dataframe state
	st.session_state.df_hc= pd.DataFrame('',index=range(1), columns=['Punto_Central', 'Radio'])

if st.button("Add rows", key='add'):
    # update dataframe state
	additional_rows= pd.DataFrame('',index=range(5), columns=['Punto_Central', 'Radio'])
	st.session_state.df_hc=pd.concat([st.session_state.df_hc,additional_rows])
	
_df=st.session_state.df_hc.copy()
  
with st.form('test1') as f:
	response = AgGrid(_df, editable=True, fit_columns_on_grid_load=True,data_return_mode=DataReturnMode.AS_INPUT,update_mode=GridUpdateMode.MODEL_CHANGED,reload_data=False,
    wrap_text=True,resizeable=True)
	st.form_submit_button('Confirm')


st.session_state.df_hc=response['data'].dropna(how='any')

DB['hc'] =response['data'].dropna(how='any').to_dict('records')






# =============================================================================
# 
# 
# DB['hc'] = st.selectbox('', options=['hc'])
# df_hc = pd.DataFrame(
#     '',
#     index=range(1),
#     columns=['Punto_Central', 'Radio']
# )
# df_hc['Punto_Central']=[5]
# df_hc['Radio']=0.30
# st.markdown('**hc**')
# response = AgGrid(df_hc, editable=True, fit_columns_on_grid_load=True)
# DB['hc']= response['data'].to_dict('records')
# #st.write(DB['hc'])
# 
# =============================================================================
# *************************



st.write("-***“arma”*** fyk [“[ “ unidad tensión “ ]” “[ “ unidad área “ ]”]")

st.write("Indica las características del acero pasivo. Se puede definir cada armadura de manera independiente o entre dos puntos y un número de armaduras")
st.write("Se puede definir las unidades en las que está dada el límite elástico del acero (tm2, kcm2, mpa, ksi,ksf, knm2).")
st.selectbox("unidad tensión ", options=["tm2", "kcm2", "mpa", "ksi","ksf", "knm2"])

st.write("Se puede definir las unidades en las que está dada el área del acero (m2, cm2, mm2, ft2, in2). Para poder dar las unidades del área debe estar definida la unidad del límite elástico")
st.selectbox("unidad área ", options=["m2", "cm2", "mm2", "ft2", "in2"])

fyk=st.text_input('"arma"', 51000)

#DB['arma'].fyk = fyk


# *************************

# Caracteristicas
st.write("\n")
#st.write("-punto inicial    punto final      número de cables     área de cada cable")
df_Caracteristicas_single = pd.DataFrame(
    '',
    index=range(1),
    columns=['Punto','Area']
)
df_Caracteristicas_single['Punto']=[6]

df_Caracteristicas_single['Area']=[0.000314]

st.markdown('**Caracteristicas_ Armaduras_Single**')
response = AgGrid(df_Caracteristicas_single, editable=True, fit_columns_on_grid_load=True)
single = response['data'].to_dict('records')




st.write("\n")
#st.write("-punto inicial    punto final      número de cables     área de cada cable")
df_Caracteristicas = pd.DataFrame(
    '',
    index=range(1),
    columns=['Punto_Inicial', 'Punto_Final', 'No_Armadura', 'Area']
)
df_Caracteristicas['Punto_Inicial']=[6]

df_Caracteristicas['Punto_Final']=[7]
df_Caracteristicas['No_Armadura']=[10]
df_Caracteristicas['Area']=[0.000314]


st.markdown('**Caracteristicas_ Armaduras_Multi**')
response = AgGrid(df_Caracteristicas, editable=True, fit_columns_on_grid_load=True)
multi  = response['data'].to_dict('records')

DB['arma']={'fyk':fyk, 'single':single, 'multi':multi}
#************************



fpk=st.number_input('fpk',1670000 )
# Caracteristicas
st.write("\n")
#st.write("-punto inicial    punto final      número de cables     área de cada cable")
df_Caracteristicas_single_pret = pd.DataFrame(
    '',
    index=range(1),
    columns=['Punto1','Area1']
)
df_Caracteristicas_single_pret['Punto1']=[6]

df_Caracteristicas_single_pret['Area1']=[0.000314]

st.markdown('**Caracteristicas_ Cables_Single**')
response = AgGrid(df_Caracteristicas_single_pret, editable=True, fit_columns_on_grid_load=True)
single_pret = response['data'].to_dict('records')




st.write("\n")
#st.write("-punto inicial    punto final      número de cables     área de cada cable")
df_Caracteristicas_pret = pd.DataFrame(
    '',
    index=range(1),
    columns=['Punto_Inicial1', 'Punto_Final1', 'No_Armadura1', 'Area1']
)
df_Caracteristicas_pret['Punto_Inicial1']=[6]

df_Caracteristicas_pret['Punto_Final1']=[7]
df_Caracteristicas_pret['No_Armadura1']=[10]
df_Caracteristicas_pret['Area1']=[0.000314]

st.markdown('**Caracteristicas_Cables_Multi**')
response = AgGrid(df_Caracteristicas_pret, editable=True, fit_columns_on_grid_load=True)
multi_pret  = response['data'].to_dict('records')

tension_inicial=st.number_input('tension_inicial', 1395000)

DB['pret']={'fpk':fpk,'tension_inicial':tension_inicial, 'single':single_pret, 'multi':multi_pret}
#************************


#DB['pret']={'fpk':float,'tension_inicial':tension_inicial,'single':,'group':[{punto_inicial:int,punto_final:int,numero(de_cable):int,area:float},{...}]}





# *************************
#st.write("* Calculate of section")


st.markdown("-***“calc”*** tipo de cálculo  [diagrama vertical] [“[ “ unidad momento “ ]”]")

st.write("Indica el cálculo a realizar. Las opciones son")

st.write("cálculo de las características geométricas de la sección")

st.write("btención del diagrama de interacción")

st.write("Si se quiere obtener el diagrama de interacción vertical, únicamente se hace para la AASHTO, hay que poner al final de la línea “vert”")
st.write("Se puede definir las unidades en las que están dados los axiles y momentos. Para el caso de diagrama de interacción se ponen unidades de momento (tm, knm, kift, kiin). Para el caso de momento curvatura se ponen unidades de fuerza (t, kn, kip).")


calc = st.selectbox("calc", options=["dibu", "inte", "inte vert"])

DB['calc']=calc

st.write("-Axil     momento X    momento Y")


df_LC = pd.DataFrame(
    '',
    index=range(1),
    columns=['Axil', 'monento_X', 'momento_Y']
)
df_LC['Axil']=[-10]
df_LC['monento_X']=[5]
df_LC['momento_Y']=[2]

st.markdown('**LC**')
response = AgGrid(df_LC, editable=True, fit_columns_on_grid_load=True, use_checkbox=True)
DB['LC'] = response['data'].to_dict('records')

st.write("Parejas de esfuerzos para los que calcular la sección. Se pueden poner hasta 100 hipótesis")

st.write("		momc	Obtención del diagrama momento curvatura")

st.write("-Axil     beta")




#%%
file='Carsec_AutoGenerated'
#name_file = tempfile.gettempdir() + "/Carsec_AutoGenerated"

#name_file = os.path.join(tempfile.gettempdir(),file)
path=os.getcwd()
path_file = os.path.join(path,file)

#name_file = os.path.join(tempfile.gettempdir(),file)
#path=os.getcwd()
#name_file = os.path.join(path,file)


CS.CARSEC_Writer(DB=DB, export_path=path_file)
#st.write(CS.CARSEC_Writer(DB=DB, export_path="Output_files/Carsec_AutoGenerated_10"))


st.subheader('Download data')
file_txt = path_file + '.txt'
with open(file_txt, "rb") as fp:
	btn = st.download_button(label="Download",data=fp,file_name="Carsec_AutoGenerated.txt",mime="application/txt")







#%%
# =============================================================================
# st.subheader('Download data')
# name_file_txt = name_file + '.txt'
# with open(name_file_txt, "rb") as fp:
# 	btn = st.download_button(label="Download Carsec Input file",data=fp,file_name="Carsec_AutoGenerated.txt",mime="application/txt")
# 	
# 
# =============================================================================


