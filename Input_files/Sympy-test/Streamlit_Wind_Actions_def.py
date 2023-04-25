#!/usr/bin/env python
# coding: utf-8

# In[2]:


from sympy import * #Function, Eq, Symbol, Rational, ln, latex
from sympy import symbols
from sympy.physics.continuum_mechanics.beam import Beam
#from IPython.display import display,  Latex, Image, SVG
from sympy import UnevaluatedExpr as UX
from sympy.core.parameters import distribute   
import streamlit as st

# 
# 
st.write('See [The EurocodeApplied.com](https://eurocodeapplied.com/) for comparison.') 


# ## Part A: Wind and thermal actions on bridge deck and piers
# ### 3.1 Introduction
# The scope of the following example is to present the wind actions and effects usually applied on a bridge, to both deck and piers.
# The following cases will be handled:
# o Bridge during its service life, without traffic
# o Bridge during its service life, with traffic
# o Bridge under construction (most critical case)
# The aforementioned cases will be considered for two alternative pier dimensions: o Squat piers of 10 m height and rectangular cross section 2.5 m x 5.0 m
# o “High” piers of 40 m height and circular cross section of 4 m diameter
# Essentially, a wind action transversal to the deck (normal to its longitudinal axis) will be considered.
# Additional indications will be given for wind action along the bridge deck and in the vertical direction.
# Through the presentation of the example reference to the relevant EN Eurocodes Parts (essentially EN 1991-1-4) will be given as appropriate and some comments, where necessary. In the following all references to clauses of EN 1991-1-4 will be given within brackets in italics [...]. If the reference concerns another EN Eurocode Part, then it will be noted, as well.
# The wind actions on bridges are described in Section [8], with some cross references to other clauses, where necessary. In [8.2] it is noted that an assessment should be made, whether a dynamic response procedure is needed. This matter is left open for the NAs. It is also stated that “normal” bridges with spans less than 40 m generally do not need dynamic calculations; some Member States (MS) have adopted as limit span for this purpose 100 m.
# In this example it is considered that there is no need for a dynamic response procedure.
# 
# 

# ### 3.2 Brief description of the procedure
# The general expression of a wind force Fw acting on a structure or structural member is given by the following formula [5.3]:


# In[3]:


#
rho = Symbol('rho')
sigma=Symbol('sigma')

#
c_s,c_d,c_f,z_e, A_ref, q_b,v_b,v_b0, z = symbols('c_s c_d c_f z_e  A_ref q_b v_b v_b0 z')

sigma_v, k_I, z_0,z_min,k_r, z_0II = symbols('sigma_v k_I  z_0 z_min k_r z_0II')

K, n, p, c_prob,c_dir, c_season = symbols('K n p c_prob c_dir c_season')

#
F_w, q_p, I_v, v_m,c_e, c_o,c_r = symbols('F_w q_p I_v v_m c_e c_o c_r',cls=Function)


# In[4]:


# Wind force F_w(z)
def Fw(z_e=z_e, A_ref=A_ref,c_d=c_d,c_s=c_s,c_f=c_f, q_p=q_p(z_e)):
    return A_ref*c_d*c_s*c_f*q_p

# Several expressions of peak velocity pressure at hight z: q_p(z)
def q1_p(rho=rho, I_v=I_v(z), v_m=v_m(z)):  
    return (1+7*I_v)* Rational(1,2) *rho*v_m**2

def q2_p(z,q_b=q_b):
    return c_e(z)*q_b

def q3_p(z, rho=rho, v_b=v_b):
    return c_e(z)*Rational(1,2)*rho*v_b**2

#def q3_p(z):
#    return ce(z)*qb()

# The corresponding (basic velocity) pressure may also compute q_b
def qb(rho=rho, v_b=v_b):
    return UX(Rational(1,2)*rho*v_b**2)

# Turbulence intensity at a hight z: I_v(z)
def I1_v(z, sigma_v=sigma_v):
    return sigma_v/v_m(z)

def I2_v(z,z_0=z_0, k_I=k_I, c_o=c_o(z) ):
    return k_I/(c_o*ln(z/z_0))

# The mean wind velocity at a hight z: v_m(z)
def vm(v_b=v_b, c_r=c_r(z), c_o=c_o(z)):
    with distribute(False): 
        return v_b*UX(c_r)*UX(c_o)

