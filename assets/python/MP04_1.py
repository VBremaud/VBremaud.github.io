"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Point en live

Tslive = np.array([40e-3]) #en sec
dTslive = np.array([1e-3]) #en sec

dlive = np.array([8e-2]) #en m
ddlive = np.array([5e-4]) #en m

deltaTlive = np.array([800e-3]) #en sec


### Données
f0=42.6e3
df0=0.1e3

T_sortie=np.array([632e-3/13,632e-3/15,616e-3/16,1324e-3/16,1.348/19,1.562/17]) #en sec
dT_sortie=np.array([1e-3]*len(T_sortie))

d=np.array([8.25e-2,8e-2,8e-2,8e-2,8e-2,8e-2]) #en m
dd=np.array([0.05e-2]*len(d))

deltaT=np.array([990e-3,830e-3,752e-3,1.616,1.378,1.79]) #en sec pour la vitesse, éventuellement rajouter une incertitude si besoin

### Traitements
f_sortie=1/T_sortie
df=dT_sortie / T_sortie**2

xdata=d/deltaT #vitesse
xerrdata=dd/d*xdata #erreur prépondérante sur la distance

ydata=f_sortie/f0 #Attention facteur 2 en réflexion ! Cf wikipedia
yerrdata=np.sqrt((df/f_sortie)**2 + (df0/f0)**2)*ydata

xlive = np.array([])
xliverr = np.array([])
if len(Tslive)>0:
    fslive = 1/Tslive
    dfslive = dTslive / Tslive**2

    xlive=dlive/deltaTlive
    xliverr=ddlive/dlive*xlive

    ylive=fslive / f0
    yliverr=np.sqrt((dfslive/fslive)**2 + (df0/f0)**2)*ylive

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

ystr='$\Delta f / f_0$ '
xstr='$v$ [m/s]'
titlestr='Différence de fréquences en fonction de la vitesse'
ftsize=18

### Ajustement

def func(x,a,b):
    return a+ b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

print("\n"+titlestr)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(12,9))
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

print("\nMesure de la célérité du son")
print("c = "+str(2/b)+" +- "+str(2*ub/b**2)+" m/s")