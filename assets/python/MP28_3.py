"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
def affine(x,a,b):
    return a*x+b
plt.close('all')

'''
RESONNANCE PARAMETRIQUE 1
AUTHOR: TOM PEYROT


'''



'''

Idée générale de cette dernière manip.
Montrer que l'on peut, à partir du principe de résonance parametrique (faire evoluer un parametre du circuit sinusoid), générer une fréquence moitie de la fréquence excitatrice. C'est fou quand même. NB: en optique non linéaire on génere une fréquence double, c'est l'inverse d'ici.

Composants [Jolidon]: R=30 Ohm, L=40 mH, C=1muF, cela doit générer une circuit RLC de fréquence de resonance 750 Hz, Q=6.6, et le multiplieur possede un gain k=0.1

Première chose à vérifier donc: on excite avec une fréquence double du système et on recupere la fréquence du filtre à peu pres car il existe plage capture donc fe/2 en pratique qui se rapproche de f0. Pour aller un petit peu plus loin, on peut montrer par la theorie que le multiplieur induit un phenomene non lineaire: on peut normalement observer une harmonique à 3fe/2 soit 3f0 dont l'amplitude RELATIVE doit valoir k*Ve/16.
Si on prend comme dans le Jolidon Ve=3.5V, k=0.1, on doit trouver une valeur de 0.02 pour l'amplitude RELATIVE. C'est ce que l'on vient vérifier ensuite. Parler des parametres de TFs etc..

Finalement, on vient verifier la relation de la bande de resonance en fonction de la tension excitatrice.

'''


## Verification du Ratio

'''

Comparaison initial de la hauteur de la hauteur des pics en exciutant à fe ils sont à fe/2 et 3*fe/2
'''

h1=176 #hauteur du premier pic
dh1=1
h2=3.6 #hauteur du second pic
dh2=0.2

R=h2/h1
dR=R*np.sqrt((dh1/h1)**2+(dh2/h2)**2)
print('Ratio mesuré='+str(R))
print('Incertitude associee='+str(dR))


k=0.1
Ve=7/2

R2=k*Ve/16
print('Ratio attendu= '+str(R2)+ '\n')  # Il pourrait être habile de verifier k et d'y mettre incertitude.


### Point en live


Velive=8
dFelive=670

uVelive=0.1
udFelive=5

xlive=np.array([Velive**2])
ylive=np.array([dFelive**2])

xliverr=np.array([2*uVelive*Velive])
yliverr=np.array([2*udFelive*dFelive])

#xliverr=[]
#yliverr=[]

### Données


Ve=np.array([20,17,14,11,8])/2 # Amplitude (Vpp/2)
dFe=np.array([2160-1332,2099-1395,2034-1465,1964-1541,1883-1625])

uVe=np.array([0.1]*len(Ve))
udFe=np.array([5]*len(dFe))
xdata=Ve**2
ydata=dFe**2

### Incertitudes

xerrdata=2*uVe*Ve
yerrdata=2*udFe*dFe


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

ystr='$\Delta f^2$ [Hz$^2$]'
xstr='$V_e^2$ [V$^2$]'
titlestr='Largeur de résonance en fonction de Ve'
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x + b

def func2(x,a,b):
    return a*x**2+b*x+c # Si desaccord, suivre Jolidon pour mettre en place un fit d'ordre 2.

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma='True')

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(12,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Preparation')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,*popt),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


### Extraction des paramètres

f0=750
ath=(k*f0)**2

print('\npente theorique attendue= '+ str(ath) +  ' Hz^2 / V^2')
print('Pente experimentale obtenue= '+str(a)+  ' +- ' + str(ua)  + ' Hz^2 / V^2')

# Resultats pas aberrants mais a ajuster avec la vraie valeur obtenue+ commentares p446 Jolidon si ca marche pas bien


Q=6.59
bth=-(2*f0/Q)**2

print('\nordonnee theorique attendue= '+str(bth)+  ' Hz^2 / V^2')
print('ordonnee experimentale obtenue= '+str(b) + ' +- ' + str(ub) + ' Hz^2')

# Memes commentaires