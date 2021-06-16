import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

# Données pour le rendement :

# ΔrH° = - 1368 kJ mol-1.
# M_eth = 46 g/mol
# rendement = Putile/Pchimique
# Putile = W / T = intégrale pdV / Tcycle
# Pchimique = meth/Meth * ΔrH° /(T_total)
### Point en live

xlive=[]
ylive=[]

#xlive=[]
#ylive=[]

xliverr=np.array([])
yliverr=np.array([])

#xliverr=[]
#yliverr=[]

### Données

Patm=1.013

#En supression
V01=20
Vol1=np.array([20,19,18,17,16,15,14,13])
Uosc1=np.array([2.66,2.88,3.08,3.36,3.67,3.98,4.42,4.79])
dP1=Patm*(V01/Vol1-1)

#En dépression
V02=15
Vol2=np.array([15,16,17,18,19,20])
Uosc2=np.array([2.70,2.40,2.18,1.95,1.77,1.62])
dP2=Patm*(V02/Vol2-1)

dP=np.concatenate((dP2,dP1))
U=np.concatenate((Uosc2,Uosc1))
# U=np.array([0.15,0.57,0.85,1,1.1,1.86,2.25,2.8,2.5,3.18,])
# I=np.array([16,218,350,330,515,1880,2450,3500,3160,4120])*1e-3

ydata=U
xdata=dP



### Incertitudes


xerrdata=np.array([0.01]*len(xdata))
yerrdata=np.array([0.05]*len(ydata))


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

ystr='$\Delta P$ [Pa]'
xstr='$U$ [V]'
titlestr="Etalonnage du capteur de pression"

### Ajustement

def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',markersize=4,label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
#plt.axis([0,3.600,0,5])
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()