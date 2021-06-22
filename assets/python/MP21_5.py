"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

####### Tracer les pertes séparément puis la somme des pertes, comme pour le transfo

rendement = 0 # Booléen mettre à 1 pour avoir le rendement, à 0 pour avoir les pertes

### Point en live

Pinducteurlive=84 #mettre à 0 ou inférieur à 0 pour ne pas afficher le point
Pinduitlive=80
Iinduitlive=0.350
Pmcclive=155
Imcclive=4.7

dPinducteurlive = 1
dPinduitlive = 1
dIinduitlive = 0.01
dPmcclive = 1
dImcclive = 0.05



### Données


Pinducteur=np.array([83,84,84,84,84,84,84,84])
Pinduit=np.array([64,73,84,99,129,133,147,181]) #Puissance dans charge
Iinduit=np.array([0.310,0.360,0.422,0.512,0.655,0.682,0.780,0.964])
Pmcc=np.array([139,149,164,186,232,238,261,317])
Imcc=np.array([4.15,4.5,4.92,5.59,6.65,6.84,7.52,8.77])

dPinducteur = np.array([0.1]*len(Pinducteur))
dPinduit = np.array([0.1]*len(Pinduit))
dIinduit = np.array([0.001]*len(Iinduit))
dPmcc = np.array([0.1]*len(Pmcc))
dImcc = np.array([0.005]*len(Imcc))

rinducteur=494
drinducteur = 0.1

rinduit=16
drinduit = 0.01

Psansind= 19 #Envoyé dans la MCC
dPsansind = 0.1

Isansind=0.630 #Pour calculer pertes effets Joule dans MCC
dIsansind= 0.001


Pavecind=58
dPavecind = 0.1

Iavecind=1.8
dIavecind = 0.01

Iinducteur=0.4
dIinducteur = 0.001

Uinducteur=220
dUinducteur = 0.1

rmcc=0.83
drmcc=0.01

Omega=1500*2*np.pi/60
dOmega=1*2*np.pi/60


# A vérifier

Pmccpertes=(0.089*Omega + 7.4e-5 * Omega**2) + rmcc*Imcc**2

Pmeca2 = Psansind - (0.089*Omega + 7.4e-5 * Omega**2) - rmcc*Isansind**2 #Pertes méca dans 2ieme machine

Pfer2= Pavecind + Uinducteur*Iinducteur - (0.089*Omega + 7.4e-5 * Omega**2) - rmcc*Iavecind**2 - Pmeca2 - rinducteur*Iinducteur**2 #On fournit via MMCC et inducteur

#ydata1= (Pinducteur + Pmcc - Pmccpertes - rinducteur*Iinducteur**2 - rinduit*Iinduit**2 - Pmeca2 - Pfer2)/(Pinducteur+Pmcc-Pmccpertes) #rendement calculé

if rendement ==1 :
    ydata=Pinduit/(Pinducteur+Pmcc-Pmccpertes)
    xdata=Pinduit
    ydata1= (Pinducteur + Pmcc - Pmccpertes - rinducteur*Iinducteur**2 - rinduit*Iinduit**2 - Pmeca2 -  Pfer2)/(Pinducteur+Pmcc-Pmccpertes) #rendement "calculé"

if rendement ==0:
    xdata=Pinduit
    ydata= (Pinducteur+Pmcc-Pmccpertes) -Pinduit #Pertes mesurées
    ydata1= rinducteur*Iinducteur**2 + rinduit*Iinduit**2 + Pmeca2 + Pfer2 #Pertes totales dans la machine synchrone, calculées


#ydata2= rinducteur*Iinducteur**2 + rinduit*Iinduit**2 + Pmeca2 + Pfer2 #Pertes totales dans la machine synchrone
# upinduc=1 --> 5
# upinduit=1 --> 5
# uIinduit=5 --> 10
# uPmcc=1 --> 5
# IMcc=5 --> 10

#La vitesse a chuté jusqu'au point n°5
#0.2 a partur de 200 pour xdata
### Incertitudes

N=1000

Pinduiti=np.zeros((N,len(xdata)))
Pinducteuri=np.zeros((N,len(xdata)))
Pmcci=np.zeros((N,len(xdata)))
Iinduiti=np.zeros((N,len(xdata)))
Imcci=np.zeros((N,len(xdata)))
rinducteuri=np.zeros(N)
rinduiti=np.zeros(N)
Pavecindi=np.zeros(N)
Psansindi=np.zeros(N)
Iavecindi=np.zeros(N)
Isansindi=np.zeros(N)
Iinducteuri=np.zeros(N)
Uinducteuri=np.zeros(N)
rmcci=np.zeros(N)
Omegai=np.zeros(N)

Y11=np.zeros((N,len(xdata)))
Y12=np.zeros((N,len(xdata)))
Y21=np.zeros((N,len(xdata)))
Y22=np.zeros((N,len(xdata)))

Pmccpertesi = np.zeros((N,len(xdata)))
Pmeca2i = np.zeros(N)
Pfer2i = np.zeros(N)

