"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live

Ulive=50
Ilive=60e-3

dUlive=1
dIlive=5e-3


xlive=np.array([Ilive])
ylive=np.array([Ulive])


xliverr=np.array([dIlive])
yliverr=np.array([dUlive])
#xlive=[]
#ylive=[]



#xliverr=[]
#yliverr=[]

### Données

def func(x,a,b):
    return a + b*x

xdata=np.array([41.9,80.2,120.2,160,199.5,240.4,281,320,360,400]) #I
ydata=np.array([30.8,60.2,90.2,117.3,141,163,178,190,200,208]) #U
xdata=xdata/1000


#0.2 a partur de 200 pour xdata
### Incertitudes

xerrdata=np.array([0.005]*len(ydata))
yerrdata=np.array([0.05]*len(xdata))



### Données fit


debut=0
fin=4

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
    xerr=xerrdata
    yerr=yerrdata

### Noms axes et titre

ystr='$U$ [V]'
xstr='$I$ [A]'
titlestr="Tension dans l'induit en fonction de l'intensité dans l'inducteur"

### Ajustement

def func(x,a,b):
    return a+b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr,absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',markersize=4,label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
#plt.axis([0,3.600,0,5])
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()