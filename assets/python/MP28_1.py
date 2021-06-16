# -*- coding: utf-8 -*-

"""
@Louis Heitz et Vincent Brémaud

"""


import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import os

plt.close('all')

Eta=1 #Booleen pour etalonnage du capteur
## Montrer en FFT l'harmonique de rang 3

'''
Penser à mettre la FFT en linéaire. Sinon on a l'impression d'avoir une contribution au rand 2 enorme.
Cette contribution existe bien sur due a la non linearité du capteur et le fait qu'il n'est pas symétrique dans sa réponse, cependant, elle est normalement quand meme moins predominante et ce n'est pas ce que l'on veut regarder
'''


### Point en live


Anglelive=88
Periodelive=16.5/8

dAnglelive=0.5
dPeriodelive=0.05*np.sqrt(2)/8

xlive=np.array([(Anglelive*np.pi/180)**2]) #
ylive=np.array([Periodelive]) #

xliverr=np.array([2*dAnglelive*Anglelive*(np.pi/180)**2])
yliverr=np.array([dPeriodelive])


### Données

Angle=np.array([90,85,80,75,70,65,60,55,50,45,40,35,30,25,20,15,10])
Tension=-np.array([9.25,8.43,7.94,7.19,6.62,6,5.56,5,4.5,4.1,3.45,2.98,2.65,2.25,1.77,1.31,0.98]) # Amplitude de la seconde oscillation à partir de laquelle on compte, Attention au signe !!
Periode=np.array([16.64,16.3,16.2,15.9,15.7,15.5,15.4,15.22,15.12,14.96,14.82,14.7,14.6,14.54,14.48,14.44,14.4])/8 # Mesure de 8 périodes en mode Single

xdata=(Angle*np.pi/180)**2
#xdata=(etalon(Tension)*np.pi/180)**2 # Pour mettre l'angle en radians
ydata=Periode


### Incertitudes
uAngle=np.zeros(len(Angle))+0.5
uTension=np.zeros(len(Tension))+0.2
uPeriode=np.zeros(len(Periode))+0.05*np.sqrt(2)/8

xerrdata=2*uAngle*Angle*(np.pi/180)**2
#xerrdata=2*etalon(Tension)*np.pi/180*uTheta[0]*np.pi/180 #Je reprend l'incertitude sur les angles de l'étalon, de toute façon on s'en fiche un peu, c'est en x!
yerrdata=uPeriode


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

ystr='T [s]'
xstr=r'$\theta_0^2$ [rad^2]'
titlestr='Vérification loi de Borda'
ftsize=18


### Ajustement

def func(x,a,b):
    return a*(1 + b*x)

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a*(1  + b*x) \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé des courbes

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o', label='Preparation')

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


Pente = a/b
uPente = Pente*np.sqrt((ua/a)**2+(ub/b)**2)

print('\nPente Borda= ' + str('%.3e'%Pente))
print('Incertitude associée = ' + str('%.1e'%uPente))

# En théorie a/b vaut 1/16=0.0625, apparemment il y a un biais : étalonnage ? T0 ?

'''
On voit d'ailleurs qu'utiliser l'etalonnage est même moins precis. Ne pas le faire :)
'''



## Etalonnage du Capteur
'''
Ceci est à mon sens un peu overkilling pour le montage mais pour des questions ca peut être interessant.
'''


#Je défini les angles positifs dans le sens trigo
V=np.array([9.18,8.59,7.63,7.22,6.48,5.88,5.30,4.81,4.29,3.87,3.37,2.91,2.45,2.05,1.61,1.20,0.75,0.37,0.001,-0.48,-0.99,-1.39,-1.80,-2.29,-2.80,-3.23,-3.70,-4.24,-4.61,-5.26,-5.9,-6.47,-7.05,-7.57,-8.37,-9.24,-10.12]) # mV
Theta=np.array([-90,-85,-80,-75,-70,-65,-60,-55,-50,-45,-40,-35,-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]) #

uV=np.zeros(len(V))+0.1
uTheta=np.zeros(len(Theta))+2

etalon=interp1d(V,Theta)

if Eta==1:
    ftsize=18
    plt.figure(figsize=(10,9))
    plt.errorbar(V,Theta,yerr=uTheta,xerr=uV,fmt='o',label='Preparation')
    plt.plot(V,etalon(V),label='Ajustement ')
    plt.title('Etalonnage',fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel('Tension (V)',fontsize=ftsize)
    plt.ylabel('Angle (degré)',fontsize=ftsize)
    plt.show()

''' Formule de Borda '''
























