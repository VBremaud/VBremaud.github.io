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



#xliverr=[]
#yliverr=[]

### Donnéesxdata=Ir

Lambda0=np.array([0.026424 , 0.0266075, 0.027158 , 0.0284425, 0.030094 , 0.030461 ,0.031562 , 0.0324795])

LambdaG=np.array([3.40,3.40,3.49,3.99,4.1,4.55,5,5.2])*1e-2
#LambdaG=dx

dLambda0=1e-4
dLambdaG=1e-3


xdata=1/Lambda0**2
ydata=1/LambdaG**2


### Incertitudes


xerrdata=2*dLambda0/Lambda0**3
yerrdata=2*dLambdaG/LambdaG**3


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

ystr='$1/\lambda_g^2 $ [1/m2]'
xstr='$1/\lambda_0^2$ [1/m2]'
titlestr='Relation de dispersion dans le guide'
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
'''
Pour plus d'info a ce sujet on se refere au CRVB
Pour l'effet GUNN il y a aussi le docuent de chez ORITEL
'''


aguide=1/(np.sqrt(4*np.abs(b)))
daguide=np.sqrt(1/4)*ub/b**2/(2*np.sqrt(1/np.abs(b)))
print('Largeur du guide= '+str(aguide*100) + ' +- ' + str(daguide*100) + ' cm')

### Verification hypothèses
























