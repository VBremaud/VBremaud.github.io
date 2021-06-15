import numpy as np
import os
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.close('all')
ftsize=18

### Point en live


Rlive = np.array([])/2000 #rayon en m
Rliveerr = np.array([1e-4])

deltaTlive = np.array([]) #en sec
deltaTliveerr = np.array([0.01]) #en sec


### Données
r = 3e-3 / 2
mu = 0.11e-3 / (4/3 * np.pi * r**3) #avec 39 billes, mesure de la masse volumique
D = 500e-3 #distance entre le début et la fin de la chute

R = np.array([1,1.5,2,2.5,3,3.5,4,4.5,5])/2000 #rayon en m
Rerr = np.array([1e-4]*len(R))

#T10 = temps de chute en sec avec une bille de diamètre 1 mm
T10 = np.array([1,1.05,1])
T15 = np.array([1,1.05,1])
T20 = np.array([1,1.05,1])
T25 = np.array([1,1.05,1])
T30 = np.array([1,1.05,1])
T35 = np.array([1,1.05,1])
T40 = np.array([1,1.05,1])
T45 = np.array([1,1.05,1])
T50 = np.array([1,1.05,1])


### Traitements
deltaT = np.array([np.mean(T10),np.mean(T15),np.mean(T20),np.mean(T25),np.mean(T30),np.mean(T35),np.mean(T40),np.mean(T45),np.mean(T50)])
deltaTerr = np.array([np.std(T10)/np.sqrt(len(T10)),np.std(T15)/np.sqrt(len(T15)),np.std(T20)/np.sqrt(len(T20)),np.std(T25)/np.sqrt(len(T25)),np.std(T30)/np.sqrt(len(T30)),np.std(T35)/np.sqrt(len(T35)),np.std(T40)/np.sqrt(len(T40)),np.std(T45)/np.sqrt(len(T45)),np.std(T50)/np.sqrt(len(T50))])

xdata = R**2
xerrdata= R * Rerr * np.sqrt(2)

ydata = D / deltaT
yerrdata= D * deltaTerr / deltaT**2

xlive = np.array([])
xliverr = np.array([])
if len(Rlive)>0:
    xlive = Rlive **2
    xliverr = Rliveerr * np.sqrt(2)

    ylive = D / deltaTlive
    yliverr = D * deltaTliveerr / deltaTlive**2

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

ystr="Vitesse [m/s]"
xstr='Rayon^2 [m^2]'
titlestr="Mesure de la viscosité"

### Ajustement

def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

### Affichage résultats sur l'invite de commande

print("\nMesure de la viscosité")
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
xtest = np.linspace(np.min(xdata),np.max(xdata),100)

plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
plt.plot(xtest,func(xtest,*popt),label='Ajustement ')
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


### Viscosité du fluide
g = 9.81
mufluide = 1000 #à changer

eta = 2/9 * (mu - mufluide) * g /b
deta = eta * ub / b

print('On trouve une viscosité dynamique = '+str(eta)+' +- '+str(deta)+' PI')



