'''

@author : Louis Heitz, Vincent Brémaud

'''


import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import scipy.integrate as integrate

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
def func(x,a,b):
    return a*x+b


plt.close('all')



### Point en live

Temp=21
F=100/(100+2*(25-Temp))
dSigma=0.02
dC=3e-3*0.875
lamb_h=34.9*F*10# Le facteur 10 est la conversion mm cm je crois
lamb_a=4.1*F*10


Clive=0.5 # On a donc dilué
Sigmalive=1.000

dclive=dC

Q=(Sigmalive/((lamb_h+lamb_a))**2/(Clive-Sigmalive/((lamb_h+lamb_a))))


N=1000

Qsimlive=np.zeros(N)


for j in range(len(Qsimlive)):
    Sigmsim=Sigmalive+dSigma*np.random.randn()
    Clivesim=Clive+dSigma*np.random.randn()*dclive
    Qsimlive[j]=(Sigmsim/(lamb_h+lamb_a))**2/(Clive-Sigmsim/(lamb_h+lamb_a))



xlive=np.array([Clive])
ylive=np.array([np.mean(Qsimlive)])


xliverr=np.zeros(len(xlive))+dclive
yliverr=np.zeros(len(xlive))+np.std(Qsimlive)

#xliverr=[]
#yliverr=[]

### Données

plt.close('all')
Temp=21
F=100/(100+2*(25-Temp))

lamb_h=34.9*F*10# Le facteur 10 est la conversion mm cm je crois
lamb_a=4.1*F*10

#Ci=np.array([0.875,0.35,0.14,0.056,0.022])#,0.009])
#Sigma=np.array([1.185,0.780,0.471,0.301,0.191])#,0.128])
Ci=np.array([1,0.75,0.25,0.1]) # On a donc dilué
Sigma=np.array([1.389,1.224,0.737,0.45])
dSigma=0.02
dC=3e-3*0.875
dc=np.zeros(len(Ci))+dC

Q=(Sigma/((lamb_h+lamb_a))**2/(Ci-Sigma/((lamb_h+lamb_a))))


N=1000

Qsim=np.zeros(len(Q))
dQsim=np.zeros(len(Q))
Sig=np.zeros(N)
C=np.zeros(N)

for j in range(len(Qsim)):
    Sig=np.zeros(N)
    C=np.zeros(N)
    Qtemp=np.zeros(N)
    for i in range (len(Sig)):
        Sig[i]=Sigma[j]+dSigma*np.random.randn()
        C[i]=Ci[j]+dC*np.random.randn()
    Qtemp=(Sig/(lamb_h+lamb_a))**2/(C-Sig/(lamb_h+lamb_a))
    Qsim[j]=np.mean(Qtemp)
    dQsim[j]=np.std(Qtemp)


xdata=Ci
ydata=Qsim

### Incertitudes


xerrdata=dc# N.B l'incertyitude semble augmenter mais l'incertitude relative elle dominue bien. Donc OK.
yerrdata=dQsim


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

xstr='Concentration en acide acétique (mol/L) '
ystr='Quotient réactionnel'
titlestr="Détermination du Ka de l'acide acétique"
ftsize=18

### Ajustement

# def func(x,a):
#     return a
#
# popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)
#
# ### Récupération paramètres de fit
#
# a=popt
# ua=np.sqrt(pcov[0,0])



### Tracé de la courbe
xfitth=np.linspace(np.min(xdata),np.max(xdata),100)
#fitth=func(xfitth,*popt)


plt.figure(figsize=(13,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.axhline(y=10**(-4.8),linestyle='--',label='Valeur attendue')
plt.plot(xdata,[np.average(yfit)]*len(xdata),label='Valeur obtenue')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.ylim([1.2e-5,2e-5])
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()

Ka=np.average(yfit)
uKa=np.std(yfit)/np.sqrt(len(yfit))
pKa=-np.log10(np.average(yfit))
upKa=pKa*uKa/Ka
print('\nSoit Ka = ' + str(Ka) + ' +- ' + str(uKa))
print('pKa= ' + str(pKa) + ' +- '+ str(upKa ))

## Determination de la pente



