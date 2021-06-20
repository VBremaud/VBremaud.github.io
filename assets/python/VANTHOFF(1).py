import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live
c1=0.1
V0=20e-3
R=8.314

Veq_live = np.array([5.05]) *1e-3
dVeq_live = np.array([0.05]) *1e-3 #incertitude sur le volume équivalent
dV0_live = np.array([0.5]) *1e-3

Tlive = np.array([22.3]) +273.15
dTlive = np.array([1])

Klive = c1*Veq_live/V0
dKlive = Klive * np.sqrt((dVeq_live/Veq_live)**2+(dV0_live/V0)**2)


xlive=1/Tlive
ylive=-R*np.log(Klive)

xliverr=(dTlive)/Tlive**2
yliverr=R*dKlive/Klive


### Données

T=np.array([3.6,33,53]) + 273.15

c1 = np.array([0.02,0.1,0.1])
Veq=np.array([14,7.35,13.3])*1e-3
dVeq = np.array([0.1,0.1,0.1])*1e-3
dV0 = np.array([1,1,1])*1e-3

K=c1*Veq/V0
dK=K * np.sqrt((dVeq/Veq)**2+(dV0/V0)**2)


xdata=1/T
ydata=-R*np.log(K)

### Incertitudes

xerrdata=(np.zeros(len(T))+1)/T**2
yerrdata=R*dK/K


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

ystr='-R ln(K) [ J/mol/K ]'
xstr="1/T [1/K]"
titlestr='Verification de la loi de Vant Hoff'

### Ajustement

def func(x,a,b):
    return  a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y =  a + b*x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) +'\n\n')
print("DeltarH = "+ str(b) +" +- "+ str(ub) +" J/mol")
print("DeltarHtab = 22.8 kJ/mol \n")
print("DeltarS = "+ str(-a) +" +- "+ str(ua) +" J/K/mol")
print("DeltarStab = 47.2 J/K/mol \n")

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


## Extraction des parametres thermo

R=8.314
dRH=-a/R

