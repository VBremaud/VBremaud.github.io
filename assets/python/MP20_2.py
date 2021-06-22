"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live

x0=47
R=102.5
Omega=2*np.pi*500

poslive=42
U1live=5.023
U2live=100*1e-3

dposlive=0.5
dU1live=0.005
dU2live=0.005

xlive=np.array([poslive-x0])
ylive=np.array([U2live/(U1live*Omega/R)])

xliverr=np.array([dposlive])
yliverr=ylive*np.sqrt((dU2live/U2live)**2 + (dU1live/U1live)**2)

# xlive=np.array([])
# ylive=np.array([])
# xliverr=np.array([])
# yliverr=np.array([])
### Données

x0=47 #Position du zero.
x=np.array([100,80,70,60,50,49,48,46,45,44,43,42,40,30,20])
x-=x0

dx=np.array([0.5]*len(x))

U1=np.array([5.022,5.024,5.024,5.024,5.024,5.024,5.024,5.022,5.022,5.022,5.022,5.022,5.022,5.022,5.020]) #Tension d'entrée, crête à crête

U2=np.array([691,653,527,342,123,96,58,11,20,45,65,85,134,338,523])*1e-3 #Tension aux bornes de la bobine
R=102.5 #pm RLC metre

Omega=2*np.pi*500


dU1=np.array([0.005]*len(U1))
dU2=np.array([0.005]*len(U2))

xdata=x
ydata=U2/(U1*Omega/R)


### Incertitudes

xerrdata=dx

yerrdata=ydata*np.sqrt((dU2/U2)**2 + (dU1/U1)**2)



### Données fit


debut=9
fin=14

if len(xlive) >0 :
    xlive=np.array(xlive)
    ylive=np.array(ylive)
    xfit=np.concatenate((xdata[debut:fin],xlive))
    yfit=np.concatenate((ydata[debut:fin],ylive))


if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata[debut:fin],xliverr))
    yerr=np.concatenate((yerrdata[debut:fin],yliverr))


if len(xliverr)== 0 :
    xerr=xerrdata[debut:fin]
    yerr=yerrdata[debut:fin]

if len(xlive) == 0 :
    xfit=xdata[debut:fin]
    yfit=ydata[debut:fin]


### Noms axes et titre

ystr=r'$M$ [H] '
xstr='$x$ [cm]'
titlestr='Capteur de position'

### Ajustement

def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr,absolute_sigma=True)


### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()

