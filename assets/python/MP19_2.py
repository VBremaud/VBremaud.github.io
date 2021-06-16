"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Point en live

Rlive = np.array([55])
dRlive =  np.array([0.1])

Uslive = np.array([-0.01])
dUslive = np.array([0.01])

Uelive = np.array([1.04])
dUelive = np.array([0.01])


### Données
Norm = 0.9 #facteur de normalisation (~0.9) avec une résistance infini en sortie.
dNorm = 0.01

R = np.array([15.5,30.5,46.9,67.6,81.5,100.1,0])
dR = np.array([0.1]*len(R))

Us = np.array([-0.58,-0.33,-0.10,0.1,0.19,0.29,-1]) * Norm
dUs = np.array([0.01]*len(Us))

Ue = np.array([1.04]*len(Us))
dUe = np.array([0.01]*len(Us))


### Traitements

xdata = R
xerrdata = dR

ydata = Us/Ue / Norm
yerrdata = ydata * np.sqrt((dUs/Us)**2+(dUe/Ue)**2+(dNorm/Norm)**2)

xlive = np.array([])
xliverr = np.array([])
if len(Rlive)>0:

    xlive=Rlive
    xliverr=dRlive

    ylive=Uslive/Uelive/Norm
    yliverr=ylive * np.sqrt((dUslive/Uslive)**2+(dUelive/Uelive)**2+(dNorm/Norm)**2)

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

ystr='Coefficient de réflexion Us/Ue []'
xstr='Résistance [$\Omega$]'
titlestr="Coefficient de réflexion en fonction de la résistance en sortie d'un câble coaxial"
ftsize=18

### Ajustement

def func(x,R):
    return (x-R)/(x+R)

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

chi2red = np.mean((yfit - func(xfit, *popt))**2/yerr[debut:fin]**2)
print("chi2 = "+ str(chi2red))

### Récupération paramètres de fit

print("\n"+titlestr)
R=popt[0]
uR=np.sqrt(pcov[0,0])
print("y = (x-R)/(x+R)")


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

print("\nMesure de l'impédance caractéristique d'un câble coaxial")
print(" Rimp = "+str(R)+" +- "+str(uR)+" Ohm")