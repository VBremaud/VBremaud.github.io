"""
@Louis Heitz et Vincent Brémaud

"""


import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
def linear(x,a,b):
    return a*x+b


plt.close('all')

'''

CARACTERISATION MCC BOUCLE OUVERTE
AUTHOR: TOM PEYROT


'''


### Point en live


'''

BOUCLE OUVERTE:

On mesure tout d'abord le Gain du système
Pour cela on applique une tension DC, on regarde quand on vainc les frottements puis on mesure le rapport
entre la tension dynamo et la tension DC efficace

'''
Vfrot=2.1
dVf=0.2
VDC=6.47
Vutile=VDC-Vfrot
Vdynamo=1.4
G=Vdynamo/Vutile



xlive=np.array([])
xliverr=np.array([])


ylive=np.array([])
yliverr=np.array([])



### Données

VMot=np.array([6.4,6.6,6.5,6.45])
VUT=VMot-Vfrot
Vdynamo=np.array([1.35,1.41,1.45,1.42])
G=Vdynamo/VUT

xdata=VMot
ydata=G



### Incertitudes



xerrdata=np.sqrt(2)*0.01+np.zeros(len(VUT))
yerrdata=G*np.sqrt(2)*np.sqrt((xerrdata/xdata)**2)


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

ystr='Gain en boucle ouverte '
xstr='Tension de commande moteur'
titlestr='Caracterisation gain en boucle ouverte'
ftsize=18

### Ajustement
'''
def func(x,a,b,c):
    return a*x+b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True,p0=[0,1,0.0008])
'''
### Récupération paramètres de fit
'''
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),npnp..sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )
'''
### Tracé de la courbe

xth=np.linspace(np.min(xdata)-1,np.max(xdata)+1,10)
plt.figure(figsize=(12,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,marker='o', color='b',mfc='white',ecolor='g',linestyle='',capsize=8,label='Preparation')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,marker='o', markersize=8, color='k',mfc='darkred',ecolor='k',linestyle='',capsize=8,label='Point ajouté')
plt.plot(xth,np.zeros(len(xth))+np.mean(ydata), color='r', linestyle='--',label='Moyenne ')
plt.fill_between(xth,np.mean(ydata)-np.std(ydata),np.mean(ydata)+np.std(ydata), color='yellow', alpha=0.5, label='Incertitude Stat')
plt.axhline(y=np.mean(ydata)-np.std(ydata),color='k')
plt.axhline(y=np.mean(ydata)+np.std(ydata),color='k')
plt.title(titlestr,fontsize=ftsize)
plt.xlim([np.min(xdata)-0.1,np.max(xdata)+0.1])
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


## Analyses plus poussées en boucle fermée

'''

Evaluation de la vitesse de reponse et de la stabilité du systeme.
On peut mettre un creneau et voir que plus on augmente le gain plus on est rapide mais on commnce a osciller
toujours rester à 1Hz.


On peut alors mettre une charge en sortie pour montrer que le systeme est asservi.
Mettre un rheostat bleu A une resistance assez faible. Dans l'ideal mesurer le courant. Se mettre en mode ROll
Et voir que qu'en enlevant la charge (un interrupteur serait le bienvenu), la machine revient à sa consigne.

On peu

'''
