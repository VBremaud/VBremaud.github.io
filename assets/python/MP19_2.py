"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live
normalisation=1
# e0
# elive=5e-3
# Clive=2.25e-12
#
# delive=0.01*1e-3
# dClive=0.02e-12
#
#
#
#
# xlive=np.array([1/(elive+e0)])
# ylive=np.array([Clive])
# xliverr=xlive*delive/(elive+e0)
# yliverr=np.array([dClive])
#

xlive=np.array([])
ylive=np.array([])
xliverr=np.array([])
yliverr=np.array([])
### Données

normalisation=1

R=np.array([0,15,35,45,70,80,100])
Us=np.array([-1,-0.55,-0.3,-0.1,0.1,0.2,0.25])
Ue=np.array([1,1,1,1,1,1,1])


Us=Us/normalisation
Ue=Ue/normalisation
dR=np.array([0.5]*len(R))
dUs=np.array([0.05]*len(Us))
dUe=np.array([0.05]*len(Ue))

xdata=R
ydata=Us/Ue

### Incertitudes

xerrdata=dR
yerrdata=ydata*np.sqrt((dUs/Us)**2 + (dUe/Ue)**2)


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

xstr='$R$ [$\Omega$]'
ystr='$U_s/U_e$ '
titlestr="Coefficient de réflexion"

### Ajustement


def func(x,a):
    return (x-a)/(x+a)

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)
chi2=np.sum(((func(xfit,*popt))-yfit)**2/(yerr[debut:fin]**2))
chi2r=chi2/len(yfit)
### Récupération paramètres de fit

a=popt[0]
ua=np.sqrt(pcov[0,0])
print("y = (x-a)/(x+a)\na = " + str(a))
print("ua = " + str(ua))
print('chi2 réduit : ' + str(chi2r))
#b=er eo / S
chi2=np.sum(((func(xfit,*popt))-yfit)**2/(yerr[debut:fin]**2))

print('\nSoit Zc = ' + str(a) + ' +- ' + str(ua) + ' Ohm\n')
### Tracé de la courbe
xplot=np.linspace(R[0],R[-1]*1.05,100)

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',markersize=4)
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xplot,func(xplot,*popt),label='Ajustement ')
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