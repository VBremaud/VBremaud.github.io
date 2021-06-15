"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Point en live

vlive = np.array([]) #en m/s
dvlive = np.array([]) #en m/s

Flive = np.array([]) #en N
dFlive = np.array([0.02]) #en N

### Données

v = np.array([6.8,8.2,10,11.2,13.1,12.4]) #en m/s
dv = np.array([0.1]*len(v)) #en m/s

F = np.array([0.08,0.145,0.21,0.255,0.36,0.3]) #en N
dF = np.array([0.02]*len(F)) #en N

### Traitements
xdata=v**2
xerrdata=2*v*dv

ydata=F
yerrdata=dF

xlive = np.array([])
xliverr = np.array([])
if len(vlive)>0:
    xlive=vlive**2
    xliverr=2*vlive*dvlive

    ylive=Flive
    yliverr=dFlive

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

ystr='Force disque [N]'
xstr='$v^2$ [m^2/s^2]'
titlestr='Force sur le disque en fonction de la vitesse au carré'
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

rho = 1.18 #rhoair dépend de T attention.
S = 0.1 #en m2

print("\nMesure de Cx")
print("Cx = "+str(b*2/rho/S)+" +- "+str(ub*2/rho/S))