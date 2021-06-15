"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Point en live

mlive = np.array([700])*1e-3 # Masse ajoutée sur le pendule pesant en g
dmlive = np.array([2])*1e-3 #incertitude sur la masse en g

Tlive = np.array([1620])*1e-3 #période du pendule en milliseconde
dTlive = np.array([10])*1e-3 # Incertitude sur la période du pendule en milliseconde, attention N mesures + intervalle.



### Données


'''

Preambule theorique: recalculer la periode du pendule pesant en fonction des differents moments d'inertie
Preambule experimental: Pendule pesant, differente masse, capteur d'angle capacitif/resistif
'''
#I] Pendule pesant vs pendule simple

# 1-(Alimenter le capteur d'angle (resistif ou capacitif))
# 2- Equilibrer le pendule sans dire de connerie
# 3- faire partir d'un angle constant assez petit.
# 4-

m= np.array([52,96,224,491,922])*1e-3 # Masse ajoutée sur le pendule pesant en g
dm = np.array([2]*len(m))*1e-3 #incertitude sur la masse en g

T=np.array([3772,3092,2332,1788,1555])*1e-3 # Periode du pendule en milliseconde
dT = np.array([5]*len(T))*1e-3 # Incertitude sur la période du pendule en milliseconde, attention N mesures + intervalle.

### Traitements
L=43e-2
dL=2e-2
g = 9.81

ydata=g*L*m*T**2/(4*(np.pi)**2)
yerrdata = ydata * np.sqrt((dm/m)**2+2*(dT/T)+(dL/L)**2)

xdata=m
xerrdata=dm

xlive = np.array([])
xliverr = np.array([])
if len(mlive)>0:
    ylive=g*L*mlive*Tlive**2/(4*(np.pi)**2)
    yliverr=ylive * np.sqrt((dmlive/mlive)**2+2*(dTlive/Tlive)+(dL/L)**2)

    xlive=mlive
    xliverr=dmlive

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

ystr='Jtot [kg.m^2]'
xstr='m [kg]'
titlestr="Mesure du moment d'intertie en fonction de la masse ajoutée"
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x+b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

print("\n"+titlestr)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )
print("a_th =  L^2 = "+ str(L**2)+' m^2')

chi2red = np.mean((yfit - func(xfit, *popt))**2/yerr[debut:fin]**2)
print("chi2 = "+ str(chi2red))
print("\nJ0 = "+ str(b) +' +- '+str(ub)+' kg.m^2')

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