def vb(c_prob=c_prob,c_dir=c_dir, c_season=c_season,v_b0=v_b0):
    return (c_prob*c_dir*c_season*v_b0)

# Terrain factor # it can be calculated as a parameter
def kr(z_0=z_0, z_0II=z_0II):
    return 0.19*(z_0/z_0II)**0.07

# The roughness factor c_r(z)
def cr(z,k_r=k_r, z_0=z_0):
    with distribute(False): 
        return k_r*ln(UX(z/z_0))
    
# the oreography factor: c_o
def co(z):
    return c_o_val

# The exposure factor c_e(z)
def ce(I_v=I_v(z), c_r=c_r(z), c_o=c_o(z)):
    return (1+7*I_v)*c_r**2*c_o**2

# The probability factor
def cprob(K=K, n=n, p=p):
    return (((1-K*ln(-ln(1-p,evaluate=False)))/(1-K*ln(-ln(0.98,evaluate=False)))))**n
#%%
#st.latex(latex(Eq(v_m(z), vm())))

# In[ ]:
st.title(' Wind and thermal actions on bridge deck and piers')

st.header('3.1 Introduction')

st.write('The scope of the following example is to present the wind actions and effects usually applied on a bridge, to both deck and piers. The following cases will be handled: o Bridge during its service life, without traffic o Bridge during its service life, with traffic o Bridge under construction (most critical case) The aforementioned cases will be considered for two alternative pier dimensions: o Squat piers of 10 m height and rectangular cross section 2.5 m x 5.0 m o “High” piers of 40 m height and circular cross section of 4 m diameter Essentially, a wind action transversal to the deck (normal to its longitudinal axis) will be considered. Additional indications will be given for wind action along the bridge deck and in the vertical direction. Through the presentation of the example reference to the relevant EN Eurocodes Parts (essentially EN 1991-1-4) will be given as appropriate and some comments, where necessary. In the following all references to clauses of EN 1991-1-4 will be given within brackets in italics [...]. If the reference concerns another EN Eurocode Part, then it will be noted, as well. The wind actions on bridges are described in Section [8], with some cross references to other clauses, where necessary. In [8.2] it is noted that an assessment should be made, whether a dynamic response procedure is needed. This matter is left open for the NAs. It is also stated that “normal” bridges with spans less than 40 m generally do not need dynamic calculations; some Member States (MS) have adopted as limit span for this purpose 100 m. In this example it is considered that there is no need for a dynamic response procedure.')


st.header('3.2 Brief description of the procedure')

st.write('The general expression of a wind force Fw acting on a structure or structural member is given by the following formula [5.3]:')

st.write(" Where:")

st.write(" - $c_{d} c_{s}$ is the structural factor [6] ")
st.write("  - $c_{f}$ is the force coefficient [8.3.1, 7.6 and 7.13, 7.9.2, respectively, for the deck, the rectangular ")
st.write("  and the cylindrical pier]")
st.write("  - $q_p(z_e)$ is the peak velocity pressure [4.5] at reference height ze, which is usually taken as the height ")
st.write("  z above the ground of the C.G. of the structure subjected to the wind action ")
st.write("  - $A_{ref}$ is the reference area of the structure [8.3.1, 7.6, 7.9.1, respectively, for the deck, the rectangular and the cylindrical pier]")    
st.write("  In the example considered, as no dynamic response procedure will be used, it may be assumed that $c_sc_d = 1.0$ [8.2(1)]. Otherwise [6.3] together with [Annex B or C] should be used to determine the structural factor.")
st.write("  The peak velocity pressure $q_p(z)$ at height $z$, includes the mean and the short-term (turbulent) fluctuations and is expressed by the formula [4.8]:")
    
st.latex(r'''\operatorname{q_{p}}{\left(z \right)} =\rho \left(\frac{7 \operatorname{I_{v}}{\left(z \right)}}{2} + \frac{1}{2}\right) \operatorname{v_{m}}^{2}{\left(z \right)}= q_{b} \operatorname{c_{e}}{\left(z \right)}=\frac{\rho v_{b}^{2} \operatorname{c_{e}}{\left(z \right)}}{2} ''')

st.write('where: ')



