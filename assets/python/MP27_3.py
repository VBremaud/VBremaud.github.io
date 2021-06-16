"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
def linear(x,a,b):
    return a*x+b


plt.close('all')


### Point en live

R1live=1e4
R2live=2.05e4

dR1live=0.01e4
dR2live=0.01e4

Unlive=1125e-3
Unp1live=6.5
U0live=9
Deltatlive=100e-3

tauplive=-Deltatlive/np.log((Unp1live-U0live)/(Unlive-U0live))

dtauplive=1e-4

xlive=np.array([1/tauplive])
xliverr=xlive*dtauplive/tauplive

ylive=np.array([1+ R2live/R1live])
yliverr=ylive*np.sqrt((dR1live/R1live)**2 + (dR2live/R2live)**2)


### Données
f0=1800
Q=1/3
omega0=2*np.pi*f0
tau=omega0/Q

"""
R1=np.array([0.999,0.999,0.995,0.986,0.899,0.489])*1e4
R2=np.array([2.01,2.10,2.00,2.00,2.00,1.0])*1e4
A=1+R2/R1


Un=np.array([1125,375,1687,1687,1950,700])*1e-3
Unp1=np.array([6.5,5.68,6.06,6.37,8.40,7.5])
U0=np.array([8.43,10.18,8.25,9.31,10.8,9.95])
Deltat=np.array([115.3,2.68,257,11.2,1.8,9.65])*1e-3
taup=-Deltat/np.log((Unp1-U0)/(Un-U0))
"""


#En sortie du filtre de Wien

# R1=np.array([0.899,0.979,0.899,0.489])*1e4
# R2=np.array([1.89,1.99,2.00,1.0])*1e4
# A=1+R2/R1
#
#
# Un=np.array([75,60,102,80])
# Unp1=np.array([251,210,185,212])
# U0=np.array([291,265,308,280])
# Deltat=np.array([2.10,12.9,0.55,4.32])*1e-3
# taup=-Deltat/np.log((Unp1-U0)/(Un-U0))

R1=np.array([0.999,0.999,0.995,0.986,0.899,0.489])*1e4
R2=np.array([2.01,2.10,2.00,2.00,2.00,1.0])*1e4
A=1+R2/R1

dR1=0.01e4
dR2=dR1

Un=np.array([1125,375,1687,1687,1950,700])*1e-3
Unp1=np.array([6.5,5.68,6.06,6.37,8.40,7.5])
U0=np.array([8.43,10.18,8.25,9.31,10.8,9.95])

Deltat=np.array([115.3,2.68,257,11.2,1.8,9.65])*1e-3
taup=-Deltat/np.log((Unp1-U0)/(Un-U0))

dtaup=1e-4

ydata=A
xdata=1/taup
### Incertitudes



yerrdata=ydata*np.sqrt((dR1/R1)**2 + (dR2/R2)**2)
xerrdata=xdata*dtaup/taup


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

ystr='Gain'
xstr=r'$1/\tau_p$ [1/s]'
titlestr='Demarrage des oscillation du pont de Wien'
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x + b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
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


## Estimation de la pente theorique

P1=Q/(omega0*2)
print(P1,2*180*470e-9)
print(a)