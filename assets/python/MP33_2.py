
"""
@Louis Heitz et Vincent Brémaud

"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live


plive=2
t12live=500*1e-6
dtlive=1e-7

xlive=np.array([plive**2])
ylive=np.array([t12live])



xliverr=np.array([0])
yliverr=np.array([dtlive])

# xlive=[]
# ylive=[]
# xliverr=[]
# yliverr=[]

### Données


C=101e-9
R=1105


liste_p=np.array([1,2,3,4,5,6,7,8,9,10,11])

t12=np.array([135.2,502,1107,1967,3065,4400,5948,7616,9214,10706,12048])*1e-6

xdata=liste_p**2
ydata=t12
#xdata=xdata/1000

### Incertitudes

xerrdata=np.array([0.0]*len(xdata))
yerrdata=np.array([1e-7]*len(ydata))


# if len(xliverr) >0 :
#
#
#
# if len(xliverr)== 0 :
#     xerr=xerrdata
#     yerr=yerrdata

### Données fit


debut=0
fin=9

if len(xlive) >0 :
    xlive=np.array(xlive)
    ylive=np.array(ylive)
    xfit=np.concatenate((xdata[debut:fin],xlive))
    yfit=np.concatenate((ydata[debut:fin],ylive))
    xerr=np.concatenate((xerrdata[debut:fin],xliverr))
    yerr=np.concatenate((yerrdata[debut:fin],yliverr))


if len(xlive) == 0 :
    xfit=xdata[debut:fin]
    yfit=ydata[debut:fin]
    xerr=xerrdata[debut:fin]
    yerr=yerrdata[debut:fin]


### Noms axes et titre

ystr='$t_{1/2}$ [s]'
xstr='$p^2$ '
titlestr="Diffusion de charge"

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
#plt.axis([0,xdata[-1]*1.05,0,ydata[-1]*1.05])
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()