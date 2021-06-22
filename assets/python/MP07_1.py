'''

@author: Louis Heitz, Vincent Brémaud

'''

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def linear(x,a,b):
    return a*x+b

def expo(x,a,b):
    return a*np.exp(20000*b/x)
def poly(x,a,b,c):
    return a*x**2+b*x+c


import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
def linear(x,a,b):
    return a*x+b


plt.close('all')


### Point en live

Lambda0live=0.027
LambdaGlive=3.70e-2

dLambda0live=0.001
dLambdaGlive=0.002

xlive=np.array([1/Lambda0live**2])
ylive=np.array([1/LambdaGlive**2])

xliverr=np.array([2*dLambda0live/Lambda0live**3])
yliverr=np.array([2*dLambdaGlive/LambdaGlive**3])


xlive=[]
xliverr=[]
#yliverr=[]

### Données

foc1=10e-2

foc2=np.array([15e-2,25e-2,50e-2,75e-2])

dfoc2=0.05e-2+np.zeros(len(foc2))


G=np.array([1.55,2.45,4.9,7.5])

dG=0.01+np.zeros(len(G))

xdata=foc2
ydata=G


### Incertitudes


xerrdata=dfoc2
yerrdata=dG


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

ystr='$G$ [1]'
xstr="$f'_2$ [m]"
titlestr='Grandissement du système optique'
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


### Extraction du parametre de guide


print('\nSoit f1= '+str(100/a) + ' +- ' + str(100*ua/a**2) + ' cm')

### Verification hypothèses