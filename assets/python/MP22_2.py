"""
@Louis Heitz et Vincent Brémaud

"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

rendement=0 # Mettre le rendement à 0 pour regarder le gain en courant. A 1 pour regarder le rendement.


### Point en live

R=5

ielive=10e-3
uoutlive=4.1

dielive=0.1e-3
dutoutlive=0.1
# Pg1live=
# Pg2live=

ioutlive=uoutlive/R
xlive=np.array([ielive])
ylive=np.array([ioutlive])



xliverr=np.array([dielive])
yliverr=np.array([dutoutlive/R])
# xlive=[]
# ylive=[]
# xliverr=[]
# yliverr=[]


### Données

def func(x,a,b):
    return a*x + b


R=5 # Mesurée au RLC metre.La resistance est l'espece de gros pavé.
ie=np.array([1.11,4.85,9.09,13.3])*1e-3 # Mesure RMS, AC+DC car u et i sinus
ue=np.array([0.94,2.57,4.37,6.17]) # Mesure RMS, AC+DC car u et i sinus
Pe=np.array([0.92,11.12,36,75])*1e-3 # Le puissancemetre donne UIcos\phi
uout=np.array([0.25,1.96,3.70,5.45])# IDem
iout=uout/R# Idem Permet d'éviter de mettre un Wattmetre supplementaire mesure RMS à l'osciillo. ou au Wattmetre de precision peu importe.
Pout=uout*iout# Idem

ig1=np.array([17,142,285,436])*1e-3 # Ca change pas grand chose mais ici faire la mesure DC car Eg continue
ig2=np.array([16,159,319,488])*1e-3 # Idem
ug1=15 # Constant
ug2=15 # Constant


Pg1=ig1*ug1
Pg2=ig2*ug2
# Pg1=np.array([0.276,2.14,4.32,6.6]) # <UI>=U<I>, c'est pour ca qu'il faut faire la mesure DC pour avoir la moyenne.
# Pg2=np.array([0.243,2.46,4.95,7.55]) # Idem
ug=15


eta=Pout/(Pe+Pg1+Pg2+Pout) #Pe négligeable, on le garde pour la forme

if rendement==0:
    xdata=ie
    ydata=iout
if rendement==1:
    xdata=ue
    ydata=eta

die=0.01*ie
diout=0.01*iout
deta=0.05*eta

### Incertitudes

if rendement ==0:
        xerrdata=die
        yerrdata=diout

if rendement ==1:
        xerrdata=die
        yerrdata=deta

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

if rendement==0:
    ystr='Iout [A]'
    xstr='Ie [A]'
    titlestr='Amplification du courant'

if rendement==1:
    ystr='$\eta$'
    xstr='$U_e$ [Vrms]'
    titlestr='Etude du rendement du montage Push-Pull'

### Ajustement


def func(x,a,b):
    return a+b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

if rendement==0:
    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Préparation')
    if len(xlive)>0:
        plt.errorbar(xlive,ylive,yerr=yliverr,fmt='o',label='Point ajouté')
    plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()
if rendement==1:
    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Préparation')
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