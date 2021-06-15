"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')


### Point en live

c0live = np.array([8e-6])
dc0live = c0live/100

Poutlive = np.array([370])*1e-6
dPoutlive = np.zeros(len(Poutlive))+1*1e-6

### Données


c0=np.array([1e-06,5e-06,1e-05,5e-05,0.0001]) # mol/L, ,0.0005
dc0=c0/100

Pin=450*1e-6
Pout=np.array([441.5,406,343,79,13.1])*1e-6# Je suppute que ce sont des microsW, ,0.58
dPout=np.zeros(len(Pout))+1*1e-6


xdata=c0
ydata=-np.log10(Pout/Pin)
### Incertitudes


xerrdata=dc0
yerrdata=-dPout/Pout

xlive = c0live
xliverr = dc0live

ylive = -np.log10(Poutlive/Pin)
yliverr = -dPoutlive / Poutlive


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

xstr='Concentration de la solution [mol/L]'
ystr='-$log(I/I_O)$ '
titlestr='Absorption en fonction de la concentration'
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

#print("\nSoit un coefficient d'atténuation = " + str(a) + ' +- ' + str(ua) + ' L/mol')
l=7
print('\nDonc une extinction molaire = ' + str(a/l) + ' +- ' + str(ua/l) + ' L/mol/cm' )


#Attention longueur d'onde !!! cf wikipedia








