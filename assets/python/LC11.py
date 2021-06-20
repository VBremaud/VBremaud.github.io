import numpy as np
import os
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.close('all')
ftsize=18


### Données


xdata= np.array([0,10,20,30,40,50,60,65,70,75,80,85,90,95,100])
ydata = np.array([1.333,1.337,1.342,1.348,1.353,1.358,1.361,1.362,1.3635,1.364,1.3645,1.364,1.3645,1.364,1.3615])

xlive = np.linspace(0,100,10)
ylive = np.array([1.363]*len(xlive))

xlive1 = np.linspace(0,100,10)
ylive1 = np.array([1.361]*len(xlive1))

### Incertitudes

xerrdata=np.array([1]*len(xdata))
yerrdata=np.array([0.0005]*len(ydata))

### Noms axes et titre

ystr='Indice de réfraction []'
xstr="Fraction volumique d'éthanol []"
titlestr="Variation de l'indice de réfraction avec la fraction d'éthanol"


Reau=1000 #Masse volumique
Reth=789
Meau=18.02 #Masse molaire
Meth=46.07

xdata2 = (xdata*Reth/Reau/Meth)/(((100-xdata)*Reau/Reau/Meau)+(xdata*Reth/Reau/Meth))*100

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')

plt.plot(xlive, ylive, '--', c='red',label = 'Distillation fractionnée')
plt.plot(xlive1, ylive1, '--', c='green', label = 'Distillation simple')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


xstr="Fraction massique d'éthanol []"

plt.figure(figsize=(10,9))
plt.errorbar(xdata2,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')

plt.plot(xlive, ylive, '--', c='red',label = 'Distillation fractionnée')
plt.plot(xlive1, ylive1, '--', c='green', label = 'Distillation simple')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()