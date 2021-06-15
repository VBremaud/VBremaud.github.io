"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')


### Point en live

Vlive = np.array([11.2])
Vliverr = np.array([0.01])

taulive = np.array([11.8])*1e-6 #microsec puis sec
dtaulive = np.array([0.1])*1e-6


### Données



V=np.array([14.3,12.18,10.18,8.06,6.10,4.01,2.33,1.02,0.69])
Verr=np.zeros(len(V))+0.01

tau=np.array([10.3,11.3,12.4,13.3,14.6,16.6,19.7,26.8,31.7])*1e-6# pm0.1 au depart t augmente apres Attention aux grands temps à ne pas deborder
dtau=np.array([0.1,0.1,0.1,0.2,0.2,0.3,0.4,0.6,1])*1e-6

R=18e3 # Resistance de charge choisie.


### Incertitudes
C=tau/R
dC=dtau/R

xdata=V
xerrdata=Verr

ydata=C
yerrdata=dC

xlive = np.array([])
xliverr = np.array([])
if len(Vlive)>0:
    xlive = Vlive
    xliverr = Vliverr

    ylive = taulive/R
    yliverr = dtaulive/R

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

xstr='Tension de polarisation [V]'
ystr='Temps de réponse [s]'
titlestr="Temps de réponse d'une photodiode"
ftsize=18

### Ajustement

def func(x,Cp,C0,V0):
    return Cp+C0/(np.sqrt(1+x/V0))

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)


### Récupération paramètres de fit

print("\n"+titlestr)
a,b,c=popt
ua, ub, uc = np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1]),np.sqrt(pcov[2,2])

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



### Extraction des paramètres du capteur

chi2r=np.sum(((func(xfit,*popt))-yfit)**2/(yerr[debut:fin]**2))/len(xfit)
print('\nChi2réduit = ' + str(chi2r))
'''
Caacité paraiste liée au cable coax
'''
print('\nCapacité parasite extraite = '+str(a)+' +- '+str(ua)+' F') # Completement en accord avec une capacité parasite de 100 pF/m

'''
Capacité C0
'''
print('\nCapacité extraite = '+str(b)+' +- '+str(ub)+' F')# Valeur difficile à quantifier.

'''
Potentiel barrière
'''

print('\nPotentiel barrière jonction = '+str(c)+' +- '+str(uc)+' V')



### Conseil Manip
'''

Le CR LOUIS/VINCENT fait l'affaire;
On peut prendre une fréquence de 3kHz environ pour le créneau envoyé sur la LED.
Si le temps le permet faire un montage suiveur sinon laisser tber.

'''



