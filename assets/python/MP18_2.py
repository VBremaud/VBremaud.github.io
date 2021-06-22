"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Point en live

Blive = np.array([0.13])
dBlive = np.array([0.002])

Ulive = -np.array([-11])*1e-3
dUlive = np.array([0.05])*1e-3


### Données
e0=(33.68+32)*1e-3 # C'est la valeur la plus grande(e=0) on prendra la valeur absolu de la difference ensuite
de=0.2
de0=np.sqrt(2)*de*1e-3
e=(28.99+28.97)*1e-3
efixe=np.abs(e-e0)

B1=np.array([114,174,212,276,348,427,475,526,575,658])
dB1=np.zeros(len(B1))+10e-3
UH1=np.array([15,27,34.5,46.8,60.4,75,84,92.8,101.9,117])*1e-3 # Pour Ih=20mA
dUH1=np.zeros(len(UH1))+0.1e-3


B2=np.array([173,243,315,386,457,532,620])
dB2=np.zeros(len(B2))+10e-3
UH2=np.array([54.2,81.5,110,137,163,191,223])*1e-3 # Pour Ih=20mA
dUH2=np.zeros(len(UH2))+0.1e-3

B=np.array([0.033,0.062,0.1,0.160,0.225,0.280,0.355,0.425,0.478,0.525,0.640,0.703,0.785,0.827,0.860]) #en T
dB=0.002 #Entre 510 et 540 pour 525

dU=0.05*1e-3
UH=-np.array([9.84,3.58,-4.55,-17.5,-31.4,-43.0,-58.6,-72.7,-83.5,-92.8,-116.1,-128.5,-144,-152.3,-158.8])*1e-3

xdata=B
ydata=UH


### Incertitudes

xdata=B
xerrdata=np.array([dB]*len(xdata))

ydata=UH
yerrdata=np.array([dU]*len(ydata))

xlive = np.array([])
xliverr = np.array([])
if len(Blive)>0:
    xlive=Blive
    xliverr=dBlive

    ylive=Ulive
    yliverr=dUlive

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

ystr='UH [V]'
xstr='B [T]'
titlestr='Tension de Hall en fonction du champ magnétique'
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x + b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

print("\n"+titlestr)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé des courbes

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

### Extraction des paramètres

'''
En tracant B=f(I) on s'attend à une pente de muON/e

''' # Pente theorique attendue
I=20e-3
e=1.6e-19
b_geo=1e-3
n=I/(e*a*b_geo) # Pente experimentale

un=n*ua/a


print('Soit n=' + str(n) + ' +- '+ str(un) + ' 1/m3')

'''
Ca marche du feu de diou ! En fait à 20% commentaire. On a pas un circuit filiforme. On a pas un milieu lineaire. On n'essaie pas de faire coller à ce modele à tout prix!
'''
### Conseil manip

'''
Venir prendre l'életroaimant ENSC508
Sonde a effet Hall ENSC 474.4 avec gaussmetre (c'est quoi ? )
Puissancemegtre GPM 8213 pour mesurer le courant en entrée.
Alim Autotransfo+Sortie redressée, filtrée, non régulée. 100V,5A : COURANT CONTINU!!!
Pied a coulisse.
Pour mesurer e au pied à coulisse prendre ce qui dépasse de l'autre côté du pied a coulisse. Partir de e nul. et mesurer de chaque côté.

Le CHIP Sonde a effet Hall qui permet de modifier le courant de Hall est: Plaquette semi-conductrice  PHYWE de L3 (dopée n (celle choisie ici) ou dopée p) + son support de lecture
"maison" + alimentation 12 V de lampe blanche (on alimente le support avec ça...)
Les cables sont cruciaux (coudées ou non) pour venir introduir le chip dans l'entrefer. On vient aussi y placer une sonde.
A l'arriere bouton pour afficher soit I soit T. COurant Hall changeable egalement.


REGLER A CHAMP NUL la tension de HALL pour quelle soit nulle. En fait, les soudures n'étant pas exactement au même endroit, il y a evidemment une difference de tension RI sur la portion considéréed.
'''






































