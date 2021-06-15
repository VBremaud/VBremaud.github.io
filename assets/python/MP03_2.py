"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Point en live

hlive = np.array([15])*1e-2 #en cm puis en m
dhlive = np.array([1])*1e-3 #en mm puis en m

mlive = np.array([20])*1e-3 #en g puis en kg
dmlive = np.array([1])*1e-3 #en g puis en kg

Tlive = np.array([17.5]) #en sec
dTlive = np.array([0.2]) #en sec

### Données
L = 150e-2
dL = 1e-2
h_P0=6.1e-2
rho=997
g=9.81
D=(5-2*0.9)*1e-3
dD=0.005*D

h=np.array([8.9,10.2,11.4,13.2,14.5,15.4,16.1,17,18,19.5,20.5])*1e-2 #en cm puis en m
dh = np.array([1]*len(h))*1e-3 #en mm puis en m

m=np.array([5,10,10,20,20,20,20,20,20,20,20])*1e-3 #en g puis en kg
dm = np.array([1]*len(m))*1e-3 #en g puis en kg

T=np.array([32.90,25.90,17.09,23.26,18.87,16.58,15.04,13.94,12.36,11.11,10.34]) #en sec
dT=np.array([0.2]*len(T)) #en sec

### Traitements
xdata=h-h_P0
xerrdata=np.sqrt(2) * dh

ydata=m/T/rho
yerrdata=ydata * np.sqrt((dm/m)**2+(dT/T)**2)

xlive = np.array([])
xliverr = np.array([])
if len(hlive)>0:
    xlive=hlive - h_P0
    xliverr=np.sqrt(2) * dhlive

    ylive=mlive/Tlive/rho
    yliverr=ylive * np.sqrt((dmlive/mlive)**2+(dTlive/Tlive)**2)


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

ystr='Débit massique $Q_v$ [m^3/s]'
xstr="Hauteur d'eau [m]"
titlestr='Débit massique en fonction de la différence de pression '
ftsize=18

### Ajustement

def func(x,a,b):
    return  b*(x+a)

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

print("\n"+titlestr)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y =  b (x +a) \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(15,9))
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


print("\nMesure de la viscosité")
eta=np.pi*D**4*rho*g/(128*b*L)
deta =eta * np.sqrt(4*(dD/D)**2+(ub/b)**2 + (dL/L)**2)

print("eta = "+str(eta)+" +- "+str(deta)+" PI")