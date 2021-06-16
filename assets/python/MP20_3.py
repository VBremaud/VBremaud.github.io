"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live

Uvidelive=53
Utubelive=15
freqlive=1.5e3

dUvidelive=0.1
dUtubelive=0.1
dfreqlive=0.05


xlive=np.array([freqlive])
ylive=np.array([np.sqrt(Uvidelive**2-Utubelive**2)/Utubelive])


xliverr=np.array([dfreqlive])
yliverr=np.sqrt((Uvidelive*dUvidelive/Utubelive**2/ylive)**2 + (Uvidelive**2/Utubelive**3*dUtubelive/ylive)**2)

#xliverr=[]
#yliverr=[]

### Données

Uvide=np.array([19.2,38.5,76.8,114.3,150.3,186.6,220.4,252.8,283.5,312.4,339.2])
Utube=np.array([12.28,14.64,15.43,15.57,15.49,15.35,15.16,14.95,14.71,14.45,14.16])
freq=np.array([500,1e3,2e3,3e3,4e3,5e3,6e3,7e3,8e3,9e3,1e4])


dfreq=1+np.zeros(len(freq))
dUvide=1+np.zeros(len(Uvide))
dUtube=1+np.zeros(len(Utube))


xdata=freq
ydata=np.sqrt(Uvide**2-Utube**2)/Utube


### Incertitudes

xerrdata=np.array([0.2]*len(xdata))

yerrdata=np.sqrt((Uvide*dUvide/Utube**2/ydata)**2 + (Uvide**2/Utube**3*dUtube/ydata)**2)


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

ystr=r'$\alpha$ '
xstr='$f$ [Hz]'
titlestr='alpha en fonction de f'

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