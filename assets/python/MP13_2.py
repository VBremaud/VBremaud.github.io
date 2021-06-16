"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live

Blive=0.2
dBlive=0.01

thetalive=-10.5
dthetalive=0.5


xlive=np.array([Blive])
ylive=np.array([thetalive])

xliverr=np.array([dBlive])
yliverr=np.array([dthetalive])

### Données

B=np.array([0.173,0.203,0.234,0.262,0.287,0.309,0.219,0.245])
theta=np.array([-9,-10.4,-12.7,-14.2,-15.5,-16.4,-11.5,-13])



dB=np.array([0.01]*len(B))
dtheta=np.array([0.5]*len(theta))

xdata=B
ydata=theta

### Incertitudes

xerrdata=dB
yerrdata=dtheta


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

ystr='$\theta$ [°]'
xstr='$B$ [T]'
titlestr="Détermination de la constante de Verdet"

### Ajustement


def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a + b x\na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )


### Tracé de la courbe


plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',markersize=4)
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
#plt.axis([0,3.600,0,5])
#plt.axis([0,xdata[-1]*1.05,0,ydata[-1]*1.05])
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()

b*=np.pi/180
l=30e-3
print('\nSoit V =' + str(b/l) + ' +- ' + str(ub/b) + ' T /rad / m')
