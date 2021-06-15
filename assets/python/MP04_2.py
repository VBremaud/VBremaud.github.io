"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
from scipy.interpolate import interp1d

plt.close('all')

### Point en live

Xlive=np.array([62]) # Position au reglet mesurée en live en mm
dXlive = np.array([2]) #en mm

Tlive = np.array([150]) #en mV
dTlive = np.array([10]) #en mV

### Données
Z=47 # Valeur du 0 mesurée au reglet

# Venir prendre les valeurs dans l'ordre de sorte à faire un debut:fin
#qui a du sens.
x=np.array([100,80,60,45,40,35,30,25,20,15,10,5,0,-10]) #en mm
dx=np.array([2]*len(x)) #en mm

T=np.array([326.4,285,143.5,-12.3,-62.4,-109.8,-145,-189,-220.9,-254,-278.5,-303,-317.5,-323]) #en mV
dT=np.array([10]*len(T)) #en mV

### Traitements
xdata=Z-x #réglage de l'offset avec le reglet
xerrdata=dx

ydata=T
yerrdata=dT

xlive = np.array([])
xliverr = np.array([])

if len(Xlive)>0:
    xlive = Z - Xlive
    xliverr = dXlive

    ylive=Tlive
    yliverr=dTlive


etalon=interp1d(ydata,xdata)
# if len(xliverr) >0 :
#     xerr=np.concatenate((xerrdata,xliverr))
#     yerr=np.concatenate((yerrdata,yliverr))
#
#
# if len(xliverr)== 0 :


### Données fit


debut=0
fin=len(xdata)+1

xfit=xdata[debut:fin]
yfit=ydata[debut:fin]
yerr=yerrdata[debut:fin]
xerr=xerrdata[debut:fin]

# if len(xlive) >0 :
#     xlive=np.array(xlive)
#     ylive=np.array(ylive)
#     xfit=np.concatenate((xdata[debut:fin],xlive))
#     yfit=np.concatenate((ydata[debut:fin],ylive))
#
#
# if len(xlive) == 0 :



### Noms axes et titre

ystr='Tension [mV]'
xstr='Position [mm]'
titlestr='Calibrage capteur de position'
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



### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Etalonnage')
if len(xlive)>0:
    plt.plot([xdata[0],xdata[-1]],[ylive,ylive],'--',c='green',label='Tension mesurée')
    plt.plot([etalon(ylive),etalon(ylive)],[ydata[-1],ylive],'--',c='green',label='Position déduite')
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Position attendue ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


### Extraction des paramètres du capteur

'''
Sensibilité du capteur
'''
s=1/a# Sensibilité en mm/mV
ds=ua/a**2
print("Sensibilité du capteur : "+str(s)+" +- "+str(ds)+" mm/mV")

'''
Resolution du capteur
'''
M=1 # Environ 1 mV decelable au multimetre, ca va dependre du multimetre du coup !
R=s*M #Résolution du capteur

'''
Justesse du capteur

Pourcela, venir mettre un point au hasard. Utiliser la régression linéaire, et comparer ensuite avec le reglet. Faire si le temps et si ca marche sinon pg.
'''

if len(xlive)>0:
    print('\nPosition déduite :' + str(etalon(ylive)[0]) + ' mm')
    print('\nPosition attendue :' + str(xlive[0]) + ' mm')





### Verification hypothèses



### Theorie et branchement

'''
Voir fiche.
'''

### Conseils manips
'''
Materiel:
-3 solenoides avec centre creux  de 250 spires
-1 ampli de courant ?? (a tester on a fait sans dans l'année)
- Circuit détection synchrone avec passe bas Fc=10 Hz environ
-UN GBF
-Un noyau de fer doux pour canaliser les lignes de champs.
-Un reglet pour mesurer la position du noyau.
-Raccorder les bobines selon schéma
-Un multimetre: Un oscilloscope n'est pas un instrument de mesure!



Alimenter 10V, 5kHZ effet capa!
'''












































#%% BALANCE A JAUGE DE CONTRAINTE








'''On veut une resolution en g pas en Volt donc
'''


# En live, venir prendre un point supplémentaire sur la droite. Si ca ne marche pas prendre 3 points rapidement.
# SI le temps le permet venir voir si le capteur marche en venant mesurer la masse d'un stylo prealablement utilisé

##Conseil MANIP

'''
SUIVRE DOCUMENT ASSOCIE MP04.pdf




'''