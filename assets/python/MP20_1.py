"""
@Louis Heitz et Vincent Brémaud

"""


import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live

flive=800
Velive=100*1e-3
Vslive=350*1e-3

dflive=1
dVelive=1e-3
dVslive=1e-3

xlive=np.array([(2*np.pi*flive)**2])
ylive=np.array([(Vslive/Velive)**2])
xliverr=np.array([8*np.pi**2*flive*dflive])
yliverr=ylive*np.sqrt((2*dVelive/Velive)**2 + (2*dVslive/Vslive)**2)

### Données

R=100
omega=2*np.pi*np.array([100,200,300,500,1000,1500,2000,3000,4000,5000,6000,7000,10000])
Ve=np.array([101.2,101.3,101.2,101.3,101.27,101.3,101.3,101.3,101.5,101.5,101.5,101.5,101.4])*1e-3
Vs=np.array([307,314,318,339,420,530,656,923,1210,1510,1830,2150,3190])*1e-3

domega=2*np.pi+np.zeros(len(omega))
dVe=1e-3+np.zeros(len(Ve))
dVs=1e-3+np.zeros(len(Vs))


xdata=omega**2
ydata=(Vs/Ve)**2


### Incertitudes

xerrdata=np.array([0.2]*len(xdata))

yerrdata=np.array([0.2]*len(ydata))



### Données fit


debut=0
fin=len(xdata)-1

if len(xlive) >0 :
    xlive=np.array(xlive)
    ylive=np.array(ylive)
    xfit=np.concatenate((xdata[debut:fin],xlive))
    yfit=np.concatenate((ydata[debut:fin],ylive))


if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata[debut:fin],xliverr))
    yerr=np.concatenate((yerrdata[debut:fin],yliverr))


if len(xliverr)== 0 :
    xerr=xerrdata
    yerr=yerrdata

if len(xlive) == 0 :
    xfit=xdata[debut:fin]
    yfit=ydata[debut:fin]


### Noms axes et titre

ystr=r'$V_s^2/V_e^2$ '
xstr='$\omega^2$ [rad^2/s^2]'
titlestr='Détermination de L'

### Ajustement

def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr,absolute_sigma=True)


### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

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


###Extraction paramètres
#Us^2/Ue^2= (r/R)^2 + L^2 omega^2 / R^2


# A haute fréquence : comportement capacitif !!

r=R*np.sqrt(a)
L=R*np.sqrt(b)
ur=r*0.5*ua/a
uL=L*0.5*ub/b
print('\nSoit r = ' + str(r) + ' +- ' + str(ur) + ' Ohm')
print('\nEt L = ' + str(L) + ' +- ' + str(uL) + ' H')








