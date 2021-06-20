# -*- coding: utf-8 -*-




import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
plt.close('all')

def linear(x,a,b):
    return a*x+b





import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
def linear(x,a,b):
    return a*x+b


plt.close('all')

'''
VERIFICATION DE LA LOI DE BIOT
AUTEUR: TOM PEYROT & BENJAMIN CAR


De l'acide tartrique à 100g/L devrait faire l'affaire.

'''
### Point en live

alpha0=180.4

xlive=np.array([])
xliverr=np.array([])


ylive=np.array([])
yliverr=np.array([])



### Données

alpha0=180.4 # Angle d'équipenombre avec la solution d'eau distillée.
alpha=np.array([184.4,183,182.4,181.2,180.7])-alpha0
dalpha=np.zeros(np.size(alpha))+0.2

cm=100 # Concentration de la solution d'acide tartrique en g/L
dcm=cm*np.sqrt((0.1/10)**2+(0.1/100)**2) #pesée et fiole jaugée
c=np.array([100,75,50,25,10])/1000 # Différentes dillutions obtenues. Convertie en g/cm^3
dc=(np.zeros(np.size(c))+dcm)/1000 # incertitude sur la concentration

#%% Données live
alphalive=np.array([183.5])-alpha0
dalphalive=np.array([0.2])
clive=np.array([80])

ydata=alpha
xdata=c
### Incertitudes



xerrdata=dc
yerrdata=dalpha


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

ystr='Angle de rotation ($^{\circ}$)'
xstr='Concentration en g/$cm^{3}$'
titlestr='Vérification expérimentale de la loi de Biot'
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x+b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )



## DOnnées numéro 2


alpha02=180.4 # Angle d'équipenombre avec la solution d'eau distillée.
alpha2=np.array([176.4,177,178.4,179.2,180.0])-alpha02
dalpha2=np.zeros(np.size(alpha2))+0.2

cm2=100 # Concentration de la solution d'acide tartrique en g/L
dcm2=cm2*np.sqrt((0.1/10)**2+(0.1/100)**2) #pesée et fiole jaugée
c2=np.array([100,75,50,25,10])/1000 # Différentes dillutions obtenues. Convertie en g/cm^3
dc2=(np.zeros(np.size(c2))+dcm2)/1000 # incertitude sur la concentration

popt2,pcov2=curve_fit(func, c2, alpha2,sigma=dalpha2,absolute_sigma=True)

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(c2,alpha2,yerr=dalpha2,xerr=dc2,marker='s', color='darkgreen',mfc='green',ecolor='g',linestyle='',capsize=8,label='acide (-) tartrique')
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,marker='o', color='darkblue',mfc='lightblue',ecolor='b',linestyle='',capsize=8,label='acide (+) tartrique')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,marker='o', markersize=8, color='k',mfc='darkred',ecolor='k',linestyle='',capsize=8,label='Point ajouté')
plt.plot(xfit,func(xfit,*popt), color='b', linestyle='--',label='Ajustement ')
plt.plot(xfit,func(c2,*popt2), color='g', linestyle='--',label='Ajustement ')

plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


## Estimation de la pente theorique

d=2
PRS=a/(d)
dPRS=ua/d
print('Pouvoir rotatoire specifique déduit='+str(PRS))
print('Incertitude associée='+str(dPRS))