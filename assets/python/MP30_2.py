"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live


Tlive=  1.05e-2
longueurlive= 5e-2

dTlive=5e-5
dlongueurlive=5e-4

xlive=np.array([longueurlive])
ylive=np.array([Tlive**2])


xliverr=np.array([dlongueurlive])
yliverr=np.array([2*dTlive*Tlive])


### Données


L=18.4e-2
D=7.4e-2
d=1.3e-2
s=np.pi*d**2/4
V=L*(np.pi*D**2/4)

T=np.array([85/7,95.2/9,104.5/11,136.4/12])*1e-3
longueur=np.array([6.9,5.1,3.85,6])*1e-2 #(2pi/T0) = c sqrt(s/(l*V)


dT=np.array([0.5e-4]*len(T))
dlongueur=np.array([0.05e-2]*len(longueur))

c=2*np.pi/T*np.sqrt((longueur)*V/s)
xdata=longueur
ydata=T**2


### Incertitudes

xerrdata=dlongueur
yerrdata=2*dT*T


if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata,xliverr))
    yerr=np.concatenate((yerrdata,yliverr))


if len(xliverr)== 0 :
    xerr=xerrdata
    yerr=yerrdata

### Données fit


debut=0
fin=5

if len(xlive) >0 :
    xlive=np.array(xlive)
    ylive=np.array(ylive)
    xfit=np.concatenate((xdata[debut:fin],xlive))
    yfit=np.concatenate((ydata[debut:fin],ylive))


if len(xlive) == 0 :
    xfit=xdata[debut:fin]
    yfit=ydata[debut:fin]


### Noms axes et titre

ystr='$T^2$ [s2] '
xstr='$L$ [m]'
titlestr='Période au carré en fonction de la longueur'

### Ajustement

def func(x,a,b):
    return b*(x+a)

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = b(x+a) \na = " + str(a) + "\nb = " + str(b))
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
# plt.xlim(-0.025,0.1)
# plt.ylim(-2e-5,9e-5)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()