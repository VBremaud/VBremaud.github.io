"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')


### Etalonnage de la decroissance
'''
Lors de la mesure simultanée de la pulsation propre et de la pulsation de precession de la partie suivante, il va falloir attendre
une vingtaine de seconde pour pouvoir mesurer la pulsation de precession. Nous estimons en préparation la perte de pulsation propre au cours du temps. Nous constatons une decroissance exponentielle dont nous tirons le parametre tau.

'''

t=np.array([30,60,90,120,150,180,210,240,270,300]) #tps en seconde
dt=np.zeros(len(t))+2 #incertitude de 2 secs
Omegapro1=np.array([522,492,464,435,410,387,366,346,328,310]) #tr / min
dO=np.zeros(len(Omegapro1))+2 #incertitudes de 2 tours / min


xdata=t
ydata=np.log(Omegapro1)

xerrdata=dt
yerrdata=dO/Omegapro1


def func(x,a,b):
    return a*x+b

popt, pcov = curve_fit(func, xdata, ydata,sigma=yerrdata,absolute_sigma=True)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

ystr='ln($\Omega_p$ (tr/min)) []'
xstr='Temps[s]'
titlestr="Mesure de la rotation propre du gyroscope en fonction du temps"
ftsize=18

plt.figure(figsize=(10,9))
xtest = np.linspace(np.min(xdata),np.max(xdata),100)

plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
plt.plot(xtest,func(xtest,*popt),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()

chi2red = np.mean((ydata - func(xdata, *popt))**2/yerrdata**2)
tau=1/a #on tire le tau de décroissance de la vitesse de rotation du gyroscope

print("Décroissance de la vitesse de rotation du gyroscope")
print("tau = "+str(-1/a)+" +- "+str(ua / a**2)+" s")
print("chi2 = "+ str(chi2red))

### Point en live


Omprolive = np.array([530])*360*np.pi/180/60 # On vient mesurer au tachymetre la pulsation (en tours par min)
dOmprolive = np.array([10])*360*np.pi/180/60 #Estimation de l'erreur sur la vitesse de rotation (en tours par min)

Tlive=np.array([20])# Periode mesurée avec la fourche optique en seconde
Tliverr=np.array([0.5])# Incertitude sur la periode (attention deux mesures + division par N périodes, plus de points mieux espacés maintenant)


### Données



omegapro=np.array([685,455,430,300,249])*360*np.pi/180/60 # Pulsation propre mesurée dès la mise en place de la masse au tachymetre.
domegapro = np.array([10]*len(omegapro))*360*np.pi/180/60


Tprec=np.array([24.7,17.1,16.6,11.8,9.5])
dTprec=np.array([0.5]*len(Tprec))

F=np.exp(20/tau)
omegapro=F*omegapro

### Traitements

xdata=1/omegapro
xerrdata=domegapro/omegapro**2

ydata=2*np.pi / Tprec
yerrdata = 2*np.pi*dTprec/Tprec**2


xlive = np.array([])
xliverr = np.array([])
if len(Tlive)>0:
    Omprolive = F*Omprolive

    xlive=1/Omprolive
    xliverr=dOmprolive/(Omprolive**2)

    ylive=2*np.pi/Tlive
    yliverr=2*np.pi*Tliverr/Tlive**2

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

ystr='$\Omega_{prec}$ [rad/s]'
xstr='$1/\Omega_{prope}$ [s/rad]'
titlestr="Mesure du moment d'intertie"
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x+b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

print("\nMesure du moment d'inertie")
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

chi2red = np.mean((yfit - func(xfit, *popt))**2/yerr[debut:fin]**2)
print("chi2 = "+ str(chi2red))

## Retrouve on le bon J ?

'''
Pour cela, il faut se replonger dans la theorie du gyroscope. On retiendra les resultats principaux. Notons phi=prec, thet=Nut et psi=propre

Dans l'approximation gyroscopique, c'est à dire {  psipoint>>phipoint ET I3psipoint>>{I2phipoint, I1thetapoint} alors on peut etablir
une relation entre la pulsation de precession et la pulsation propre: phipoint=mgl/I3psipoint

l=distance de la masse à l'axe de rotation de precession.
I3: moment d'inertie selon son axe principal (le long de l'axe de la tige): 1/2 MR^2
Par symétrie les deux autres moments d'inertie sont égaux et valent: m/4(R^2+h^2/3)

Nous allons ici montrer que l'on retrouve une valeur coherente pour la valeur de I3 et vérifier l'approximation gyroscopique;

NB: Quelques infos dans le JOLIDON sur la theorie et les explications mais pas tres interessant sur l'experience car systeme different.

'''


m=135.8*1e-3# C'est la masse ajoutée pour déséquilibrer le gyroscope et le faire précésser. Il s'agit d'une petite masse percée. qui permet de s'insérer à l'arrière de la grosse masse de 1735g.
dm=1e-3

M=1735*1e-3 # Indiqué sur le plateau de la masse du gyro ENSPARISSACLAY
dM=1e-3

R=12.8*1e-2# Rayon de la masse principale
dR=2e-3

L=20.6e-2 # Distance de m à l'axe de précession.
dL=2e-2

g=9.81
h=2.3e-2 # Epaisseur du cylindre principal de masse 1735g

'''
I} Verification de la valeur du moment d'inertie principal.
'''

J=m*g*L/a
dJ=J*np.sqrt((dL/L)**2+(ua/a)**2)

Jth=M*R**2/2
print("\nDétermination du moment d'inertie avec la pente")
print('J = '+str(J)+' +- '+str(dJ)+' kg.m^2')
print('Jth = '+str(Jth)+' kg.m^2')

'''
Commentaire: La valeur theorique est un peu faible comparée à la valeur extraite par l'experience. On voit tout d'abord que c'est très sensible à deux parametrees; le premier: la distance L et le deuxieme la masse m. On peut donc invoquer un biais au niveau de l'équilibrage qui se traduirait par une masse effective m un peu différente. C'est l'explication le plus probable. D'autres explications liées à des frottements et un Jeff sont possibles egalement.
'''


'''
II] Verification de l'hypothese gyroscopique

'''
omegaprec = ydata
J2=1/4*(M*R**2+h**2/3)

print("\nVérification de l'approximation gyroscopique")
R1=omegapro/omegaprec
R2=Jth*omegapro/(J2*omegaprec)

print('R1='+str(R1)) #doit être très grand devant 1
print('R2='+str(R2)) #doit être très grand devant 1

# On verifie bien l'approximation gyroscopique


