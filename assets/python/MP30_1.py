"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live

f0=42.6e3
df0=0.1e3

Tlive=0.077
dlive=8e-2
ddlive=1e-3
deltaTlive=1.5

dTlive=1e-3
ddeltaTlive=0.05

xlive=np.array([dlive/deltaTlive])
ylive=np.array([1/Tlive/(f0)])

#xlive=[]
#ylive=[]

xliverr=ddlive/dlive*xlive
yliverr=np.sqrt((dTlive/Tlive)**2 + (df0/f0)**2)*ylive

#xliverr=[]
#yliverr=[]

### Données

T_sortie=np.array([632e-3/13,632e-3/15,616e-3/16,1324e-3/16,1.348/19,1.562/17])

f_sortie=1/T_sortie
f0=42.6e3
d=np.array([8.25e-2,8e-2,8e-2,8e-2,8e-2,8e-2])
dd=0.05e-2


df=0.001*f_sortie
df0=0.1e3
deltaT=np.array([990e-3,830e-3,752e-3,1.616,1.378,1.79])

v=d/deltaT
xdata=v
ydata=f_sortie/f0 #Attention facteur 2 en réflexion ! Cf wikipedia


### Incertitudes

xerrdata=dd/d*xdata
yerrdata=np.sqrt((df/f_sortie)**2 + (df0/f0)**2)*ydata


if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata,xliverr))
    yerr=np.concatenate((yerrdata,yliverr))


if len(xliverr)== 0 :
    xerr=xerrdata
    yerr=yerrdata

### Données fit


debut=0
fin=len(xdata)+1

if len(xlive) >0 :
    xlive=np.array(xlive)
    ylive=np.array(ylive)
    xfit=np.concatenate((xdata[debut:fin],xlive))
    yfit=np.concatenate((ydata[debut:fin],ylive))


if len(xlive) == 0 :
    xfit=xdata[debut:fin]
    yfit=ydata[debut:fin]


### Noms axes et titre

ystr='$\Delta f / f_0$ '
xstr='$v$ [m/s]'
titlestr='Différence de fréquences en fonction de la vitesse'

### Ajustement

def func(x,a,b):
    return a+ b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )


c=2/b
uc=c*ub/b
print('\nSoit c =' + str(2/b) + ' +- ' + str(uc) + ' m/s')

### Tracé de la courbe

plt.figure(figsize=(12,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
# plt.xlim(-0.025,0.1)
# plt.ylim(-2e-5,9e-5)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()