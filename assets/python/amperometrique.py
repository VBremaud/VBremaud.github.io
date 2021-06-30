# -*- coding: utf-8 -*-
"""
Created on Wed May  5 21:22:38 2021

@author: Louis Heitz, Vincent Bremaud
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
def affine(x,a,b):
    return a*x+b
plt.close('all')


### Point en live

Vlive=9.5
Ilive=0.05e-3

dVlive=0.05
dIlive=0.005e-3

xlive=np.array([Vlive])
ylive=np.array([Ilive])

xliverr=np.array([dVlive])
yliverr=np.array([dIlive])



### Données



V=np.array([3,4,5,6,7,8,9,10,11,12,13,14,15,17])
I=np.array([0.16,0.13,0.1,0.085,0.06,0.035,0.018,0,-0.0038,-0.008,-0.0115,-0.015,-0.0177,-0.0224])*1e-3


xdata=V
ydata=I

### Incertitudes

xerrdata=np.zeros(len(V))+100e-6
yerrdata=np.zeros(len(I))+1e-6


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

ystr='I [A]'
xstr='V [mL]'
titlestr='Amperométrie à potentiel fixé'
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x + b
deb1=0
fin1=9



popt1, pcov1 = curve_fit(func, xfit[deb1:fin1], yfit[deb1:fin1],sigma=yerr[deb1:fin1],absolute_sigma='True')
popt2, pcov2 = curve_fit(func, xfit[fin1-1:], yfit[fin1-1:],sigma=yerr[fin1-1:],absolute_sigma='True')

### Récupération paramètres de fit


### Tracé de la courbe

plt.figure(figsize=(13,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,marker='o', color='b',mfc='white',ecolor='g',linestyle='',capsize=8,label='Preparation')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,marker='o', markersize=8, color='k',mfc='darkred',ecolor='k',linestyle='',capsize=8,label='Point ajouté')
plt.plot(xfit[deb1:fin1-1],func(xfit[deb1:fin1-1],*popt1), color='r', linestyle='--',label='Ajustement ')
plt.plot(xfit[fin1-2:],func(xfit[fin1-2:],*popt2), color='r', linestyle='--')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
#os.chdir(r'C:\Users\tompe\OneDrive\Documents\PHYSIQUE\DOSSIER_AGREG\LC\LC28_Cin_Electrochi')
plt.savefig('Titrage.pdf')
plt.show()


### Extraction des paramètres


### Verification hypothèses


##% Conseil manip
'''
La manip n'est pas compliqué on fait un dosage des ions Fe2 par Ce4.
On suit par potentiométrie avec 2 électrodes de platine et une électrode ECS avec le potentiostat

Le seul choix à faire est la concentration des solutions de Sel de Mohr et de Cerium. Il faut trouver un compromis:
- Pour avoir un volume équivalent décent (10 mL) (donc une solution de Sel de Mohr pas trop concentrée quand même)
-Pour avoir des paliers de diffusion suffisament haut (sinon courants ridicules et très fluctuants) (bon quand même un peu concentré)
-Pouvoir faire tremper les électrodes

Dans l'experience menée dans ce code on a une solution titrante à 0.05 M et un volume de 5mL de Fe2+ à 0.01 (dans lequel on a ajouté environ 50 mL pour faire tremper les electrodes). Une simulation dozzaqueux d'un titrage potentiométrique donne un volume équivalent de 10 mL, c'est bien ce qu'on obtient.

On (Vous en fait) preconise une solution à 0.1 en sel de Mohr (ne pas faire la dillution) et en prendre 20 mL avec une solution à 0.2 de Cerium.
Cela donnerait un volume équivalent à 10 mL, des paliers conséquents. (On peut ajouter 20 mL d'eau distillée pour faire tremper les électrodes sans changer le volume eq).

PRECAUTION POUR LE TITRAGE AMPERO:

Je préconise de faire la courbe IE lorsqu'il n'y a que le Fer. La fer sur le bon calibre 2mA ou 20 mA pour voir ce qui est le mieux. Probablement 2 mA.
On verifie que tout se passe bien. Normalement on voit l'oxydation du Fe2. On peut alors se placer dans la zone d'intérêt pour un dosage ampérométrique: la zone entre la vague d'oxydation de Fe2 et le mur du solvant. Par consommation de Fe2 on va avoir abaissement du palier jusqu'à l'équivalence ou ca vaudra 0 puis négatif.

Expérimentalement, il faut bien s'assurer que la boite ne fait pas nawak. Pour cela, on se place dans le mode émission de signal. On choisit constante et on coche GBF. On vient verifier avec le voltmetre que la carte envoie bien 1V. Si c'est bien le cas, alors le système fonctionne et il suffit de venir récupérer le courant au voltmètre sur la sortie courant en convertissant selon le calibre choisi. On peut alors commencer le dosage.


'''