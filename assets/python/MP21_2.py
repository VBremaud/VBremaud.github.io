"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live

xlive=[]
ylive=[]

#xlive=[]
#ylive=[]

xliverr=np.array([])
yliverr=np.array([])

#xliverr=[]
#yliverr=[]

### Données


xdata=np.array([0.279,0.530,1.49,2.14,2.68]) #I secondaire
ydata=np.array([0.199,0.3755,1.0824,1.72,2.14]) #U secondaire

# xdata=np.array([0.03,0.068,0.113,0.155,0.2]) #I primaire
# ydata=np.array([1.27,2.76,4.53,6.22,7.98]) #U primaire


#xdata=xdata/1000

### Incertitudes

xerrdata=np.array([0.01]*len(xdata))
yerrdata=np.array([0.05]*len(ydata))


if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata,xliverr))
    yerr=np.concatenate((yerrdata,yliverr))


if len(xliverr)== 0 :
    xerr=xerrdata
    yerr=yerrdata

### Données fit


debut=0
fin=len(xdata)

if len(xlive) >0 :
    xlive=np.array(xlive)
    ylive=np.array(ylive)
    xfit=np.concatenate((xdata[debut:fin],xlive))
    yfit=np.concatenate((ydata[debut:fin],ylive))


if len(xlive) == 0 :
    xfit=xdata[debut:fin]
    yfit=ydata[debut:fin]


### Noms axes et titre

ystr='$U$ [V]'
xstr='$I$ [A]'
titlestr="Détermination dela résistance du secondaire"

### Ajustement

noise=0*np.random.rand(1,len(yfit))


yfit= yfit+ noise
yfit=yfit[0]

def func(x,a,b):
    return a+b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True,bounds=[(-1e-9,0),(1e-9,100)])

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
plt.axis([0,xdata[-1]*1.05,0,ydata[-1]*1.05])
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()
