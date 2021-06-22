import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

from scipy.optimize import minimize_scalar
def linear(x,a,b):
    return a*x+b


plt.close('all')

'''
-----------------------------------------------------------------------------------------------------------------
---------------------------------------MANIP 1 BALANCE ARRACHEMENT------------------------------------------------
------------------------------------------------------------------------------------------------------------------
'''



### Point en live



xlive=np.array([]) # Poids mesuré en live
ylive=np.array([]) # Tension en V mesurée en live


xliverr=xlive
yliverr=np.array([])

#xliverr=[]
#yliverr=[]

### Données

#Grossissement total
yp=39.4
f=100

y=1e-3
d=25e-2
thetap=np.arctan(yp/f)
theta=np.arctan(y/d)

G=thetap/theta

#Grossissement oculaire

yp2=36.75e-2
foeil=100e-2
thetap2=np.arctan(yp2/foeil)
y2=0.9e-2
theta2=np.arctan(y2/d)
Goc = thetap2/theta2

#Grossissement objectif

h=39.4e-2
ab=36.75e-2/9

Gob=h/ab

dimage=0.8e-2
D=90.5e-2
fproj=100e-3

a=fprof*dimage/(D-fproj)

delta=160e-3

foc=250e-3/Goc
h=a*delta/foc #Diamètre du diaphragmme d'ouverture

ON = Gob*np.sin(a/(2*foc)) #Fonctionne avec réseau de 100 à 300 traits / mm

### Incertitudes


xerrdata=dD
yerrdata=dU


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

xstr='Distance entre les prisme (mm) '
ystr='Tension oscillo (V)'
titlestr='Decroissance de londe evanescente'
ftsize=18

### Ajustement

def func(x,B,d):
    return 1/np.sqrt(np.cosh(x/d)**2+B*np.sinh(x/d)**2)

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)
### Récupération paramètres de fit
'''
a,c=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )
'''
### Tracé de la courbe
xfitth=np.linspace(0,25,100)
fitth=func(xfitth,*popt)


plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,marker='o', color='b',mfc='white',ecolor='g',linestyle='',capsize=8,label='Preparation')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,marker='o', markersize=8, color='k',mfc='darkred',ecolor='k',linestyle='',capsize=8,label='Point ajouté')
plt.plot(xfitth,fitth, color='r', linestyle='-',label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


### Extraction des paramètres du capteur

#Delta
print('Valeur de delta extraite')
print(popt[1])
print(np.sqrt(pcov[1,1]))

#A et B
print('Autre valeur du fit')
print(popt[1])
print(np.sqrt(pcov[1,1]))

print(popt[0])
print(np.sqrt(pcov[0,0]))

# Retour à la longueur d'onde
d=popt[1]*1e-3
lamb=2.2e-2

angle=60
n=np.sqrt((1+(lamb/(2*np.pi*d))**2))/np.sin(angle*np.pi/180)

print('n')
print(n)
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
LIRE DOC
# Pour se rassurer commencer avec les grosses masses. Absolument mettre deux résistances de précision de 10 kOhm pour éviter les fluctuations
#Verifier qu'a priori peu voir pas decelable le courant délivré par l'alim.
#Utiliser l'ampli sinon trop petit.



'''

