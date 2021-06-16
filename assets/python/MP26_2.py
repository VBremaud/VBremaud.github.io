"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live

tref=15.9e-9


tlive=1e-9
Ldonnelive=0

dtlive=0.2e-9
dLlive=0.05e-2


xlive=np.array([22.4*1e-2-Ldonnelive])
ylive=np.array([tref-tlive])



xliverr=np.array([dLlive])
yliverr=np.array([dtlive])

#xlive=[]
#ylive=[]
#xliverr=[]
#yliverr=[]

### Données

tref=15.9e-9 # pm 0.2

t=np.array([1.6,0.8,0.3])*1e-9

dt=np.array([0.1,0.1,0.1])*1e-9

L=np.array([28.5])*1e-2#offset : -6.1 3.9 offseet = 22.4

Ldonne=np.array([-6.1,3.9,14])*1e-2

L=(22.4*1e-2-Ldonne)
dL=np.array([0.2,0.2,0.2])*1e-2

xdata=L

ydata=tref-t


### Incertitudes

xerrdata=dL
yerrdata=dt


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

ystr='$\Delta t$ [s]'
xstr='L [m]'
titlestr='Ecart en temps à la référence en fonction de la distance'

### Ajustement

def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()

# deltaT = -2 L/c + 2 L0 / c
c = 3e8
print("Distance L0 mesurée = "+str(a*c/2)+" +- "+str(ua*c/2)+" m")