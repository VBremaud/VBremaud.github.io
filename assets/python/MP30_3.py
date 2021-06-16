import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit



ftsize=18

freq=1 # Mettre à 1 pour verifier la dependance en frequence.
'''
Prendre le module ECHOSCOPE.
Prendre la cuve sur lequel on peut translater la sonde réceptrice
Brancher la sonde émettrice et faire adaptation d'impédance sur l'entrée de cuve.
Placer la sonde réceptrice dans le bon sens et faire le trigger sur l'enveloppe a priori le trigger est pourrave
Mesurer l'amplitude du pic recu, le temps de propagation et la distance emetteur recepteur à partir d'une distance donnée. Nous avions comencé à 3cm l'un de l'autre pour la posito de reference.

L'idée de la manip est de montrer l'attenuation d'une onde acoustique dans un fluide.
Nous allons dans un premier temps montrer que comment cette amplitude decroit


Puis nous evaluerons l'evolution du facteur de relaxation avec la fréquence.
La fréquence peut se voir en regardant au sein du pulse l'oscillation produite. En fait la sonde envoie pendant un certain temps un signal d'une certaine amplitude avec une certaine fréquence.

'''


### Point en live
Tlive=np.array([1.12e-6/3]) #Mesure du temps entre trois oscillations (microsec)

xlive_in=np.array([6])*1e-2 #Position du récepteur (m)
ylive_in=np.array([0.6]) # Amplitude du maximum (V)

xliverr_in=np.array([1])*1e-3
yliverr_in=np.array([0.05])

if len(xlive_in)>0:
    xlive=xlive_in#-Position[0]
    ylive=np.log(ylive_in)#/Amplitude[0])
else:
    xlive=np.array([])
    ylive=np.array([])


if len(xlive_in)>0:
    xliverr=xliverr_in*np.sqrt(2)
    yliverr=2*yliverr_in/ylive_in
else:
    xliverr=np.array([])
    yliverr=np.array([])


### Données


#Autres fréquences mesurées.
'''
T=2.54e-6/3
Amplitude=np.array([1.27,1.23,1.14,1.056,0.975,0.893,0.856])
temps=np.array([0,6.4,13.38,18.54,24.96,29.86,34.5])*1e-6
Position=np.array([6.3,7.5,8.9,9.9,11.2,12.1,13])*1e-2

T=1.7e-6/3
Amplitude=np.array([1.42,1.337,1.287,1.143,1.03,0.906,0.806,0.656])
temps=np.array([0,19,24.2,34.2,42.5,48,54.6,64.1])*1e-6
Position=np.array([3,4.5,5.4,7.4,9,10,11.2,13.1])*1e-2
'''

T=1.12e-6/3 #Période du signal
Amplitude=np.array([0.704,0.529,0.346,0.251,0.165,0.112])
temps=np.array([0,8.3,17.76,24.94,33.18,40.9])*1e-6
Position=np.array([5.7,7.2,9,10.4,12,13.4])*1e-2

#print(Position/temps)

cson=1915
f=1/T
Amplitude_dat=Amplitude/Amplitude[0]#Normalise l'amplitude
Position_dat=Position-Position[0]#Pour que la position initiale soit la référence
decrement=np.log(Amplitude_dat)

xdata=Position_dat
ydata=decrement


if len(xlive_in)>0:
    xlive=xlive_in-Position[0]
    ylive=np.log(ylive_in/Amplitude[0])

### Incertitudes

dAmplitude=10e-3
dtemps=140e-9
dPosition=1e-3

xerrdata=np.array([dPosition]*len(xdata))
yerrdata=dAmplitude/Amplitude


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

ystr="log(A/A0)"
xstr="Distance (m)"
titlestr="Attténuation du paquet d'onde dans le glycérol"

### Ajustement

def func(x,a,b):
    return  a*x + b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print('\nAtténuation à une fréquence donnée')
print("y =  ax + b \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,fmt='o',xerr=xerrdata,label='Preparation')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


### Récupération paramètres de fit



eta=1.49
rho=1.26e3
omega=2*np.pi*f
cson=1915
alpha_th=eta*omega**2/(2*rho*cson**3) # On suppose ici le fluide incompressible, on a pas trop moyen de le verifier.


print('\nalpha_th : ' + str(alpha_th)+ ' m')

alpha=np.abs(a)

print('alpha_exp : ' + str(alpha)+ ' m')
print('u(alpha_exp) : ' + str(ua)+ ' m')


## Verification hypothèses

'''
On verifie que le temps de relaxation du fluide est bien plus petit que la periode d'oscillation.
'''

tau=eta/(rho*cson**2)
print('omega*tau = '+str(omega*tau)) # On verifie bien que cette approximation est valide.












if freq==1:



    ### Point en live

    Tlive=np.array([1.12])*1e-6/3 #Mesure du temps entre trois oscillations (microsec)
    dTlive=np.array([0.01])*1e-6/3

    xlive=(2*np.pi/Tlive)**2
    ylive=np.array([-a])

    xliverr=2*(2*np.pi/Tlive)*2*np.pi*dTlive/Tlive**2
    yliverr=np.array([ua])

    ### Données
    T=np.array([2.54e-6/3,1.7e-6/3])

    f2=(2*np.pi/T)**2
    alpha=np.array([7.12,10.9])

    xdata=f2
    ydata=alpha

    ### Incertitudes
    dT=0.01e-6/3
    ualpha=np.array([0.4,0.6])

    uf2 = 2*(2*np.pi/T)*2*np.pi*dT/T**2

    xerrdata=uf2
    yerrdata=ualpha


    if len(xliverr) >0 :
        xerr=np.concatenate((xerrdata,xliverr))
        yerr=np.concatenate((yerrdata,yliverr))

    if len(xliverr)== 0 :
        xerr=xerrdata
        yerr=yerrdata

    ### Données fit

    debut=0  #
    fin=len(xdata)+1

    if len(xlive) >0 :
        xlive=np.array(xlive)
        ylive=np.array(ylive)
        xfit=np.concatenate((xdata[debut:fin],xlive))
        yfit=np.concatenate((ydata[debut:fin],ylive))


    if len(xlive) == 0 :
        xfit=xdata[debut:fin]
        yfit=ydata[debut:fin]


    poptf, pcovf = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)
    af,bf=poptf
    uaf,ubf=np.sqrt(pcovf[0,0]),np.sqrt(pcovf[1,1])


    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Preparation')
    if len(xlive)>0:
        plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point en direct')
    plt.plot(xfit,func(xfit,*poptf),label='Ajustement ')
    plt.title('Variation de l\'absorption',fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel('f^2 (Hz^2)',fontsize=ftsize)
    plt.ylabel('Coefficient d\'absorption linéaire [m]',fontsize=ftsize)
    plt.show()

    ## Extraction du parametre de fit

    print('\nAjustement en fonction de la fréquence \n')
    print("y =  ax + b \na = " + str(af) + "\nb = " + str(bf))
    print("ua = " + str(uaf) + "\nub = " + str(ubf) )


    Pth=eta/(2*rho*cson**3)
    print('Valeur théorique de la pente : ' + str(Pth) + ' m s^2') # Commenter qu'on pourrait peut être remettre en cause avec la seconde viscoité. Peut être aussi que l'on ne connait pas assez bien le parametre de viscosité ou la vitesse du son dans le glycerol.