st.write(" $\rho$ is the air density (which depends on the altitude, temperature and barometric pressure to be expected in the region during wind storms; the recommended value, used in this example, is $1.25 kg/m3$ ")
st.write('- $v_m(z)$ is the mean wind velocity at a height $z$ above the ground [4.3] ')
st.write('- $I_v(z)$ is the turbulence intensity at height $z$, defined [4.4(1)] as the ratio of the standard deviation of ')
st.write('the turbulence divided be the mean velocity, and is expressed by the following formula [4.7]')



# In[5]:
st.write('Input parameters')

c_dir_val = st.number_input('c_dir:', value=1.0, key='c_dir')

c_season_val= st.number_input('c_season:', value=1.0, key='c_season')

v_b0_val= st.number_input('v_b0:', value=26.0, key='v_b0')

p_val= st.number_input('p:', value=0.01, key='p')

K_val= st.number_input('K:', value=0.2, key='K')

n_val= st.number_input('n:', value=0.5, key='n')

rho_val= st.number_input('rho:', value=1.25, key='rho')

z_0_val= st.number_input('z_0:', value=0.05, key='z_0')

z_0II_val= st.number_input('z_0II:', value=0.05, key='z_0II')

z_val= st.number_input('z:', value=10.0, key='z')

z_min_val= st.number_input('z_min:', value=2.0, key='z_min')

k_I_val= st.number_input('k_I:', value=1.0, key='k_I')

A_ref_val= st.number_input('A_ref:', value=800.0, key='A_ref')

c_d_val= st.number_input('c_d:', value=1.0, key='c_d')

c_s_val= st.number_input('c_s:', value=1.0/c_d_val, key='c_s')

c_f_val= st.number_input('c_f:', value=1.55, key='c_f')

c_o_val= st.number_input('c_o:', value=1.0, key='c_o')


#%%

text = '<p style="font-family:sans-serif; color:Red; font-size: 42px;">GREAT!</p>'
st.markdown(text, unsafe_allow_html=True)

Params = '<p style="font-family:sans-serif; color:Green; font-size: 32px;">This is your selected parameters:</p>'

st.markdown(Params, unsafe_allow_html=True)


st.markdown(f""" 
- $c_{{dir}}=$ {c_dir_val}
- $c_{{season}}=$ {c_season_val}

- $v_{{b0}}=$ {v_b0_val}
- $c=$ {p_val}
- $K=$ {K_val}
- $n=$ {n_val}
- $\\rho=$ {rho_val}
- $z_{{0}}=$ {z_0_val}
- $z_{{0,II}}=$ {z_0II_val}
- $z=$ {z_val}
- $z_{{min}}=$ {z_min_val}
- $k_{{I}}=$ {k_I_val}
- $A_{{ref}}=$ {A_ref_val}
- $c_{{d}}=$ {c_d_val}
- $c_{{s}}=$ {c_s_val}
- $c_{{f}}=$ {c_f_val}
- $c_{{o}}=$ {c_o_val}



""")


# In[12]:


st.latex(latex(Eq(F_w(z_e),Fw(z_e))))




# In[7]:


st.latex(latex(Eq(q_p(z),q1_p(z))))
st.latex(latex(Eq(q_p(z),q2_p(z))))
st.latex(latex(Eq(q_p(z),q3_p(z))))
st.latex(latex(Eq(q_b,qb())))





# In[8]:


st.markdown(f"""
where:

- $\\rho$ is the air density (which depends on the altitude, temperature and barometric pressure to be expected in the region during wind storms; the recommended value, used in this example, is ${rho_val} kg/m3$
- $v_m(z)$ is the mean wind velocity at a height $z$ above the ground [4.3]
- $I_v(z)$ is the turbulence intensity at height $z$, defined [4.4(1)] as the ratio of the standard deviation of
the turbulence divided be the mean velocity, and is expressed by the following formula [4.7]

""")


# In[9]:


st.latex(r'''I_v(z)=\frac{\sigma_{v}}{\operatorname{v_{m}}{\left(z \right)}}=\frac{k_{I}}{\operatorname{c_{o}}{\left(z \right)} \log{\left(\frac{z}{z_{0}} \right)}} \quad \text{for} \quad z_{min}\leq z\leq z_{max}''')


# In[10]:


#display(Eq(I_v(z), I1_v(z)))
#display(Eq(I_v(z), I2_v(z)))


