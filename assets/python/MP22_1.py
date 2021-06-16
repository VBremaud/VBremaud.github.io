"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
def linear(x,a,b):
    return a*x+b


plt.close('all')


### Point en live


xlive=np.array([0.800])*1e-3
ylive=np.array([20])+273.15# Resistance mesurée en live


xliverr=(np.zeros(len(xlive))+0.005)*1e-3
yliverr=np.zeros(len(ylive))+1+0.003*ylive

#xliverr=[]
#yliverr=[]

### Données

R1=1000
R2=np.array([])
G=np.array([])


ydata=G
xdata=R2
### Incertitudes

dG=np.zeros(len(G))+1
dR=np.zeros(len(R2))+1
xerrdata=dR
yerrdata=dG


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

xstr='Resistance R2 de lampplificateur ($\Omega$) '
ystr='Gain de lamplificateur'
titlestr='Caractérisation dun amplificateur non inverseur.'
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x + b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,marker='o', color='b',mfc='white',ecolor='g',linestyle='',capsize=8,label='Preparation')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,marker='o', markersize=8, color='k',mfc='darkred',ecolor='k',linestyle='',capsize=8,label='Point ajouté')
plt.plot(xfit,func(xfit,*popt), color='r', linestyle='--',label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


### Extraction des paramètres du capteur



### CONSEIL MANIP



































