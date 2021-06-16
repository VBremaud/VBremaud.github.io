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


### Point en live



xlive=np.array([10])
xliverr=np.array([0.01])


ylive=np.array([1.85])*1000/6
yliverr=np.array([0.01])*1000/6



### Données

'''

BOUCLE OUVERTE:

On mesure tout d'abord le Gain du système
Pour cela on applique une tension DC, on regarde quand on vainc les frottements puis on mesure le rapport
entre la tension dynamo et la tension DC efficace

'''
Vfrot=2.1 # Attention!!!!!! SUR le moteur pas sur la consigne!
dVf=0.2
VDC=6.47 # Sur le moteur putain
Vutile=VDC-Vfrot
Vdynamo=1.4
G=Vdynamo/Vutile
print(G)


'''
BOUCLE FERMEE

On va appliquer une tension de consigne continue (DC) et on va regarder jusqu'à quand le moteur peut suivre, c'est à dire l'image de la vitesse de rotation à saturation en fonction de la tension mise sur le hacheur en entrée.

Pour avoir une courbe de comparaison (theorique), On regarde la tension envoyée sur le moteur (la tension qui sort du hacheur et qui va vers le moteur). Le hacheur va fournir alpha*E. Lorsque alpha=1, il ne peut plus augmenter et on devrait fournir Ehacheur. Simplement il existe deux pertes: l'une dans le Hacheur (de 1.8V) ce qui implique de prendre E moteur et une par frottement donc la tension max sur la dynamo est Satth=(EMoteur-Vfrot)*G



Cette manip permet de montrer qu'on a bien compris: La grandeur asservie est la tension image de la rotation. C'est donc la tension isue de la dynamo. Cette tension doit être la même de celle donnée en consigne, i.e celle délivrée par le GBF car le correcteur s'applique à que la différence soit nulle entre les deux grandeurs. En pratique, bien que l'entrée du hacheur indique [0,10V] il peut prendre 12V en entrée. Il existe donc une façon très rapide de voir quand le système sature, ce sera lorsquee cette tension atteint 12V. On peut donc mettre un multimètre en entrée de consigne=sortie de comparateur avec un T. On trace alors la vitesse limite à laquelle on peut asservir (image de la vitesse donc tension mesurée par la dynamo corrigée) en fonction de la tension d'alim.


Cette valeur peut être retrouvée théoriquement. La tension maximale utile que l'on peut obtenir est la tension fournie au moteur à saturation à laquelle on retranche les pertes et on vient multiplier par le gain moteur/dynamo.
'''


Ehacheur=np.array([5,10,15,20,25])
EMoteur=np.array([3.3,8,12.68,16.95,21.71])# C'est la valeur obtenue en saturation.
Sat=np.array([0.380,1.85,3.34,4.72,6.29])*1000/6 # C'est la valeur commune obtenue sur la consigne et en sortie de dynamo. A corriger si la dynamo est differente


Satth=(EMoteur-Vfrot)*G*1000/6


xdata=Ehacheur
ydata=Sat
### Incertitudes



xerrdata=0.01*Ehacheur
yerrdata=np.zeros(len(Sat))+0.01*1000/6


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

ystr='Vitesse limite dasservissement [Tr/min] '
xstr='Ehacheur [V]'
titlestr="Etude de la plage d'asservissement"
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x+b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe


xth=np.linspace(np.min(xfit),np.max(xfit),10)
plt.figure(figsize=(10,9))

plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o', label='Preparation')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,fmt='o',label='Point ajouté')
plt.plot(xth,func(xth,*popt),label='Ajustement ')
plt.plot(xdata,Satth, color='k', marker='',markersize=13,linestyle='--', mfc='grey',label='Origine Saturation',zorder=1)
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


## Analyses plus poussées en boucle fermée

'''

On peut alors mettre une charge en sortie pour montrer que le systeme est asservi.
Mettre un rheostat bleu A une resistance assez faible. Dans l'ideal mesurer le courant. Se mettre en mode ROll
Et voir que qu'en enlevant la charge (un interrupteur serait le bienvenu), la machine revient à sa consigne.

On peu

'''
