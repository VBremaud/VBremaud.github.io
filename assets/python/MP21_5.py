"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

####### Tracer les pertes séparément puis la somme des pertes, comme pour le transfo

rendement = 1 # Booléen mettre à 1 pour avoir le rendement, à 0 pour avoir les pertes

### Point en live

Pinducteurlive=84
Pinduitlive=80
Iinduitlive=0.350
Pmcclive=155
Imcclive=4.7


rinducteur=494
rinduit=16

Psansind= 19 #Envoyé dans la MCC
Isansind=0.630 #Pertes effets Joule dans MCC

Pavecind=58
Iavecind=1.8

Iinducteur=0.4
Uinducteur=220



xlive=[]
ylive=[]

#xlive=[]
#ylive=[]

xliverr=np.array([])
yliverr=np.array([])

#xliverr=[]
#yliverr=[]

### Données


Pinducteur=np.array([83,84,84,84,84,84,84,84])
Pinduit=np.array([64,73,84,99,129,133,147,181]) #Puissance dans charge
Iinduit=np.array([0.310,0.360,0.422,0.512,0.655,0.682,0.780,0.964])
Pmcc=np.array([139,149,164,186,232,238,261,317])
Imcc=np.array([4.15,4.5,4.92,5.59,6.65,6.84,7.52,8.77])

rinducteur=494
rinduit=16

Psansind= 19 #Envoyé dans la MCC
Isansind=0.630 #Pour calculer pertes effets Joule dans MCC

Pavecind=58
Iavecind=1.8

Iinducteur=0.4
Uinducteur=220

rmcc=0.83

Omega=1500*2*np.pi/60

dPinduit=1
dPinducteur=1
dPmcc=1
dPmccpertes=1

dPmeca2=0.1
dPfer2=0.1

dIinduit=0.05



# A vérifier

Pmccpertes=(0.089*Omega + 7.4e-5 * Omega**2) + rmcc*Imcc**2 #Données à vérifier ?

Pmeca2 = Psansind - (0.089*Omega + 7.4e-5 * Omega**2) - 0.98*Isansind**2 #Pertes méca dans 2ieme machine

Pfer2= Pavecind + Uinducteur*Iinducteur - (0.089*Omega + 7.4e-5 * Omega**2) - 0.98*Iavecind**2 - Pmeca2 - rinducteur*Iinducteur**2 #On fournit via MMCC et inducteur

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

if rendement ==1 :
    yerrdata=[]
    xerrdata=[]
    for k in range(len(xdata)):
        Pinduiti=np.zeros(N)
        Pinducteuri=np.zeros(N)
        Pmcci=np.zeros(N)
        Pmccpertesi=np.zeros(N)
        for i in range(N):
            Pinduiti[i]=Pinduit[k]+dPinduit*np.random.randn()
            Pinducteuri[i]=Pinducteur[k]+dPinducteur*np.random.randn()
            Pmcci[i]=Pmcc[k]+dPmcc*np.random.randn()
            Pmccpertesi[i]=Pmccpertes[k]+dPmccpertes*np.random.randn()
        eta=Pinduiti/(Pinducteuri+Pmcci-Pmccpertesi)
        yerrdata.append(np.std(eta))
        xerrdata.append(np.std(Pinduiti))
    xerrdata=np.array(xerrdata)
    yerrdata=np.array(yerrdata)

    yerrdata1=[]
    xerrdata1=[]
    for k in range(len(xdata)):
        Pinduiti=np.zeros(N)
        Pinducteuri=np.zeros(N)
        Pmcci=np.zeros(N)
        Pmccpertesi=np.zeros(N)
        Pmeca2i=np.zeros(N)
        Pfer2i=np.zeros(N)
        for i in range(N):
            Pinduiti[i]=Pinduit[k]+dPinduit*np.random.randn()
            Pinducteuri[i]=Pinducteur[k]+dPinducteur*np.random.randn()
            Pmcci[i]=Pmcc[k]+dPmcc*np.random.randn()
            Pmccpertesi[i]=Pmccpertes[k]+dPmccpertes*np.random.randn()
            Pmeca2i[i]=Pmeca2+dPmeca2*np.random.randn()
            Pfer2i[i]=Pfer2+dPfer2*np.random.randn()
        y=  (Pinducteuri + Pmcci - Pmccpertesi - rinducteur*Iinducteur**2 - rinduit*Iinduit[k]**2 - Pmeca2i -  Pfer2i)/(Pinducteuri+Pmcci-Pmccpertesi)
        yerrdata1.append(np.std(y))
        xerrdata1.append(np.std(Pinduiti))
    xerrdata1=np.array(xerrdata1)
    yerrdata1=np.array(yerrdata1)


if rendement ==0:
    yerrdata=[]
    xerrdata=[]
    for k in range(len(xdata)):
        Pinduiti=np.zeros(N)
        Pinducteuri=np.zeros(N)
        Pmcci=np.zeros(N)
        Pmccpertesi=np.zeros(N)

        for i in range(N):
            Pinduiti[i]=Pinduit[k]+dPinduit*np.random.randn()
            Pinducteuri[i]=Pinducteur[k]+dPinducteur*np.random.randn()
            Pmcci[i]=Pmcc[k]+dPmcc*np.random.randn()
            Pmccpertesi[i]=Pmccpertes[k]+dPmccpertes*np.random.randn()
        y=Pinducteuri+Pmcci-Pmccpertesi -Pinduiti
        yerrdata.append(np.std(y))
        xerrdata.append(np.std(Pinduiti))
    xerrdata=np.array(xerrdata)
    yerrdata=np.array(yerrdata)

    yerrdata1=[]
    xerrdata1=[]
    for k in range(len(xdata)):
        Pinduiti=np.zeros(N)
        Pinducteuri=np.zeros(N)
        Pmcci=np.zeros(N)
        Pmccpertesi=np.zeros(N)
        Pmeca2i=np.zeros(N)
        Pfer2i=np.zeros(N)
        Iinduiti=np.zeros(N)
        for i in range(N):
            Pinduiti[i]=Pinduit[k]+dPinduit*np.random.randn()
            Pinducteuri[i]=Pinducteur[k]+dPinducteur*np.random.randn()
            Pmcci[i]=Pmcc[k]+dPmcc*np.random.randn()
            Pmccpertesi[i]=Pmccpertes[k]+dPmccpertes*np.random.randn()
            Pmeca2i[i]=Pmeca2+dPmeca2*np.random.randn()
            Pfer2i[i]=Pfer2+dPfer2*np.random.randn()
            Iinduiti[i]=Iinduit[k]+dIinduit*np.random.randn()
        y=  rinducteur*Iinducteur**2 + rinduit*Iinduiti**2 + Pmeca2i + Pfer2i
        yerrdata1.append(np.std(y))
        xerrdata1.append(np.std(Pinduiti))
    xerrdata1=np.array(xerrdata1)
    yerrdata1=np.array(yerrdata1)


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
    plt.errorbar(xdata,ydata1,yerr=yerrdata1,xerr=xerrdata1,fmt='o',markersize=4,label='Données "calculées"')
    if len(xlive)>0:
        plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
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
    plt.errorbar(xdata,ydata1,yerr=yerrdata1,xerr=xerrdata1,fmt='o',markersize=4,label='Données "calculées"')
    if len(xlive)>0:
        plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
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