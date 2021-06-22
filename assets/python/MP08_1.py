# -*- coding: utf-8 -*-
"""
Created on Fri May 14 15:25:48 2021

@author: Benjamin
"""


import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

'''
-----------------------------------------------------------------------------------------------------------------
---------------------------------------MANIP ------------------------------------------------
--------------------------------------------------------------------------------------------
'''

### Point en live

ilive=0.825*1e-3/6

lamblive=445e-9

err_i=0.005_1e-3/6

err_lamb=5*1e-9

xlive=np.array([lamblive]) #
ylive=np.array([ilive]) #

xliverr=np.array([err_lamb])
yliverr=np.array([err_i])


### Données

i=np.array([0.9,0.945,1.0716,1.11,1.27])*1e-3/6
lamb=np.array([443,473,531,553,633.5])*1e-9


f=100e-3

xdata=lamb
ydata=i


### Incertitudes

xerrdata=np.array([5*1e-9]*len(xdata))
yerrdata=np.array([0.005*1e-3/6]*len(ydata))


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

titlestr="interfrange en fonction de la longueur d'onde"
ystr='$i$ [m]'
xstr="$\lambda$ [m]"
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x + b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = alpha x  + beta \nalpha= " + str(a) + "\nbeta = " + str(b))
print("u(alpha) = " + str(ua) + "\nu(beta) = " + str(ub) )

### Tracé des courbes

xfitt=np.linspace(np.min(xdata),np.max(xdata),100)
plt.figure(figsize=(12,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,marker='o', color='b',mfc='white',ecolor='g',linestyle='',capsize=8,label='Preparation')

if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,marker='o', markersize=8, color='k',mfc='darkred',ecolor='k',linestyle='',capsize=8,label='Point ajouté')
plt.plot(xfitt,func(xfitt,*popt), color='r', linestyle='--',label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()

###

print("\n\n Soit a = f'/alpha = "  + str(f/a*1e3) + " mm")






