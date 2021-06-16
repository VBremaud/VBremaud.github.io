"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')


### Point en live
R1=1000
R2live=2500
Glive=3.51


dR2live=1
dGlive=0.1

xlive=np.array([R2live])
ylive=np.array([Glive])


xliverr=xlive*dR2live/R2live
yliverr=ylive*dGlive/Glive

#xliverr=[]
#yliverr=[]

### Données

R1=1000
R2=np.array([2,3,4])*1e3
G=1 + R2/R1 + 0.01


ydata=G
xdata=R2


### Incertitudes

dG=np.zeros(len(G))+0.1
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

xstr="Résistance R2 de l'amplificateur [$\Omega$] "
ystr="Gain de l'amplificateur []"
titlestr="Caractérisation d'un amplificateur non inverseur."
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
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Preparation')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,*popt),label='Ajustement ')
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



































