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
#
# Llive=439.7
# klive=
#
# dLlive=
#
# xlive=np.array([1/Llive**2])
# xliverr=np.array([])
#
#
# ylive=np.array([])/6
# yliverr=np.array([0.00002/6*np.sqrt(2)])


xlive=np.array([])
xliverr=np.array([])
### Données

#Pour avoir une canneulreu : delta_k = k lambda_k = deltan(lambda_k) e. On détermine l'ordre pour la première cannelure puis on en déduit les deltak. On trace ensuite delta_l/e = delta n en fonction de 1/lambda^2


L=[426,439.7,455.18,472,489.9,510.10,532,556.27,582.82,612.7,646.01]
 #longueur d'onde
#L=[487,512,539,569,605,645,687]
L.reverse() #Pour l'avoir dans le bon sens
L=np.array(L)*1e-9

k=np.zeros(len(L)-1) #Recherche de l'ordre
OPD=np.zeros(len(L)-1) #différence de marche
u=np.zeros(len(L)-1)
for i in range (len(L)-1):
    u[i]=L[i+1]/(L[i]-L[i+1]) #Au premier ordre
    k[i]=L[i+1]/(L[i]-L[i+1])
    OPD[i]=k[i]*L[i]


k=np.array([17,18,19,20,21,22,23,24,25,26]) #On prend le premier ordre puis on complète
for i in range (len(L)-1):
      OPD[i]=k[i]*L[i]



e=1.2e-3
de=0.005e-3

dL=np.array([1e-9]*len(L))
dOPD=k*dL[:-1]

xdata=1/(L[:-1]**2)
ydata=OPD/e



### Incertitudes



xerrdata=2*dL[:-1]/L[:-1]**3
yerrdata=np.sqrt((dOPD/OPD)**2)*ydata# + (de/e)**2)*ydata




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

if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata[debut:fin],xliverr))
    yerr=np.concatenate((yerrdata[debut:fin],yliverr))


if len(xliverr)== 0 :
    xerr=xerrdata[debut:fin]
    yerr=yerrdata[debut:fin]

### Noms axes et titre

ystr=r'$\Delta n$'
xstr=r'1/$\lambda^2$ [$m^{-2}$]'
titlestr='Loi de Cauchy pour la biréfringence'
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x+b


popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr,absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(12,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
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


## Estimation de la pente theorique



















