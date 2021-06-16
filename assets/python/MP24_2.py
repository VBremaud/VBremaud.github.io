import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
def linear(x,a,b):
    return a*x+b


plt.close('all')

'''
-----------------------------------------------------------------------------------------------------------------
--------------------------------------BRUIT THERMIQUE------------------------------------------------
------------------------------------------------------------------------------------------------------------------
'''



### Point en live

G0live=6.5/(39*1e-3*5.1/1000)
Rlive=500
MaxDSPlive=-80

dG0live=50
dRlive=1
dDSPlive=1



Veff2live=10**(MaxDSPlive/10)/G0live**2


xlive=np.array([Rlive])
ylive=np.array([Veff2live])


xliverr=np.array([dRlive])
yliverr=ylive*np.sqrt((2*dG0live/G0live)**2 + (np.log(10)/10*dDSPlive)**2)

#xliverr=[]
#yliverr=[]

### Données

G0=6.5/(39*1e-3*5.1/1000)
R=np.array([0,51,100,180,270,390,510,680,820,1000])
MaxDSPlog=np.array([-90.2,-87.4,-85.65,-83.70,-82.27,-80.80,-79.95,-78.80,-78.11,-77])


Veff2=10**(MaxDSPlog/10)/G0**2

dG0=50
dDSP=np.array([2,2,2,2,1,1,1,0.5,0.5,0.5])
dR=np.zeros(len(R))+1

xdata=R
ydata=Veff2
### Incertitudes


xerrdata=dR
yerrdata=ydata*np.sqrt((2*dG0/G0)**2 + (np.log(10)/10*dDSP)**2)


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

xstr=r'R [$\Omega$]'
ystr='$V_{eff}^2$ [$V^2$]'
titlestr='Mesure de bruit thermique'
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
xfitth=np.linspace(0,12,100)
fitth=func(xfitth,*popt)


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


### Extraction de la pente

T=273+22

print(' \n Soit kb =' + str( a/(4*T)) + ' +- ' + str(ua/(4*T)) + ' J/K')
kb=1.38e-23
#
# print('pente theorique')
# print(4*kb*T)
#
#
#
# print('pente obtenue')
# print(a)

### Verification hypothèses

'''
Pas d'hypothèses à vérifier. Il faut discuter absolument du:

-De l'utilisation du pont de Wheatstone (refaire calcul)
-De l'amplificateur
-De la détection synchrone (à voir)
-Des limites du capteur

'''


##% Conseil manip

'''
Lire DOC POLY L3.

Matos: Maquette bruit thermique avec resistances variables
Alim pour la plaquette
GBF et oscillo


Dans un prmeier temps on caracterise l'ampli (on ne regarde pas juste le bruit de resustance)
pour cela on se place sur le calibre GBF. Prendre un oscillo de compete, ca change a priori pas fondamentalement
mais pour le bruit c'est toujours mieux, on prendra DSOX 3014A (il permet de moyenner ca bug sur les petis)
Brancher le GBF sur l'entrée.
IGOR:Pulse de 0.04V, Tpulse=200ns, Periode=20micro, Duree=20 micro
Venir moyenner 100 fois sur l'oscillo et venir lire et moyenner 100 fois sur la macro.
Acquerir le Bode pour une resistance pour regarder quelle est la fréquence max et passer en sinus sur le GBF pour
mesurer les gains à la main.


Pour le Gain, je trouve un gain max à 0.8MHz J'ai verifi& que la DSP etait max à ce niveau.

'''












