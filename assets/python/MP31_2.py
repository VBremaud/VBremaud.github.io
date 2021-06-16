import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
def linear(x,a,b):
    return a*x+b


plt.close('all')

"""
@Louis Heitz et Vincent Brémaud

"""

### Point en live

flive=217.5
Ulive=12.5

dflive=0.02
dUlive=1

xlive=np.array([flive])
ylive=np.array([Ulive])


xliverr=np.array([dflive])
yliverr=np.array([dUlive])



### Données



f=np.array([217,218,219,219.5,220,220.5,221,220.3,219.7,219.8,219.9,220.1,220.2,220.15,220.17,220.14,220.13])

U=np.array([12,13,27,39,172,68,31,140,59,76,103,529,365,909,630,985,949])
dU=(np.zeros(len(U))+5)/np.max(U)

ylive=ylive/max(U)
yliverr=yliverr/max(U)
U=U/np.max(U) #Pour normaliser



xdata=f
ydata=U
### Incertitudes

df=np.zeros(len(f))+0.02


xerrdata=df
yerrdata=dU


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

xstr='$f$ [Hz]'
ystr='$U/U_0$ '
titlestr="Tension du micro (normalisée) en fonction de la fréquence d'excitation"
ftsize=18

### Ajustement



def func(x,Q,x0):
    return 1/np.sqrt(Q**2*(1-(x/x0)**2)**2+(x/x0)**2)


popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True,p0=[5000,220],maxfev=2000)
#print(popt)
### Récupération paramètres de fit
'''
a,c=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )
'''
### Tracé de la courbe

xfit2=np.linspace(np.min(xdata),np.max(xdata),1000)
yfit2=func(xfit2,*popt)
#ytest=func(xfit2,2000,220)

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
#plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,marker='o', color='b',mfc='white',ecolor='g',linestyle='',capsize=8,label='Preparation')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit2,yfit2, label='Ajustement ')
#plt.plot(xfit2,ytest)
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


