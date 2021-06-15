"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')
ftsize=18

### Point en live


lambdlive = np.array([550])*1e-9
dlambdlive = np.array([1e-9])

nlive = np.array([2])
mlive = np.array([3.5])


### Données




lambd=np.array([656,485.5,433.5])*1e-9#1nm
dlambd=np.zeros(len(lambd))+1e-9

n=np.array([2,2,2])
m=np.array([3,4,5])

ydata=1/lambd
xdata=1/n**2-1/m**2


### Incertitudes

yerrdata=dlambd/lambd**2
xerrdata=np.zeros(len(xdata))+0.000001

xlive=1/nlive**2-1/mlive**2
ylive=1/lambdlive

xliverr=np.zeros(len(xlive))+0.000001
yliverr=dlambdlive/lambdlive**2

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

xstr=r'1/$n^2$-1/$m^2$ []'
ystr=r'$1/\lambda$ $[1/m]$'
titlestr='Mesure de la constante de Rydberg'

### Ajustement

def func(x,a,b):
    return a*x+b
popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True,p0=[1e9,0],maxfev=2000)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a*x+b \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe


plt.figure(figsize=(13,9))
xtest = np.linspace(np.min(xdata),np.max(xdata),100)

plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
plt.plot(xtest,func(xtest,*popt),label='Ajustement ')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()

## Extraction paramètres


Rh=a
print('Constante de Rydberg déduite:'+str(Rh/1e7))
print('Incertitude deduite'+str(ua/1e7))
print('Valeur theorique attendue'+str(1.097))

#%% CONSEIL MANIP
'''
Relire LeDIffon p353 pour les interprétations !
Absolument prendre le OCEAN FLAME.
'''

