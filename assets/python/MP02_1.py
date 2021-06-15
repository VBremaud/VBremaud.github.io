"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Point en live

majoutlive = np.array([0.15]) #en g
dmajoutlive = np.array([0.01]) #en g

Ulive = np.array([0.75]) #en V
dUlive = np.array([0.01]) #en V

### Données

m_balance=0.35 #en g

g=9.81
majout=np.array([0,0.1,0.2,0.4,0.5]) #en g
dmajout=np.array([0.01]*len(majout)) #en g, à vérifier

U=np.array([0.542,0.695,0.854,1.16,1.33]) #en V
ddU=np.array([0.542,0.695,0.854,1.16,1.33])/100 #en V, à vérifier


### Traitements

m_balance=0.35
g=9.81
masse=majout+m_balance

xdata=g*masse*1e-3 #en N
xerrdata=g*dmajout*1e-3 #en N

ydata=U
yerrdata=ddU

xlive = np.array([])
xliverr = np.array([])
if len(majoutlive)>0:
    xlive=g*(majoutlive+m_balance)*1e-3
    xliverr=g*dmajoutlive*1e-3

    ylive=Ulive
    yliverr=dUlive

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

ystr='$U$ [V] '
xstr='$mg$ [N]'
titlestr="Etalonnage de la balance d'arrachement"
ftsize=18

### Ajustement

def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

print("\nEtalonnage de la balance")
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
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

### Mesure de la tension de surface
print("\nMesure de la tension de surface de ...") #à compléter

#Avec l'anneau
R=(18.62+19.61)*1e-3/4 #rayon moyen
dR=1e-3
#dU=445e-3 #433 c'est ok  pour ethanol, variation de la tension
dU=1.18 # pour l'eau, varation de la tension
L=4*np.pi*R #périmètre de l'anneau x 2

gamma=dU/(b*L)
dgamma=gamma*np.sqrt((dR/R)**2+(ub/b)**2)

print("gamma (anneau) = "+str(gamma)+" +- "+str(dgamma)+" N/m")

#Avec la lame
dU=145e-3
L=2*19.75e-3
dL=1e-3

gamma=dU/(b*L)
dgamma=gamma*np.sqrt((dL/L)**2+(ub/b)**2)

print("gamma (lame) = "+str(gamma)+" +- "+str(dgamma)+" N/m")