for i in range(N):
    for k in range(len(xdata)):
        Pinduiti[i][k]=Pinduit[k]+dPinduit[k]*np.random.randn()
        Pinducteuri[i][k]=Pinducteur[k]+dPinducteur[k]*np.random.randn()
        Pmcci[i][k]=Pmcc[k]+dPmcc[k]*np.random.randn()
        Iinduiti[i][k]=Iinduit[k]+dIinduit[k]*np.random.randn()
        Imcci[i][k]=Imcc[k]+dImcc[k]*np.random.randn()

    rinducteuri[i]=rinducteur+drinducteur*np.random.randn()
    rinduiti[i]=rinduit+drinduit*np.random.randn()
    Pavecindi[i]=Pavecind+dPavecind*np.random.randn()
    Psansindi[i]=Psansind+dPsansind*np.random.randn()
    Iavecindi[i]=Iavecind+dIavecind*np.random.randn()
    Isansindi[i]=Isansind+dIsansind*np.random.randn()
    Iinducteuri[i]=Iinducteur+dIinducteur*np.random.randn()
    Uinducteuri[i]=Uinducteur+dUinducteur*np.random.randn()
    rmcci[i]=rmcc+drmcc*np.random.randn()
    Omegai[i]=Omega+dOmega*np.random.randn()

    Pmccpertesi[i] =(0.089*Omegai[i] + 7.4e-5 * Omegai[i]**2) + rmcci[i]*Imcci[i]**2
    Pmeca2i[i] = Psansindi[i] - (0.089*Omegai[i] + 7.4e-5 * Omegai[i]**2) - rmcci[i]*Isansindi[i]**2
    Pfer2i[i]= Pavecindi[i] + Uinducteuri[i]*Iinducteuri[i] - (0.089*Omegai[i] + 7.4e-5 * Omegai[i]**2) - rmcci[i]*Iavecindi[i]**2 - Pmeca2i[i] - rinducteuri[i]*Iinducteuri[i]**2

    Y11[i]= Pinduiti[i]/(Pinducteuri[i]+Pmcci[i]-Pmccpertesi[i])
    Y12[i]= (Pinducteuri[i] + Pmcci[i] - Pmccpertesi[i] - rinducteuri[i]*Iinducteuri[i]**2 - rinduiti[i]*Iinduiti[i]**2 - Pmeca2i[i] -  Pfer2i[i])/(Pinducteuri[i]+Pmcci[i]-Pmccpertesi[i])

    Y21[i]= (Pinducteuri[i]+Pmcci[i]-Pmccpertesi[i]) -Pinduiti[i]
    Y22[i]= rinducteuri[i]*Iinducteuri[i]**2 + rinduiti[i]*Iinduiti[i]**2 + Pmeca2i[i] + Pfer2i[i]

xerrdata=np.array([np.std(Pinduiti.T[:][k]) for k in range(len(xdata))])

if rendement == 1 :
    yerrdata = np.array([np.std(Y11.T[:][k]) for k in range(len(xdata))])
    yerrdata1 = np.array([np.std(Y12.T[:][k]) for k in range(len(xdata))])

else:
    yerrdata = np.array([np.std(Y21.T[:][k]) for k in range(len(xdata))])
    yerrdata1 = np.array([np.std(Y22.T[:][k]) for k in range(len(xdata))])

