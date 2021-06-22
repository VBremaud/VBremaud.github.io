"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Données

#Grossissement total
yp=39.4
f=100

y=1e-3
d=25e-2
thetap=np.arctan(yp/f)
theta=np.arctan(y/d)

G=thetap/theta

#Grossissement oculaire

yp2=36.75e-2
foeil=100e-2
thetap2=np.arctan(yp2/foeil)
y2=0.9e-2
theta2=np.arctan(y2/d)
Goc = thetap2/theta2

#Grossissement objectif

h=39.4e-2
ab=36.75e-2/9

Gob=h/ab

dimage=0.8e-2
D=90.5e-2
fproj=100e-3

a=fproj*dimage/(D-fproj)

delta=160e-3

foc=250e-3/Goc
h=a*delta/foc #Diamètre du diaphragmme d'ouverture

ON = Gob*np.sin(a/(2*foc)) #Fonctionne avec réseau de 100 à 300 traits / mm