# In[11]:


st.latex(r''' I_v(z)=I_v(z_{{min}}) \quad\qquad \text{for} \quad\qquad z\leq z_{{min}}''')




# In[12]:


st.markdown(f"""
where:

- $k_I$ is the turbulence factor (NDP value). The recommended value, used in the example, is ${k_I_val}$
- $c_o(z)$ is the oreography factor [4.3.3]
- $z_0 $ is the roughness length [Table 4.1]
The peak velocity pressure may also be expressed as a product of the exposure factor $c_e(z)$ and the basic velocity pressure qb [Eq. 4.10]. Charts of $c_e (z)$ may be drawn as a function of the terrain category and the oreography, such as [Fig. 4.2] for $c_o = {c_o_val}$ (flat terrain, [4.3.3]).
The mean wind velocity is expressed by the formula [4.3]:

""")


# In[13]:


st.latex(latex(Eq(v_m(z),vm())))

st.markdown(f""" 
where:
- $c_r(z)$ is the roughness factor, which may be an NDP, and is recommended to be determined
according to the following formulas [4.3.2]:""")


st.latex(r'''\operatorname{c_{r}}{\left(z \right)} = k_{r} \log{\left(\frac{z}{z_{0}} \right)} \quad \text{ for }\quad  \quad z_{min}\leq z\leq z_{max}''')
 
st.latex(r'''\operatorname{c_{r}}{\left(z \right)} = \operatorname{c_{r}}{\left(z_{min} \right)}\qquad \quad\text{ for }\quad  \quad z_{min}\leq z\leq z_{max}''')

# In[14]:

st.latex(latex(Eq(c_r(z),c_r(z_min))))


st.markdown(f""" 
 where:
# 
- $z_0$ is the roughness length [Table 4.1]
# 
 - $k_r$ terrain factor depending on the roughness length and evaluated according the following formula [4.5]:
""")

# In[15]:


st.latex(latex(Eq(k_r,kr())))


# In[16]:


zmax=200


# In[17]:



st.markdown(f"""
with:

- $ z_{{0II}}=$ {z_0II_val} m  (terrain category II, [Table 4.1]) 

- $z_{{min}}$ is the minimum height defined in [Table 4.1] 

- $z_{{max}}$ is to be taken as {zmax} m

- $z_0, z_{{min}}$ depend on the terrain category; recommended values are given in [Table 4.1]


It is to note, by comparing the formulas [4.8] and [4.3], that the following expression may be deduced for $c_e(z)$:

""")




# In[18]:


st.latex(latex((Eq(c_e(z),ce(z)))))


st.markdown(f""" Finally, the basic wind velocity $v_b$ is expressed by the formula [4.1]: """)

# In[19]:


st.latex(latex((Eq(v_b,vb(c_prob,c_dir, c_season,v_b0)))))

# In[20]:


st.markdown(f"""

Where:

- $v_b$ is the basic wind velocity, defined at 10 m above ground of terrain category II

- $v_{{b,0}}$ is the fundamental value of the basic wind velocity, defined as the characteristic 10 minutes mean wind velocity (irrespective of wind direction and season of the year) at 10 m above ground level in open country with low vegetation and few isolated obstacles (distant at least 20 obstacle heights)
 
- $c_{{dir}}$ is the directional factor, which may be an NDP; the recommended value is {c_dir_val}

- $c_{{season}}$ is the season factor, which may be an NDP; the recommended value is {c_season_val}

In addition to that a probability factor $c_{{prob}}$ should be used, in cases where the return period for the design defers from $T = 50$ years. This is usually the case, when the construction phase is considered. Quite often also for bridges $T = 100$ is considered as the duration of the design life, which should lead to $c_{{prob}} > 1.0$. The expression of cprob is given in the following formula [4.2], in which the values of K and n are NDPs; the recommended values are ${K_val}$ and ${n_val}$, respectively:
""")


# In[21]:



st.latex(latex((Eq(c_prob, cprob()))))


# In[22]:


