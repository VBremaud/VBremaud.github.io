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

pos_vernierlive = np.array([10.925])
largeur_diffraction_live = np.array([1.6])

pos_vernierlive*=1e-3
largeur_diffraction_live*=0.5e-3

### Données

lamb=650e-9
f2=500e-3
offset_vernier=10.55e-3


position_vernier=np.array([10.85,10.90,10.95,11]) #vernier 11.05
largeur_diffraction=np.array([1.96,1.74,1.52,1.36]) #largeur diffraction 1.33

ver_err=0.005e-3
diff_err=0.01e-3

position_vernier*=1e-3
largeur_diffraction*=0.5e-3

xdata=(position_vernier-offset_vernier)/lamb
ydata=f2/largeur_diffraction

#xdata=xdata/1000

### Incertitudes

xerrdata=np.array([ver_err/lamb]*len(xdata))
yerrdata=np.array(f2*diff_err/largeur_diffraction**2)

xlive = (pos_vernierlive-offset_vernier)/lamb
ylive = f2/largeur_diffraction_live

xliverr = np.array([ver_err/lamb]*len(xlive))
yliverr = np.array(f2*diff_err/largeur_diffraction_live**2)

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

ystr='f/deltax'
xstr='b/lambda'
titlestr="Diffraction par une fente"

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

print("On trouve une pente de "+str(b)+" +- "+str(ub)+", pour une pente théorique de 1")