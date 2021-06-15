"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Point en live


Dmlive = np.array([25])/180*np.pi #en degré puis rad
dDmlive = np.array([0.1])/180 *np.pi #incertitude gonio à vérifier, penser à mesurer 2 Dm

lambdlive = np.array([500])*1e-9 #valeur tabulée


### Données
m = 1 #ordre 1 / -1

Dm = np.array([10,20,30])/180*np.pi
dDm = np.array([0.1]*len(Dm))/180 *np.pi

lambd = np.array([200,400,600])*1e-9

### Traitements

xdata=lambd #vitesse
xerrdata=np.array([0]*len(xdata))

ydata=np.sin(Dm/2)

yerrdata = np.zeros(len(ydata))

N=1000
for j in range(len(ydata)):
    DM = np.zeros(N)
    Y = np.zeros(N)
    for i in range(N):
        DM[i]=Dm[j]+dDm[j]*np.random.randn()
        Y[i] = np.sin(DM[i]/2)
    yerrdata[j] = np.std(Y)

xlive = np.array([])
xliverr = np.array([])
if len(Dmlive)>0:

    xlive=lambdlive
    xliverr=np.array([0]*len(xlive))

    ylive=np.sin(Dmlive/2)

    DM = np.zeros(N)
    Y = np.zeros(N)
    for i in range(N):
        DM[i]=Dmlive+dDmlive*np.random.randn()
        Y[i] = np.sin(DM[i]/2)
    yliverr = np.array([np.std(Y)])

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

ystr='sin($D_m$/2) '
xstr='$\lambda$ [m]'
titlestr='Détermination du nombre de pas du réseau'
ftsize=18

### Ajustement

def func(x,a,b):
    return a+ b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

print("\n"+titlestr)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a + b x \na = " + str(a) + "\nb = " + str(b))
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

print("\nPas du réseau")
print("a = "+str((2*b)/m/1000)+" +- "+str(ub/b*(2*b)/m/1000)+" traits/mm")