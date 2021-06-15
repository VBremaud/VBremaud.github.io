"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

ftsize=18


'''
Brancher les thermocouple type T sur chaque branchement du module picolog des thermocouple (le truc bleu)
Connecter ce module en USB à l'ordi
Allumer le module de visualisation courant qui active les ventilos sur les pelletiers situés aux extremités du tube (permet d'avoir une surface chaude et une surface froide)
Tension : 500mV offset et 500 mV d'amplitude [il faut aller de 0 à 1V] et 3 mHz
Allumer le picolog
Acquerir la température en fonction du temps.


Equilibre thermique atteint en 1h30 environ.

'''
#Affichage si True
graphe1 = True #lambda avec la phase, tracé de omega t en fonction de x
graphe2 = True #lambda avec l'amplitude, tracé de log(A) en fonction de x
graphe3 = True #variation de la température moyenne le long du barreau pour vérifier la présence de pertes thermiques ou non

### Points en live

# Les differents numeros sont les differents capteurs

t1min = np.array([26,])#min.sec
t1s = np.array([37,])#min.sec
dt1= 5# seconde

t2min = np.array([27,])#min.sec
t2s = np.array([25,])#min.sec
dt2=5

t3min = np.array([28,])#min.sec
t3s = np.array([10,])#min.sec
dt3=5

t4min = np.array([29,])#min.sec
t4s = np.array([2,])#min.sec
dt4=5

t5min = np.array([29,])#min.sec
t5s = np.array([52,])#min.sec
dt5=5

t6min = np.array([30,])#min.sec
t6s = np.array([26,])#min.sec
dt6=10


### Données

omega=2*np.pi*3e-3
t1=t1min*60+t1s
t2=t2min*60+t2s
t3=t3min*60+t3s
t4=t4min*60+t4s
t5=t5min*60+t5s
t6=t6min*60+t6s

A1 = np.array([36.02-32])
A2 = np.array([33.25-31.51])
A3 = np.array([30.81-30.11])
A4 = np.array([28.36-28.09])
A5 = np.array([27.58-27.44])
A6 = np.array([26.52-26.47])
dA= np.sqrt(2)*0.02

A_moy=np.array([(32+36.02)/2,(33.25+31.51)/2,(30.81+30.11)/2,(28.36+28.09)/2,(27.58+27.44)/2,(26.52+26.47)/2])

A=np.concatenate([A1,A2,A3,A4,A5,A6])
T=np.concatenate([t1,t2,t3,t4,t5,t6])

X=23e-3+np.array([0,1,2,3,4,5])*94e-3

### Incertitudes

dt = np.array([dt1,dt2,dt3,dt4,dt5,dt6])
da = np.array([dA]*len(A))
dx = np.array([2e-3] * len(X))
da_moy = np.array([2e-2]*len(A))

if graphe1:

    ### Données fit

    xdata = X
    ydata = omega * T

    debut=0
    fin=len(xdata)+1

    xfit = X
    xerrdata = dx
    xerr = xerrdata

    yfit = omega * T
    yerrdata = omega * dt
    yerr = yerrdata

    ### Noms axes et titre

    ystr='omega x t [phase]'
    xstr='Distance au module Peltier [m]'
    titlestr='Omega x t en fonction de la distance'

    ### Ajustement

    def func(x,a,b):
        return a + b*x

    popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

    ### Récupération paramètres de fit

    a,b=popt
    ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

    ### Affichage résultats sur l'invite de commande

    print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
    print("ua = " + str(ua) + "\nub = " + str(ub) )
    print ("On trouve en suivant la phase, delta = ", 1/b, "m, avec une incertitude ", ub / b**2, "m")
    print("On trouve en suivant la phase, lambda =", 8.96e3*380*omega*(1/b)**2/2, "W/m/K, avec une incertitude ", (ub / b**2) * (b) * np.sqrt(2) *8.96e3*380*omega*(-1/b)**2/2, "W/m/K")


    ### Tracé de la courbe

    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
    plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()


if graphe2:

    ### Données fit

    xdata = X
    ydata = np.log(A)

    debut=0
    fin=len(xdata)+1

    xfit = X
    xerrdata = dx
    xerr = xerrdata

    yfit = np.log(A)
    yerrdata = da / A
    yerr = yerrdata

    ### Noms axes et titre

    ystr='log(Amplitude) [log(m)]'
    xstr='Distance au module Peltier [m]'
    titlestr='Amplitude en fonction de la distance au module Peltier'

    ### Ajustement

    def func(x,a,b):
        return a + b*x

    popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

    ### Récupération paramètres de fit

    a,b=popt
    ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

    ### Affichage résultats sur l'invite de commande

    print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
    print("ua = " + str(ua) + "\nub = " + str(ub) )
    print ("On trouve avec la variation de l'amplitude, delta = ", -1/b, "m, avec une incertitude ", ub / b**2, "m")
    print("On trouve avec la variation de l'amplitude, lambda =", 8.96e3*380*omega*(-1/b)**2/2, "W/m/K, avec une incertitude ", (ub / b**2) * (-b) * np.sqrt(2) *8.96e3*380*omega*(-1/b)**2/2, "W/m/K")

    ### Tracé de la courbe

    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
    plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()


if graphe3:

    ### Données fit

    xdata = X
    ydata = A_moy

    debut=0
    fin=len(xdata)+1

    xfit = X
    xerrdata = dx
    xerr = xerrdata

    yfit = A_moy
    yerrdata = da_moy
    yerr = yerrdata

    ### Noms axes et titre

    ystr='Température moyenne [°C]'
    xstr='Distance au module Peltier [m]'
    titlestr='Température moyenne en fonction de la distance au module Peltier'

    ### Ajustement

    def func(x,a,b):
        return a + b*x

    popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

    ### Récupération paramètres de fit

    a,b=popt
    ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

    ### Affichage résultats sur l'invite de commande

    print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
    print("ua = " + str(ua) + "\nub = " + str(ub) )


    ### Tracé de la courbe

    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
    plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()
