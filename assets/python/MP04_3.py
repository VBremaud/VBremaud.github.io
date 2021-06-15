"""
@Louis Heitz et Vincent Brémaud

"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Point en live

mlive=np.array([20]) #en g
dmlive=np.array([1])*1e-3 #en mg puis en g

Ulive = np.array([-15])
dUlive = np.array([0.3])

### Données

U=np.array([0.06,-4.4,-25.9])
dU=np.array([0.6,0.3,0.3])

m=np.array([0,9.9,30]) #en g
dm=np.array([1]*len(m))*1e-3 #en mg puis en g

### Traitements
xdata=m
xerrdata=dm

ydata=U
yerrdata=dU

xlive = np.array([])
xliverr = np.array([])

xerr=xerrdata
yerr=yerrdata
if len(mlive)>0:
    xlive = mlive
    xliverr = dmlive

    ylive = Ulive
    yliverr = dUlive
#
# if len(xliverr) >0 :
#     xerr=np.concatenate((xerrdata,xliverr))
#     yerr=np.concatenate((yerrdata,yliverr))
#
#
# if len(xliverr)== 0 :


### Données fit


debut=0
fin=len(xdata)+1


xfit=xdata[debut:fin]
yfit=ydata[debut:fin]




### Noms axes et titre

ystr='Tension [mV]'
xstr="masse ajoutée [g]"
titlestr='Tension en fonction de la masse ajoutée'
ftsize=18

### Ajustement

def func(x,a,b):
    return  a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

print("\n"+titlestr)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y =  a + b*x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )


### Tracé de la courbe

plt.figure(figsize=(10,9))
xtest = np.linspace(np.min(xdata),np.max(xdata),100)

xlive2=(ylive-a)/b
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
plt.plot(xtest,func(xtest,*popt),label='Ajustement ')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Masse attendue')
    plt.errorbar(xlive2,ylive,yerr=yliverr,fmt='o',c='red',label='Masse déduite')
    plt.plot([0,xlive2],[ylive,ylive],'--',c='red')
    plt.plot([xlive2,xlive2],[min(func(xtest,*popt)),ylive],'--',c='red')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()

### Extraction des paramètres du capteur

'''
Sensibilité du capteur
'''
s=1/b# Sensibilité en kg/mV
ds=ub/b**2
print("Sensibilité du capteur : "+str(s)+" +- "+str(ds)+" kg/mV")

'''
Resolution du capteur
'''
M=1 # Environ 1 mV decelable au multimetre, ca va dependre du multimetre du coup !
R=s*M #Résolution du capteur

print('\nMasse déduite : ' + str(xlive2[0]) + ' g')
print('\nMasse attendue : ' + str(xlive[0])+ ' g')
