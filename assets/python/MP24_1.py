import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os


def linear(x,a,b):
    return a*x+b


plt.close('all')

'''
-----------------------------------------------------------------------------------------------------------------
--------------------------------------BRUIT THERMIQUE------------------------------------------------
------------------------------------------------------------------------------------------------------------------
'''



### Point en live


Dlive=150*1e-3
ulive=0.59*1e-3

dDlive=1e-3
dulive=1e-5


xlive=np.array([Dlive])
ylive=np.array([ulive])


xliverr=np.array([dDlive])
yliverr=np.array([dulive])

#xliverr=[]
#yliverr=[]

### Données

D=np.array([50,100,200,400])*1e-3 #Plage dynamique
u=np.array([0.195,0.391,0.781,1.563])*1e-3 #Pas en tension





xdata=D
ydata=u
### Incertitudes


xerrdata=1e-3+np.zeros(len(xdata))
yerrdata=1e-5+np.zeros(len(ydata))


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

xstr='Dynamique (V)'
ystr='Pas de tension (mV)'
titlestr='Mesure de Bruit'
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

### Tracé de la courbe
xfitth=np.linspace(0,12,100)
fitth=func(xfitth,*popt)


plt.figure(figsize=(12,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Preparation')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,*popt),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


### Extraction de la pente
n=-np.log(a)/np.log(2)
dn=ua/a

print('\n Soit un nombre de bits n =' + str(n) + ' +- ' + str(dn))