st.markdown(f""" 

To resume:

To determine the wind actions on bridge decks and piers, it seems convenient to follow successively the following steps:

-  Determine $v_b$ (by choosing $v_{{b,0}}$, $c_{{dir}}$, $c_{{season}}$ and $c_{{prob}}$, if relevant); $q_b$ may also be determined at this stage.

-  Determine $v_m (z)$ (by choosing terrain category and reference height $z$ to evaluate $c_r (z)$ and $c_o(z)$).

-  Determine $q_p(z)$ (either by choosing directly $c_e(z)$, where possible, either by evaluating $I_v(z)$, after choosing $c_o(z)$).

-  Determine $F_w$ (after evaluating $A_{{ref}}$ and by choosing $c_f$ and $c_sc_d$, if relevant).

""")


st.header("3.3 Wind actions on the deck")
# 
st.subheader("3.3.1 BRIDGE DECK DURING ITS SERVICE LIFE, WITHOUT TRAFFIC")
# 
# 

# In[23]:


st.markdown(f"""
The fundamental wind velocity $v_{{b,0}}$ is an NDP to be determined by each Member State (given in the form of zone/iso-curves maps, tables etc.). For the purpose of this example the value $v_{{b,0}} = {v_b0_val}$ m/s (see Chapter 1, 1.4.4.3) has been considered. It is also considered that $c_{{dir}} = {c_dir_val}$ and $c_{{season}} = {c_season_val}$.

In the case of bridges it is usually considered that $T= 100$ years (see Chapter 1, 1.4.1) Such design working life is reflected by a (mean) probability of occurrence of the extreme event $p ={p_val}$. Therefore one gets :
""")


# In[24]:


st.latex(latex((Eq(c_prob,cprob(K, n, p)))))
st.latex(latex((Eq(c_prob,cprob(K=K_val, n=n_val, p=p_val)))))
#c_prob_val=cprob(K=K_val, n=n_val, p=p_val).doit()
c_prob_val=round(cprob(K=K_val, n=n_val, p=p_val).doit(),2)
st.latex(latex((Eq(c_prob,c_prob_val))))


# In[25]:


st.markdown(f""" This value ($c_{{prob}}$   will be further used in this example. (Note : The relevant presentation during
the Workshop has been based on $c_{{prob}} = {c_prob_val}$). Thus : """)

# In[26]:


st.latex(latex((Eq(v_b, vb(c_prob,c_dir, c_season,v_b0)))))
v_b_val=round(vb(c_prob=c_prob_val,c_dir=c_dir_val, c_season=c_season_val,v_b0=v_b0_val),2)
st.latex(latex((Eq(v_b, v_b_val))))


# In[27]:


st.markdown(f"""The corresponding (basic velocity) pressure may also be computed, according to [Eq. 4.10]:""")


# In[28]:


st.latex(latex((Eq(q_b,qb(rho, v_b)))))
q_b_val=round(qb(rho=rho_val, v_b=v_b_val).doit(),2)
st.latex(latex((Eq(q_b,q_b_val))))


# In[29]:


st.markdown(f"""Concerning the reference height of the deck $z_e$, this may be considered more or less equal to the mean distance $z$ between the centre of the bridge deck and the soil surface [8.3.1(6)]. In the general case of a sloppy valley it is more conservative to use a lower (deeper) point of the soil surface (or the water) beneath the bridge deck. In the present example a very flat valley will be considered with a roughness category II. It is also to note that in practice the upper part of the foundation is covered by a soil layer of some thickness. Following these considerations it has been considered, for simplicity, that $z_e = z$.
The two cases of pier heights will, of course, be considered separately.

Squat pier, $z = {z_val}$  m
""")


# In[30]:


st.markdown(f"""For terrain category II,  $z_0 ={z_0_val}$ and $z_{{min}} = {z_min_val} m < 10 m = z$ [Table4.1], thus:""")


# In[31]:


st.markdown('and')


# In[32]:


k_r_val=kr(z_0=z_0_val, z_0II=z_0II_val)

st.latex(latex((Eq(k_r,k_r_val))))

st.latex(latex((Eq(c_r(z),cr(z,k_r=k_r, z_0=z_0)))))
st.latex(latex((Eq(c_r(z_val),cr(z_val,k_r=k_r_val, z_0=z_0_val)))))

c_r_val=round(cr(z_val,k_r=k_r_val, z_0=z_0_val).doit(),1)
st.latex(latex((Eq(c_r(z_val),c_r_val))))


# In[33]:


