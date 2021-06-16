"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Point en live


Ilive = np.array([225])*1e-3
dIlive = np.array([25])*1e-3

nlive = np.array([2.5])


### Données
# On va mesurer en relatif.
n=np.array([1,2,3,4,4.5,4,3,2,1,0,-1])#Nombre de Frange mesurée. La photodiode n'est pas une bonne idée car trop de fluctuation. On repere l'apparition d'un anneau noir.
I=np.array([110,193,248,375,588,913,1411,1747,2037,2403,2845])*1e-3 # Intensité mesurée avec un amperemetre avant barreau.
dI = np.array([10,20,30,40,50,60,80,100,120,140,160])*1e-3

H=11712*I # Loi de JBD a prendre plus precisemment.
lamb=650e-9 # Longueur d'onde du laser avec incertitude de 30 nm environ.
dL=lamb/2*n # Une frange correspond à une variation d'un bras du michelson donc un allongement du barreau de lambda/2

L=1 # A la louche 1 m merite detre pris plus precisemment;
ddL = 0.05

# On cherche l'allongement relatif en fonction du champ B.
xdata=H
ydata=dL/L

### Incertitudes


xerrdata=17712*dI
yerrdata=np.array([ddL/L]*len(xdata))*ydata

xlive = np.array([])
xliverr = np.array([])
if len(Ilive)>0:

    xlive=11712*Ilive
    xliverr=11712*dIlive

    ylive=lamb/2*nlive/L
    yliverr=ylive * ddL/L

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

xstr='H champ excitateur [A/m]'
ystr='Allongement relatif [$\Delta L$ / $L$]'
titlestr='Magnétostriction en fonction du champ excitateur'
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x+b

popt, pcov = curve_fit(func, xfit, yfit,sigma=None)
### Récupération paramètres de fit

print("\n"+titlestr)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe
xfitth=np.linspace(0,12,100)
fitth=func(xfitth,*popt)

plt.figure(figsize=(17,9))
xtest = np.linspace(np.min(xdata),np.max(xdata),100)

plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,c='green',fmt='o',label='Point ajouté')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()
