# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')



def I_diffraction(x,largeur,offset):
    u=(x-offset)/(largeur/2)
    return np.sinc(u)**2
### Point en live


Imaxlive=0.4
Iminlive=0.398
xpic_max=14e-3
xpic_min=14.4e-3
offset_xpic=14.35e-3


largeur_live=0.0018 #lambda*f/b

blive=-0.0e-3
b0mes=0.17e-3

dI=2E-3

Imaxlive*=1/I_diffraction(xpic_max,largeur_live,offset_xpic)
Iminlive*=1/I_diffraction(xpic_min,largeur_live,offset_xpic)

Clive=(Imaxlive-Iminlive)/(Imaxlive+Iminlive)

xlive=np.array([blive+b0mes])
ylive=np.array([Clive])




xliverr=np.array([1e-5])
yliverr=dI*np.sqrt((1/(Imaxlive-Iminlive))**2 + 1/(Imaxlive+Iminlive)**2)*ylive

xlive=np.array([])
xliverr=np.array([])


### Données

#Imax=np.array([0.212,0.711,0.291,0.432,0.562,0.624])
#Imin=np.array([0.023,0.157,0.240,0.307,0.384,0.557])


#bmes=np.array([0.36,0.45,0.55,0.60,0.7,0.8])*1e-3

# Imax=np.array([0.54,0.719,0.922,0.656,0.769,0.737,0.875,0.605,0.661,0.771,0.837])
# Imin=np.array([0.04,0.129,0.366,0.460,0.660,0.513,0.643,0.516,0.595,0.622,0.655])
#
#
# bmes=np.array([-0.1,-0.05,0,0.05,0.1,0.15,0.20,0.25,0.3,0.35,0.4])*1e-3

def I_diffraction(x,largeur,offset):
    u=(x-offset)/(largeur/2)
    return np.sinc(u)**2

Imax=np.array([0.506,0.787,0.847,0.918,0.866,0.829,0.943,0.651,0.843,0.911])
xpic_max=np.array([14.35,14.31,14.25,14.25,14.34,14.35,14.3,14.28,14.16,14.1])*1e-3
Imin=np.array([0.0867,0.197,0.374,0.714,0.748,0.604,0.691,0.574,0.668,0.725])
xpic_min=np.array([14.44,14.42,14.36,14.39,14.25,14.25,14.2,14.18,14.28,14.21])*1e-3
offset_xpic=np.array([14.35,14.31,14.25,14.25,14.25,14.25,14.2,14.18,14.16,14.1])*1e-3

bmes=np.array([-0.1,-0.05,-0.005,0.05,0.1,0.15,0.2,0.25,0.35,0.4])*1e-3
dI=0.01
db=1e-5
b0mes=0.13e-3

bmes+=b0mes
f=100e-3
ames=0.317*1e-3
lamb=633.5*1e-9
b_young=70e-6
largeur_diffraction=2*lamb*f/b_young

Imax*=1/I_diffraction(xpic_max,largeur_diffraction,offset_xpic)
Imin*=1/I_diffraction(xpic_min,largeur_diffraction,offset_xpic)
C=(Imax-Imin)/(Imax+Imin)




def I_interference(x,a,f,lamb,offset):
    delta=a*(x-offset)/f
    return 1+np.cos(2*np.pi*delta/lamb)



xdata=bmes
ydata=C

### Incertitudes

xerrdata=np.array([db]*len(xdata))
yerrdata=(dI*np.sqrt((1/(Imax-Imin))**2 + 1/(Imax+Imin)**2)*ydata)


if len(xliverr) >0 :
    print('oh')
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

ystr='C'
xstr='b [m]'
titlestr="Contraste en fonction de la largeur de la fente source"
ftsize=18

### Ajustement

def func(x,a,b,b0):
    return b*np.abs(np.sin(a*x)/(a*x))+b0

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True,p0=[13128,1,1e-4])

### Récupération paramètres de fit

a,b,b0=popt
ua,ub,ub0=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1]),np.sqrt(pcov[2,2])
print("y =  beta*sinc(alpha (a*x))  + gamma \nalpha= " + str(a) + "\nbeta = " + str(b) +"\ngamma = " +str(b0))
print("u(alpha) = " + str(ua) + "\nu(beta) = " + str(ub) + "\nu(gamma) = " +str(ub0) )

chi2=np.sum(((func(xfit,*popt))-yfit)**2/(yerr[debut:fin]**2))
chi2r=chi2/len(yfit)

print('\nchi2r = ' + str(chi2r))

### Tracé des courbes

xfitt=np.linspace(np.min(xdata),np.max(xdata),100)
plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Preparation')

if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfitt,func(xfitt,*popt),label='Ajustement ')
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