st.markdown(f"""As far as the oreography factor $c_o(z)$ is concerned, due to the flat valley it is considered that $c_o(z) = 1.0$. In fact, in the general case where the ground level beneath the bridge is lower than the surrounding ground the $c_o < 1.0$. Therefore the peak wind velocity is:""")


# In[34]:


st.latex(latex((Eq(v_m(z),vm()))))
st.latex(latex((Eq(v_m(z_val),vm(v_b=v_b_val, c_r=c_r_val, c_o=c_o_val)))))
v_m_val=round(vm(v_b=v_b_val, c_r=c_r_val, c_o=c_o_val).doit(),2)
st.latex(latex((Eq(v_m(z_val),v_m_val))))


st.markdown(f"""The turbulence intensity is:""")

# In[35]:


I2_v(z)


# In[36]:

st.latex(latex((Eq(I_v(z),I2_v(z)))))
I_v_val=round(I2_v(z=z_val,z_0=z_0_val, k_I=k_I_val,c_o=c_o_val),2)
st.latex(latex((Eq(I_v(z_val),I_v_val))))


st.markdown(f"""and""")
# 

# In[37]:


st.latex(latex((Eq(q_p(z),q1_p()))))
q_p_val=round(q1_p(rho=rho_val, I_v=I_v_val,v_m=v_m_val),2)  

st.latex(latex((Eq(q_p(z),q_p_val))))


# In[38]:


st.latex(latex((Eq(q_p(z),q2_p(z)))))


st.markdown(f"""Hence""")

# In[39]:


c_e_val=round(q_p_val/q_b_val,2)
st.latex(latex(Eq(c_e(z),c_e_val)))


# In[40]:


st.markdown(f"""We can also calculate c_e(z) directly""")
st.latex(latex((Eq(c_e(z), ce()))))
c_e_val= round(ce(I_v=I_v_val, c_r=c_r_val, c_o=c_o_val),2)

st.latex(latex((Eq(c_e(z_val),c_e_val))))


# In[41]:


st.latex(latex((Eq(F_w(z),Fw(z)))))
# after some calculations we show the following values

A_ref_val=800
c_f_val=1.55


st.latex(latex((Eq(A_ref, A_ref_val))))
st.latex(latex((Eq(c_f, c_f_val))))

# Substituting into the wind force equation:

#Fw(z_e=z_e, A_ref=A_ref,c_d=c_d,c_s=c_s,c_f=c_f, q_p=q_p(z_e)):

F_w_val= round(Fw(z_e=z_val,A_ref=A_ref_val,c_d=c_d_val, c_s=c_s_val, c_f=c_f_val,q_p=q_p_val),2)

st.latex(latex((Eq(F_w(z_val), F_w_val))))


# In[42]:



st.markdown(f"""

In this specific case the same result could be obtained by making use of [Fig. 4.2], because $c_o(10) = {c_o_val}$.

Further calculations are needed to determine the wind force on the deck [5.3].

Both the force coefficient cf and the reference area $A_{{ref}}$ of the bridge deck [8.3.1] depend on the width to (total) depth ratio b/dtot of the deck, where dtot represents the depth of the parts of the deck which are considered to be subjected to the wind pressure.

In the case of the bridge in service, without consideration of the traffic, according to [8.3.1(4) and Table 8.1], $d_{{tot}}$ is the sum of the projected (windward) depth of the structure, including the projecting solid parts, such as footway or safety barrier base, plus $0.3m$ for the open safety barrier used in the present example, in each side of the deck (see also Fig. 1.10 and drawings (Fig.1.11) of the cross section). Consequently:

$$d_{{tot}}=2.800+0.400-2.025*2.500+0.200+2*0.300=3.1375+0.200+0.600=3.9375 \\approx 4.00 m$$ 

""")


# In[43]:


# Addition parameters

d_tot, b, L, c_fx0, c_fx=symbols('d_tot b L c_fx0 c_fx')
# d_tot is the sum of the projected (windward) depth of the structure
d_tot_val=4

#
b_val=12.0
L_val=200.0
c_fx0_val=1.55


# In[44]:


d_tot=symbols('d_tot')
#st.latex(latex((Eq(d_tot,d_tot_val))))




# In[45]:


