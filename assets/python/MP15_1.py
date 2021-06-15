"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Point en live

Blive= np.array([0.8])
dBlive = np.array([0.005])

dlive = np.array([31.9])*1e-3
delive = np.array([0.005*1e-3])


### Données
d0=32.23*1e-3
I=1 #interprétation

#e=np.array([31.92,31.09,30.87,29.82,28.56,27.82,27.31,26.67])*1e-3 #,29.11

#B=np.array([1.710,1.398,0.823,0.731,0.664,0.625,0.554])#,0.839

B=np.array([0.733,0.858])
d=np.array([32.02,31.78])*1e-3
de=0.005*1e-3 #à vérifier
dB=0.005 #à vérifier

e=2*(d0-d)
xdata=1/e
ydata=B


### Incertitudes

xerrdata=de/e**2
yerrdata=np.array([dB]*len(ydata))

xlive = np.array([])
xliverr = np.array([])
if len(Blive)>0:
    xlive=1/(2*(d0-dlive))
    xliverr=delive*xlive**2

    ylive=Blive
    yliverr=dBlive

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

ystr='B [T]'
xstr='1/e [1/m]'
titlestr="Champ dans l'entrefer en fonction de 1/e"
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x + b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

print("\n"+titlestr)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé des courbes

plt.figure(figsize=(10,9))
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

print("pente théorique mu0 N i  x Se / Sb")





















