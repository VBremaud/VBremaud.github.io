"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Point en live

freqlive = np.array([25]) #mesure au gbf en Hz
dfreqlive = np.array([0.01])

lamblive = np.array([2])*1e-2 #mesure à la règle de plusieurs lambda
dlamblive = np.array([0.02])*1e-2 #lambda en cm

### Données

freq=np.array([20,25.04,30.01,35.00,40,45,50.1])
dfreq =np.array([0.01]*len(freq))

lamb=np.array([(28.7-18)/5,(29.5-19)/6,(29.2-20.2)/6,(29.5-21.5)/6,(29-23)/5,(29.8-23.2)/6,(28.7-23.5)/5])*1e-2 #en cm
dlamb = np.array([0.02]*len(lamb))*1e-2

### Traitements
grossissement = 2 #ATTENTION à BIEN LE PRENDRE EN COMPTE, A CHANGER OU VERIFIER

lamb/= grossissement
dlamb/= grossissement

k=2*np.pi/lamb
dk = 2*np.pi * dlamb /lamb**2

omega=2*np.pi*freq
domega = 2*np.pi*dfreq

xdata= k
xerrdata = 2*np.pi * dlamb /lamb**2

ydata=omega**2
yerrdata=2*domega*omega

xlive = np.array([])
xliverr = np.array([])
if len(freqlive)>0:
    lamblive/= grossissement
    dlamblive/= grossissement

    klive = 2*np.pi/lamblive
    dklive = 2*np.pi * dlamblive /lamblive**2

    omegalive = 2*np.pi*freqlive
    domegalive = 2*np.pi*dfreqlive

    xlive= klive
    xliverr= 2*np.pi * dlamblive /lamblive**2

    ylive= omegalive**2
    yliverr = 2*domegalive*omegalive


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

ystr='$\omega^2$ [rad^2/s^2] '
xstr='$k$ [1/m]'
titlestr="Relation de dispersion"
ftsize=18

### Ajustement
h=2e-2
g=9.81
rho=1e3

def func(x,gamma):
    return np.tanh(x*h)*(g*x+ gamma*x**3/rho)

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

gamma, dgamma = popt[0], np.sqrt(pcov[0][0])
print('gamma = '+str(gamma)+' +- '+str(dgamma)+' N/m')

### Tracé de la courbe

plt.figure(figsize=(10,9))
xtest = np.linspace(np.min(xdata),np.max(xdata),100)

plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
plt.plot(xtest,func(xtest,gamma),label='Ajustement ')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()