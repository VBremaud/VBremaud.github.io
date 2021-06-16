"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live


Gammalive=1000e-9
faslive=2000

dGammalive=10e-9
dfaslive=50

xlive=np.array([1/Gammalive])
ylive=np.array([4*np.pi**2*faslive**2])

# xlive=[]
# ylive=[]

xliverr=xlive*dGammalive/Gammalive
yliverr=np.array([8*np.pi**2*dfaslive*faslive])

#xliverr=[]
#yliverr=[]

### Données


L=36e-3
C=220e-9
R=10
#3V, 400 microseconde durée pulse, 100.000 microseconde durée acquisition, sinc autoV, abaisse triger
Gamma=1e-6

fas=np.array([2110,2540,4380,5970,7940,12370])#17430,35500])
dfas=np.array([50]*len(fas))

Gamma=np.array([966e-9,437e-9,84.7e-9,42.7e-9,22.77e-9,9.37e-9])#,4.53e-9,0.95e-9])
dGamma=np.array([0.1e-9]*len(Gamma))


xdata=1/Gamma
ydata=4*np.pi**2*fas**2
###  Attention, mesurer Gamma au RLC mètre !!!!

### Incertitudes

xerrdata=xdata*dGamma/Gamma
#yerrdata=np.array([10]*len(ydata))

yerrdata=8*np.pi**2*dfas*fas


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

ystr='$\omega_{AS}^2$ [rad^2/s^2]'
xstr="1/$\Gamma$ [1/F]"
titlestr='Pulsation de résonance du mode AS en fonction de 1/gamma'

### Ajustement

def func(x,a,b):
    return  a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y =  a + b*x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )


Rtest=np.sqrt((1/((2/b)*C) - a)*2*(2/b)**2)

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
# plt.xlim(-0.025,0.1)
# plt.ylim(-2e-5,9e-5)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()