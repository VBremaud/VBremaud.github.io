import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats

ftsize=18

C0fe2=1e-3
C0fe3=1e-2
V0fe2=40
Uref=197



dV0=0.05
dV=0.1
DC02=0.01*C0fe2
DC03=0.01*C0fe3

### Point en live

Ulive=np.array([400])
Vlive=np.array([0.4])


if len(Ulive)>0:
    Cfe2 = V0fe2*C0fe2/(Vlive+V0fe2)
    Cfe3 = Vlive*C0fe3/(Vlive+V0fe2)

    xlive=np.log(Cfe3/Cfe2)
    ylive=Ulive+Uref
    xliverr=np.array(np.sqrt((dV/Vlive)**2 + (dV0/V0fe2)**2+(DC02/C0fe2)**2 + (DC03/C0fe3)**2))
    yliverr=np.array([0.1])

else:
    xlive=[]
    ylive=[]
    xliverr=np.array([])
    yliverr=np.array([])


### Données



Vol=np.array([0.25,0.5,0.75,1.025,1.25,1.5,2,2.5,3,4]) # Volume Versé
U=np.array([380,394,403,409,412,415,420,424,427,432]) # Tension mesurée

Cfe2 = V0fe2*C0fe2/(Vol+V0fe2)
Cfe3 = Vol*C0fe3/(Vol+V0fe2)

xdata=np.log(Cfe3/Cfe2)
ydata=U+Uref

### Incertitudes

xerrdata=np.array(np.sqrt((dV/Vol)**2 + (dV0/V0fe2)**2+(DC02/C0fe2)**2 + (DC03/C0fe3)**2))
yerrdata=np.array([0.1]*len(U))


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

ystr='$\Delta E$ [mV]'
xstr='$log([Fe^{3+}]/[Fe^{2+})]$ '
titlestr='Tension mesurée en fonction du rapport des concentrations'

### Ajustement

noise=0*np.random.rand(1,len(yfit))


yfit= yfit+ noise
yfit=yfit[0]

def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )
#print("r2 = " + str(r_value**2) )

print('\nSoit E° = '  +str(a/1000) +  ' +- ' + str(ua/1000) + ' V')

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement linéaire ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()