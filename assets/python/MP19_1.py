"""
@Louis Heitz et Vincent Brémaud

"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live
e0=0.69e-3

elive=5e-3
Clive=2.25e-12

delive=0.01*1e-3
dClive=0.02e-12




xlive=np.array([1/(elive+e0)])
ylive=np.array([Clive])
xliverr=xlive*delive/(elive+e0)
yliverr=np.array([dClive])


### Données

#freq = 1kHz

e0=0.69*1e-3
e=np.array([0.5,1,1.5,2,2.5,3,4,6,9,14,16])*1e-3 #-0.4,0
C=np.array([7.86,6.02,4.88,4.14,3.6,3.25,2.66,2,1.47,1.05,0.94])*1e-12#19.17,11.53,
xdata=1/(e+e0)
ydata=C
#Limite vernier : 16.5 mm

S=11.7e-4
de=0.01*1e-3
dC=0.02e-12

### Incertitudes

xerrdata=xdata*de/(e+e0)
yerrdata=np.array([dC]*len(ydata))


if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata,xliverr))
    yerr=np.concatenate((yerrdata,yliverr))


if len(xliverr)== 0 :
    xerr=xerrdata
    yerr=yerrdata

### Données fit


debut=4
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

ystr='$C$ [F]'
xstr='$1/e$ [1/m]'
titlestr="Capacité en fonction de 1/e"

### Ajustement


def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a + b x\na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

#b=er eo / S

eps0=b/S
print('er e0 = ' + str(eps0))
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