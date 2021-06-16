"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

bif=0 #Booleen : pour avoir diagramme de bifurcation, mettre à 1. Pour la droite mettre à 0



### Point en live

Omegalive=205
anglelive=58

dOmegalive=1
danglelive=2

anglelive*=np.pi/180
danglelive*=np.pi/180
Omegalive*=2*np.pi/60
dOmegalive*=2*np.pi/60

if bif==0:
    ylive=np.array([np.cos(anglelive)])
    xlive=np.array([1/Omegalive**2])
    xliverr=np.array([2*dOmegalive/Omegalive**3])
    yliverr=np.array([np.sin(anglelive)*danglelive])
xlive=[]
ylive=[]



xliverr=[]
yliverr=[]

### Données


Omega=np.array([109,158,188,198,213,252])
dOmega=np.zeros(len(Omega))+1

Omega=Omega*2*np.pi/60
dOmega*=2*np.pi/60
angle=np.array([0,10,45,55,62,70])*np.pi/180

dangle=(np.zeros(len(angle))+2)*np.pi/180

#angle=np.array([0,0,0,0,0,35,50,57,65,72,75,75])

#Omega=np.array([50.6,58,91,118,131,160,184,196,217,246,263,281])

g=9.81
R=4.3e-2
Omegac=np.sqrt(g/R)


if bif==0:
    xdata=1/Omega**2
    ydata=np.cos(angle)

if bif==1:
    xdata=Omega
    ydata=angle
#xdata=xdata/1000

### Incertitudes

if bif==0 :
    xerrdata=2*dOmega/Omega**3
    yerrdata=np.sin(angle)*dangle

if bif==1:
    xerrdata=dOmega
    yerrdata=dangle


if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata,xliverr))
    yerr=np.concatenate((yerrdata,yliverr))


if len(xliverr)== 0 :
    xerr=xerrdata
    yerr=yerrdata

### Données fit
deb_bif=0
fin_bif=len(xdata)+1

deb_fit=1
fin_fit=len(xdata)+1

if bif ==0 :
    debut=deb_fit
    fin=fin_fit

if bif ==1 :
    debut=deb_bif
    fin=fin_bif

if len(xlive) >0 :
    xlive=np.array(xlive)
    ylive=np.array(ylive)
    xfit=np.concatenate((xdata[debut:fin],xlive))
    yfit=np.concatenate((ydata[debut:fin],ylive))


if len(xlive) == 0 :
    xfit=xdata[debut:fin]
    yfit=ydata[debut:fin]


### Noms axes et titre

if bif==0:
    ystr='$cos \Theta_{eq}$ '
    xstr='1/$\Omega^2$ [s^2/rad^2]'
    titlestr="Ajustement linéaire"

if bif==1:
    ystr='$\Theta_{eq}$ [rad]'
    xstr='$\Omega$ [rad/s]'
    titlestr="Diagramme de bifurcation"



### Ajustement


def func(x,a,b):
    return a+b*x

def func2(x,a,b):
    return np.heaviside(x-a,1)*b*np.sqrt(np.abs(x-a))


if bif ==0 :
    popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

if bif ==1 :
    popt, pcov = curve_fit(func2, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

if bif==0 :
    a,b=popt
    ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
    print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
    print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

if bif==0 :
    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Préparation')
    if len(xlive)>0:
        plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
    plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    #plt.axis([0,3.600,0,5])
    #plt.axis([0,xdata[-1]*1.05,0,ydata[-1]*1.05])
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()

if bif==1:
    xplot=np.linspace(0,25,1000)
    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Préparation')
    if len(xlive)>0:
        plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
    plt.plot(xplot,func2(xplot,*popt),label='Ajustement ')
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    #plt.axis([0,3.600,0,5])
    #plt.axis([0,xdata[-1]*1.05,0,ydata[-1]*1.05])
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()