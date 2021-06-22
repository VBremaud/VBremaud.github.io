"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')



### Point en live

Cal=9# Ce paramètre permet de prendre en compte correctement l'origine des angles.

anglelive = (np.array([17])+Cal)*np.pi/180 #angle en degré puis en rad
dAlive = np.array([1])*np.pi/180

P0live = np.array([50e-6])
dP0live = np.array([0.5e-6])

Ulive = np.array([-137])*-(1e-3)
dUlive = np.array([0.1e-3])


### Données

angle=(np.array([354,359,4,9,14,19,24,29,34,39,44,49,54,59,64,69,74,79,84])+Cal)*np.pi/180

P0=51e-6# La puissance mesurée en entrée pour le maximum de signal grâce à un puissance metre optique.
dP0=0.5e-6

U=-1e-3*np.array([-168,-166,-160,-152,-143,-132,-120,-107,-92.5,-78.5,-65,-51.5,-39.5,-28.5,-20.5,-14.5,-9,-6.5,-6.5]) # #Tension sur la resistance de charge mesurée par cursors à l'oscillo. Elle indique le courant délivrée. On la prend dans le cadran bas gauche en XY !!
dU=np.zeros(len(U))+0.1*1e-3 # On neglige le calibre devant la variation

R=9e3
dR=10 # Incertitude sur R (j'ai pris la derniere incrémentation sur la plaquette mais c'est peu etre fort)

### Traitements

I=U/R
dI=I*np.sqrt((dU/U)**2+(dR/R)*2)
P=P0*np.cos(angle)**2
dA=(np.zeros(len(angle))+1)*np.pi/180
dP=P*np.sqrt((dP0/P0)**2+(np.tan(angle)*dA)**2) # FOrmule par propagation des incertitudes.

xdata=P
ydata=I

xerrdata=dP
yerrdata=dI


xlive = np.array([])
xliverr = np.array([])
if len(P0live)>0:
    xlive = P0live*np.cos(anglelive)**2
    xliverr = xlive * np.sqrt((dP0live/P0live)**2+(np.tan(anglelive)*dAlive)**2)

    ylive = Ulive / R
    yliverr = ylive*np.sqrt((dUlive/Ulive)**2+(dR/R)*2)

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

xstr='Puissance optique [W]'
ystr='Intensité [A]'
titlestr='Conversion Puissance optique courant '
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x+b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)
### Récupération paramètres de fit

print("\n"+titlestr)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe
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


### Extraction des paramètres du capteur


'''
Sensibilité en Puissance
Ca donne un ordre de grandeur de ce que l'on doit obtenir!
'''

print('Sensibilite en A/W'+str(a))
print('Incertitude associée'+str(ua))


lbda=633e-9
e=1.6e-19
h=6.62e-34
c=3e8

eta=h*c*a/(lbda*e)
deta=h*c*ua/(lbda*e)
'''
Petit calcul archi classique: eta=(Nombre d'électron produit)/(Nombre de Photon arrivant)

I=dq/dt=Ne*e/dt
Popt=Nph*hc/lambda*dt

Nel/Nph=h*c*I/(Popt*lbda*e)
'''


print('Rendement quantique='+str(eta))
print('Incertitude associee'+str(deta))

'''
Commentaire: valeur complètement raisonnable pour une photodiode classique.

'''


## COnseil Manip

#%% Caracteristique statique de la photodiode: MANIP1


''' Caractéristique statique photodiode'''

'''Principe des mesures
1- Tout d'abord faire le montage et bien comprendre qu'on ne peut pas mesurer simultanément la tension au borne d'une resistance et de la photodiode car probleme de masse. On mesure systematiquement une tension par rapport à une masse. Ecrire le circuit.

Pour info, la cathode d'une photodiode est du coté plat de --<|--(cathode)

2- Dans un premier temps on va tracer la caractéristique de la photodiode. Pour cela on trace I=f(U). U est mesuré immediatement sur la diode et I est mesurée grace à une sonde differentielle sur la resistance. Pour comprendre la caractéristique, il faut parler de point de fonctionnement. C'est le croisement entre la caractéristique de la diode et celui U=E-RI mesuré au borne de la resistance. Cela explique la limitation de la caractéristique en fonction de la resistance choisie. Pour cela utiliser le mode XY de l'oscillo (surtout pas en mode DC).

3- On peut enfin vérifier que dans la zone de la photodiode (quadrant bas gauche), la lumière est proportionnelle au flux lumineux. On peut soit utiliser la loi de Malus avec un polariseur soit prendre un puissancemetre.

#NB: la diode doit cracher environ 600 muW

Après la diode on place deux polariseurs analyseurs et on se place en mode XY
La photodiode est sensible à la lumiere exterieure, il faut prendre dans les mêmes conditions

'''