st.markdown(f"""

The depth (height) of the concrete support of the safety barrier has been taken into account, since $0.200 > 0.025 x 3.500 + 0.030 + 0.080 = 0.0875 + 0.110 = 0.1975 m$ ( projection of the remaining slope of the deck to the center line, waterproofing layer, asphalt layer).

Hence:

$b/d_{{tot}} = {b_val} / {d_tot_val} = 3 (12.00 / 3.94 ≈ 3.05)$

$A_{{ref}} =d_{{tot}} *L={d_tot_val} *{L_val}= {d_tot_val *L_val} m2$

$c_{{fx,0}} \\approx {c_fx0_val}$ [Fig. 8.3]

$c_{{fx}} = c_{{fx,0}} \\approx {c_fx0_val}$ [Eq. 8.1]

""")


# 
st.markdown(f"""
If the bridge is sloped transversally (e.g. a curved bridge) $c_{{fx,0}}$ should be increased by $$3%$$ per degree of inclination, but no more than $$25%$$ [8.3.1(3)]
Finally:$
""")

# In[46]:


st.latex(latex((Eq(F_w(z_val), F_w_val))))


# In[47]:


# wind load in x-direction

w_val=F_w_val/L_val


# In[48]:



st.markdown(f"""
Or “wind load” in the transverse (x-direction): $w = F_w/L= {F_w_val}/{L_val} \\approx {round(F_w_val/L_val,2)}$ $kN/m$
It is also to note that in [8.3.2] a simplified method is proposed for the evaluation of the wind force in x-
direction. In fact formula [5.3] is slightly modified and becomes the following formula [8.2]:

""")


# In[49]:


C, A_refx = symbols('C A_refx')

expr16=Rational(1,2)*rho*v_b**2*C*A_refx

st.latex(latex((Eq(F_w(z),expr16))))


# In[55]:



st.markdown(f"""

Where $C = c_e * c_{{f,x}}$ is given in [Tab. 8.2] depending on $b/d_{{tot}}$ and $z_e$ . In our case one would get (by interpolation) the value:
$(3.0-0.5) / (4.0-0.5) = (6.7-C)/(6.7-3.6) \\rightarrow 2.5/3.5 = (6.7-C)/3.1 \\rightarrow C = 6.7 - 3.1*2.5/3.5 = 4.4857 \\approx 4.49 \\approx 4.5$, to be compared with the “exact” value $C= c_e * c_{{f,x}}={c_e_val} * {c_fx0_val}\\approx {round(c_e_val * c_fx0_val,1)}  $. Using the interpolated value of $C$ one gets:

$F_w=0.5*{rho_val}*{round(v_b_val,1)}^2*{round(c_e_val * c_fx0_val,1)} *{A_ref_val} ={round(0.5*rho_val*v_b_val**2*c_e_val * c_fx0_val*A_ref_val,2)}=????=1312kN$ 

Which, in this case, is practically equal with the “exact” value.


**“High” pier, $z = 40$ m**

For terrain category II, $z_0 = {z_0_val}$ and $z_{{min}} ={z_min_val}m < 40 m=z$[Table4.1],thus:

""")


# ## write a function to calculate C

# In[60]:



st.markdown(f"""

Or “wind load” in the transverse (x-direction): $w = A_{{ref}}/L={A_ref_val/L_val} kN/m$

The comparison with the simplified method of [8.3.2] requires double interpolations, as follows:

-  For $z_e \leq 20 m$,
$(3.0-0.5) / (4.0-0.5) = (6.7-C)/(6.7-3.6) \\rightarrow 2.5/3.5 = (6.7-C)/3.1\\rightarrow C = 6.7 - 3.1*2.5/3.5 = 4.4857 \\approx 4.49 \\approx 4.5$

- For $z_e = 50 m$, 
$(3.0-0.5) / (4.0-0.5) = (8.3-C)/(8.3-4.5) \\rightarrow 2.5/3.5 = (8.3-C)/3.8 \\rightarrow  C = 6.3 - 3.8*2.5/3.5 = 5.5857 \\approx 5.59 \\approx 5.6$

- Finally:
$(50-40) / (50-20) = (5.6-C)/(5.6-4.5) \\rightarrow 10/30 = (5.6-C)/1.1 \\rightarrow C = 5.6 - 1.1*1/3 \\approx 5.23$

Using the interpolated value of C one gets:

""")



