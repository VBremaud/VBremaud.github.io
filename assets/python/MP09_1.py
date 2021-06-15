"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')
ftsize=18

### Point en live

xlentille_contrastelive = np.array([72])*1e-2
Flive = np.array([2.5])



### Données

lambd = 633e-9
f2=50e-3
# D=np.array([])
# y=np.array([])
# b=D-(1/f2-1/y)**(-1)-y

xecran=166e-2
xtrou=9.7e-2

#xlentille_contraste=np.array([82,68.5,60.3,52,46.5,43,40.8])*1e-2
xlentille_contraste=np.array([81,65.5,58.5,54.8,48.5])*1e-2
#xlentille_apparition=np.array([86.5,72.2,63.6,59.3])*1e-2
D=xecran-xtrou
y=xecran - xlentille_contraste
b=D-(1/f2-1/y)**-1-y
#F=np.array([2,3,4,5,6,7,8])
F=np.array([2,3,4,5,6])

xdata=F
ydata=1/b

#xdata=xdata/1000

### Incertitudes

xerrdata=np.array([0]*len(xdata))
yerrdata=np.array([0.02]*len(ydata)) #MC

Ylive = xecran - xlentille_contrastelive
blive = D-(1/f2-1/Ylive)**(-1)-Ylive

xlive = Flive
ylive = 1/blive

xliverr = np.array([0])
yliverr = np.array([0.02]) #MC

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

ystr='$1/b$ [1/m]'
xstr='$\mathcal{F}$'
titlestr="Diffraction de Fresnel"

### Ajustement


def func(x,a,b):
    return a+b*x

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
#plt.axis([0,xdata[-1]*1.05,0,ydata[-1]*1.05])
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()

print("Rayon expérimental du trou = "+str((1/b*lambd)**(1/2))+" +- "+str((ub/b**2*lambd)/(2*(1/b*lambd)**(1/2)))+' m')
#l'ordonnée à l'origine permet de remonter à la distance entre le trou diffractant et le col du faisceau laser, a priori inutile.