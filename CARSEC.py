#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 14:29:57 2022

@author: namnguyen
"""

import pandas as pd
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
import copy
from collections import defaultdict,OrderedDict


#%%# Create a None Database

# =============================================================================

# DB['titulo']=str

# DB['unid']=str
# DB['norm']=str
# DB['secc_horm']=str
# DB['coef']={'coef_horm':float,'coef_arma':float,'coef_pret':float}
# DB['phi']={'phi_compresion':float,'phi_traccion':float}
# DB['puntos']=[{'punt':1, 'X':0,'Y':0},{'punt':2, 'X':2,'Y':0},{...}] # pandasDataFrame.to_dict('records')
 

# DB['horm']={'fck':float,'puntos_contorno':[[points],[points],...]}

# DB['hp']=[[points],[points],...]  NOTE: this is a list of lists.
# DB['hc']=[{punto:int,radio:float},{...}]

# DB['arma']={'fyk':float,'single':[{punto:int,area},{...}],'group':[{punto_inicial:int,punto_final:int,numero(de_armaduras):int,area:float},{...}]}
# DB['pret']={'fpk':float,'tension_inicial':float,'single':[{punto:int,area (cada cable)},{...}],'multi':[{punto_inicial:int,punto_final:int,numero(de_cable):int,area:float},{...}]}

# DB['calc']='str'   ( options : "dibu", "inte", "inte vert") 

# DB['LC']=[{"Axil":-10, 'monento_X':5, 'monento_Y':2}]
# 
# =============================================================================

#%% Functions:
def CARSEC_Writer(DB,export_path='CARSEC'):
    with open(export_path+'.txt', 'w') as f:
        f.write(DB['titulo']+' \n')
        f.write('* Tipo de seccion '+'\n')  
        f.write('secc '+str(DB['secc_horm'])+' \n')
        f.write('* Unidades a emplear. Opciones: tm - knm - lbin'+'\n')
        f.write('unid '+str(DB['unid'])+' \n')
        f.write('* Normativa a emplear. Opciones: ehe  asashto '+'\n')  
        f.write('norm '+str(DB['norm'])+' \n')
        f.write('* Coeficientes de seguridad EHE o coeficientes phi AASHTO. No es obligatoria '+'\n')  
        f.write('coef horm '+str(DB['coef']['coef_horm'])+' arma '+str(DB['coef']['coef_arma']) + ' pret '+str(DB['coef']['coef_pret'])+  ' \n')
        
        # DB['phi']={'phi_compresion':float,'phi_traccion':float}
        f.write('phi ')
        for v in DB['phi'].values(): 
            f.write( str(v)+' ')
        f.write('\n')

        f.write('* Puntos '+'\n')  
        f.write('punt '+'\n')
        for v in DB['puntos']:
            for k in v.keys():           
                f.write(str(v[k])+' ')
            f.write('\n')

        #f.write('* Definición del hormigón: fck, modulo de elasticidad. Este último es obligatorio '+'\n')     
 #DB['horm']={'fck':float,'puntos_contorno':[[points],[points],...]}
        f.write('* Definición del hormigón: fck, modulo de elasticidad. Este último es obligatorio '+'\n')     
        

            
        for v in  DB['horm']['puntos_contorno']:
            if v!=[]:
                f.write('horm '+str(DB['horm']['fck'])+' \n')
                for k in v:
                    f.write(str(k)+' ')
                f.write('\n')
            
                    
        for v in DB['hp'] :
            if v!=[]:
                f.write('hp ')
                for k in v:
                    f.write(str(k)+' ')
                f.write('\n')
                
                
        

        for v in DB['hc']:
            f.write('hc')
            for k in v.keys():
                f.write(str(v[k])+' ')
            f.write('\n')   
        
                

            
        f.write('* Definicion del acero pasivo: fyk '+'\n')   
        
        f.write('arma '+str(DB['arma']['fyk'])+' \n')
    
        for v in DB['arma']['single']:
            for k in v.keys():           
                f.write(str(v[k])+' ')
            f.write('\n')
        
        for v in DB['arma']['multi']:
            for k in v.keys():           
                f.write(str(v[k])+' ')
            f.write('\n')
            
        f.write('pret '+str(DB['pret']['fpk'])+' '+str(DB['pret']['tension_inicial'])+' \n')
        
        for v in DB['pret']['single']:
            for k in v.keys():           
                f.write(str(v[k])+' ')
            f.write('\n')
        
        for v in DB['pret']['multi']:
            for k in v.keys():           
                f.write(str(v[k])+' ')
            f.write('\n')
        
        
        if DB['norm'] != 'aashto' and  DB['calc']== 'inte vert':
            print(' vert only available for aashto!, the calc parameter has changed to inte')
            DB['calc']='inte'
        f.write('calc '+str(DB['calc'])+' \n')        
        for v in DB['LC'] :
            for k in v.keys():
                f.write(str(v[k])+' ' )
            f.write('\n')
        f.write('fin')    
    
    
    

#%%                         
    
def save_to_json(DB,name='my_DB'):
    with open(name+'.json', 'w') as f:
        json.dump(DB, f)
#%%        
def load_json(path='my_DB.json'):
    f= open('my_DB.json', 'r')
    DB=json.load(f)
    f.close()
    return DB

#%%
    
# Create a function Streamlit to JSON !!!!!!

def DB_to_json(DB):
    #read DB to Dict
    # Create a loop to check if the values are DF and transform to JSON
    for k,v in DB.items():
        if type(v)== pd.core.frame.DataFrame:
            v.to_json(orient='split')
        else:
            v=json.dumps(v)
            

def table_to_dict(dict_tables):
	#Create a multi database where each Database equivalents to one unique ID
	ID_list = (dict_tables['Properties']['ID'].unique()).tolist()
	multi_DB={}
	for i in ID_list:
		multi_DB[i]=defaultdict(lambda: defaultdict(dict))
		multi_DB[i]['titulo']=i
		for k in dict_tables:
			_df = dict_tables[k][dict_tables[k]['ID'] == i]
			if k=='Properties':
				multi_DB[i]['secc']=_df['secc'].tolist()[0]
				multi_DB[i]['unid']=_df['unid'].tolist()[0]
				multi_DB[i]['norm']=_df['norm'].tolist()[0]
				# coeficients 
				multi_DB[i]['coef']['coef_horm']=_df['coef_horm'].tolist()[0]
				multi_DB[i]['coef']['coef_arma']=_df['coef_arma'].tolist()[0]
				multi_DB[i]['coef']['coef_pret']=_df['coef_pret'].tolist()[0]
				# phi
				multi_DB[i]['phi']['phi_compression']=_df['phi_compression'].tolist()[0]
				multi_DB[i]['phi']['phi_traction']=_df['phi_traction'].tolist()[0]
				#parameters for concrete
				multi_DB[i]['horm']['fck']=_df['horm_fck'].tolist()[0]
				# parameters for armadura
				multi_DB[i]['arma']['fyk']=_df['arma_fyk'].tolist()[0]
				#parameters for prestressing cables
				multi_DB[i]['pret']['fpk']=_df['pret_fpk'].tolist()[0]
				multi_DB[i]['pret']['tension_inicial']=_df['tension_inicial'].tolist()[0]
				#parameters for calculation type
				multi_DB[i]['calc']=_df['calc'].tolist()[0]
				
			elif k=='puntos':
				multi_DB[i]['puntos']=_df.iloc[:,1:100].to_dict('records')

			elif k=='puntos_contorno':
				_list=[]
				for j in range(_df.shape[0]):
					_list.append(_df.iloc[j,1:100].dropna().tolist())
				multi_DB[i]['horm']['puntos_contorno']=_list
			
			elif k=="hueco_circular":
				multi_DB[i]['hc']=_df.iloc[:,1:100].to_dict('records')
			
			elif k=="hueco_poligonal":
				_list=[]
				for j in range(_df.shape[0]):
					_list.append(_df.iloc[j,1:100].dropna().tolist())
				multi_DB[i]['hp']=_list
				
			elif k=="armadura_single":
				multi_DB[i]['arma']['single']=_df.iloc[:,1:100].to_dict('records')
			
			elif k=="armadura_group":
				multi_DB[i]['arma']['multi']=_df.iloc[:,1:100].to_dict('records')
				
			elif k=="cable_single":
				multi_DB[i]['arma']['single']=_df.iloc[:,1:100].to_dict('records')
			
			elif k=="cable_group":
				multi_DB[i]['pret']['multi']=_df.iloc[:,1:100].to_dict('records')
				
			elif k=="LC":
				multi_DB[i]['LC']=_df.iloc[:,1:100].dropna().to_dict('records')
	
	return multi_DB



#def multi_CARSEC_writer(multi_DB,export_path='CS_Multi_'):
def multi_CARSEC_writer(multi_DB,export_path=''):
	for i_d in multi_DB:
		CARSEC_Writer(multi_DB[i_d], export_path=export_path+str(i_d))




#def excel_to_CARSEC(load_path,export_path='CS_Multi_'):
def excel_to_CARSEC(load_path,export_path=''):
	dict_tables = pd.read_excel(load_path,sheet_name=None)
	multi_DB=table_to_dict(dict_tables)
	multi_CARSEC_writer(multi_DB=multi_DB,export_path=export_path)
	return dict_tables,multi_DB




def polygonal_graphics(x,y,path):

	fig, ax = plt.subplots()
	
	
	trapezoid = patches.Polygon(xy=list(zip(x,y)), fill=False)
	ax.add_patch(copy.copy(trapezoid))
	
	t_start = ax.transData
	t = mpl.transforms.Affine2D().rotate_deg(0)
	t_end = t + t_start
	
	trapezoid.set_transform(t_end)
	ax.add_patch(trapezoid)
	ax.set_xlim([-5, 5])
	ax.set_ylim([-5, 5])
	fig.savefig(path+'.png',bbox_inches='tight',dpi=100)