xlive = np.array([])
xliverr = np.array([])
if Pinducteurlive>0:

    Pmccperteslive=(0.089*Omega + 7.4e-5 * Omega**2) + rmcc*Imcclive**2

    xlive=np.array([Pinduitlive])
    if rendement==1:
        ylive1=Pinduitlive/(Pinducteurlive+Pmcclive-Pmccperteslive)
        ylive2= (Pinducteurlive + Pmcclive - Pmccperteslive - rinducteur*Iinducteur**2 - rinduit*Iinduitlive**2 - Pmeca2 -  Pfer2)/(Pinducteurlive+Pmcclive-Pmccperteslive)

    else:
        ylive1= (Pinducteurlive+Pmcclive-Pmccperteslive) -Pinduitlive #Pertes mesurées
        ylive2= rinducteur*Iinducteur**2 + rinduit*Iinduitlive**2 + Pmeca2 + Pfer2

    Pinduiti=np.zeros(N)
    Pinducteuri=np.zeros(N)
    Pmcci=np.zeros(N)
    Iinduiti=np.zeros(N)
    Imcci=np.zeros(N)
    rinducteuri=np.zeros(N)
    rinduiti=np.zeros(N)
    Pavecindi=np.zeros(N)
    Psansindi=np.zeros(N)
    Iavecindi=np.zeros(N)
    Isansindi=np.zeros(N)
    Iinducteuri=np.zeros(N)
    Uinducteuri=np.zeros(N)
    rmcci=np.zeros(N)
    Omegai=np.zeros(N)

    Y11=np.zeros(N)
    Y12=np.zeros(N)
    Y21=np.zeros(N)
    Y22=np.zeros(N)

    Pmccpertesi = np.zeros(N)
    Pmeca2i = np.zeros(N)
    Pfer2i = np.zeros(N)

    for i in range(N):
        Pinduiti[i]=Pinduitlive+dPinduitlive*np.random.randn()
        Pinducteuri[i]=Pinducteurlive+dPinducteurlive*np.random.randn()
        Pmcci[i]=Pmcclive+dPmcclive*np.random.randn()
        Iinduiti[i]=Iinduitlive+dIinduitlive*np.random.randn()
        Imcci[i]=Imcclive+dImcclive*np.random.randn()

        rinducteuri[i]=rinducteur+drinducteur*np.random.randn()
        rinduiti[i]=rinduit+drinduit*np.random.randn()
        Pavecindi[i]=Pavecind+dPavecind*np.random.randn()
        Psansindi[i]=Psansind+dPsansind*np.random.randn()
        Iavecindi[i]=Iavecind+dIavecind*np.random.randn()
        Isansindi[i]=Isansind+dIsansind*np.random.randn()
        Iinducteuri[i]=Iinducteur+dIinducteur*np.random.randn()
        Uinducteuri[i]=Uinducteur+dUinducteur*np.random.randn()
        rmcci[i]=rmcc+drmcc*np.random.randn()
        Omegai[i]=Omega+dOmega*np.random.randn()

        Pmccpertesi[i] =(0.089*Omegai[i] + 7.4e-5 * Omegai[i]**2) + rmcci[i]*Imcci[i]**2
        Pmeca2i[i] = Psansindi[i] - (0.089*Omegai[i] + 7.4e-5 * Omegai[i]**2) - rmcci[i]*Isansindi[i]**2
        Pfer2i[i]= Pavecindi[i] + Uinducteuri[i]*Iinducteuri[i] - (0.089*Omegai[i] + 7.4e-5 * Omegai[i]**2) - rmcci[i]*Iavecindi[i]**2 - Pmeca2i[i] - rinducteuri[i]*Iinducteuri[i]**2

        Y11[i]= Pinduiti[i]/(Pinducteuri[i]+Pmcci[i]-Pmccpertesi[i])
        Y12[i]= (Pinducteuri[i] + Pmcci[i] - Pmccpertesi[i] - rinducteuri[i]*Iinducteuri[i]**2 - rinduiti[i]*Iinduiti[i]**2 - Pmeca2i[i] -  Pfer2i[i])/(Pinducteuri[i]+Pmcci[i]-Pmccpertesi[i])

        Y21[i]= (Pinducteuri[i]+Pmcci[i]-Pmccpertesi[i]) -Pinduiti[i]
        Y22[i]= rinducteuri[i]*Iinducteuri[i]**2 + rinduiti[i]*Iinduiti[i]**2 + Pmeca2i[i] + Pfer2i[i]

    xliverr = np.array([np.std(Pinduiti)])
    if rendement == 1 :
        yliverr1 = np.array([np.std(Y11)])
        yliverr2 = np.array([np.std(Y12)])

    else:
        yliverr1 = np.array([np.std(Y21)])
        yliverr2 = np.array([np.std(Y22)])

"""
if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata,xliverr))
    yerr=np.concatenate((yerrdata,yliverr))

if len(xliverr)== 0 :
    xerr=xerrdata
    yerr=yerrdata

### Données fit


debut=0
fin=len(xdata)

if len(xlive) >0 :
    xlive=np.array(xlive)
    ylive=np.array(ylive)
    xfit=np.concatenate((xdata[debut:fin],xlive))
    yfit=np.concatenate((ydata[debut:fin],ylive))


if len(xlive) == 0 :
    xfit=xdata[debut:fin]
    yfit=ydata[debut:fin]

"""

### Noms axes et titre

if rendement==1:
    ystr='$\eta$'
    xstr='$P_c$ [W]'
    titlestr="Rendement de la machine synchrone "

if rendement ==0:
    ystr='Pertes [W]'
    xstr='$P_c$ [W]'
    titlestr="Pertes de la machine synchrone "

### Tracé de la courbe

if rendement ==1:
    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',markersize=4,label='Données mesurées')
    plt.errorbar(xdata,ydata1,yerr=yerrdata1,xerr=xerrdata,fmt='o',markersize=4,label='Données "calculées"')
    if len(xlive)>0:
        plt.errorbar(xlive,ylive1,yerr=yliverr1,xerr=xliverr,fmt='o',c='green',label='Données mesurées live')
        plt.errorbar(xlive,ylive2,yerr=yliverr2,xerr=xliverr,fmt='o',c='red',label='Données "calculées" live')
    #plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    #plt.axis([0,3.600,0,5])
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()
else :
    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',markersize=4,label='Données mesurées')
    plt.errorbar(xdata,ydata1,yerr=yerrdata1,xerr=xerrdata,fmt='o',markersize=4,label='Données "calculées"')
    if len(xlive)>0:
        plt.errorbar(xlive,ylive1,yerr=yliverr1,xerr=xliverr,fmt='o',c='green',label='Données mesurées live')
        plt.errorbar(xlive,ylive2,yerr=yliverr2,xerr=xliverr,fmt='o',c='red',label='Données "calculées" live')
    #plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    #plt.axis([0,3.600,0,5])
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()