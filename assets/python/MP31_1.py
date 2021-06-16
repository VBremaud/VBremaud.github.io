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
L=50e-3
C=10e-9

Rlive=150
DFlive=450
Flive=7100

dRlive=5
DDFlive=5
dFlive=5


xlive=np.array([1/Rlive])

ylive=np.array([Flive/DFlive])




xliverr=np.array([dRlive/Rlive**2])
yliverr=ylive*np.sqrt((DDFlive/DFlive)**2+(dFlive/Flive)**2)

#xliverr=[]
#yliverr=[]

### Données



R=np.array([100,200,300,400])
DF=np.array([315,640,960,1250])
F=np.array([7100,7100,7100,7100])
Q=F/DF



xdata=1/R
ydata=Q
### Incertitudes
dDF=np.zeros(len(DF))+10*np.sqrt(2)
dF=np.zeros(len(F))+100
dR=np.zeros(len(R))+5

dQ=Q*np.sqrt((dDF/DF)**2+(dF/F)**2)

xerrdata=dR/R**2
yerrdata=dQ


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

xstr='1/R [$\Omega^{-1}$]'
ystr='Q'
titlestr='Etude du facteur de qualité du circuit RLC'
ftsize=18

### Ajustement



def func(x,a,b):
    return a*x+b


popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

xfit2=np.linspace(np.min(xdata),np.max(xdata),10)
yfit2=func(xfit2,*popt)
Valth=xfit*np.sqrt(L/C)

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
# plt.plot(xfit,Valth,marker='s', color='k',mfc='grey',linestyle='', markersize=8,label='Valeur theorique')
plt.plot(xfit2,yfit2,label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()








