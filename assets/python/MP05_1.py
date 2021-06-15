"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

liste_couleur=['b','c','g','r','m','y','k']

#Données en livé = une des listes

### Données

Temp=np.array([47.1]) # En degré celcius

P1=np.array([10.25,10.75,11.25,12,13,14,15,16.5,18,20,22.5,25.5,28.75,32.75,36,41.5]) #En Bar
V1=np.array([3.85,3.7,3.5,3.25,3,2.75,2.5,2.25,2,1.75,1.5,1.25,1,0.75,0.5,0.25]) #En millilitre

P2=np.array([]) #En Bar
V2=np.array([]) #En millilitre

P3=np.array([]) #En Bar
V3=np.array([]) #En millilitre

P4=np.array([]) #En Bar
V4=np.array([]) #En millilitre

#Faire la P4 et V4 en live par exemple.

P=[]
P.append(P1)
P.append(P2)
P.append(P3)
P.append(P4)
P=np.array(P)

V=[]
V.append(V1)
V.append(V2)
V.append(V3)
V.append(V4)
V=np.array(V)


P*=1e5
V*=1e-6

dP=0.25e5 #En Pascal
dV=0.025e-6 # en m3

ydata=P*V
xdata=1/V



### Incertitudes

xerrdata=np.array(dV/V**2)
yerrdata=[]
for k in range(len(P)):
    yerrdata.append(np.array(ydata[k]*np.sqrt((dP/P[k])**2 + (dV/V[k])**2)))
yerrdata=np.array(yerrdata)

xlive = np.array([])
xliverr = np.array([])
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

ystr='$PV$ [J] '
xstr='$1/V$ [1/m$^3$]'
titlestr="Réalisation d'un thermomètre primaire"
ftsize=18

### Ajustement

def func(x,a,b):
    return a + b*x

popt,pcov=[],[]
for k in range(len(Temp)):
    debut=0
    fin=len(xfit[k])-5
    xfitk=xfit[k][debut:fin]
    yfitk=yfit[k][debut:fin]
    yerrk=yerr[k][debut:fin]
    poptk, pcovk = curve_fit(func, xfitk, yfitk,sigma=yerrk,absolute_sigma=True)
    popt.append(poptk)
    pcov.append(pcovk)

### Récupération paramètres de fit

for k in range(len(Temp)):
    a,b=popt[k]
    ua,ub=np.sqrt(pcov[k][0,0]),np.sqrt(pcov[k][1,1])
    print("Pour T = " + str (Temp[k]) + '°C, on trouve : \n')
    print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
    print("ua = " + str(ua) + "\nub = " + str(ub) +'\n \n')

### Tracé de la courbe

plt.figure(figsize=(10,9))
for k in range(len(Temp)):
    a,b=popt[k]
    T=Temp[k]
    col=liste_couleur[k]
    lab="T = " + str(T) + "°C"
    plt.errorbar(xdata[k],ydata[k],yerr=yerrdata[k],xerr=xerrdata[k],fmt='o',c=col,label=lab)
    plt.plot(xfit[k],func(xfit[k],a,b),c=col)

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


### Interprétation

#L'ordonnée à l'origine vaut nRT, connaissant n et R on détermine T, on peut également déterminer les coefficients du Viriel avec un fit plus complexe

n = 1.67e-3 #on suppose n connu, à vérifier
R = 8.31

for k in range(len(Temp)):
    print("Température mesurée = "+str(popt[k][0]/R/n)+" +- "+str(np.sqrt(pcov[k][0,0])/R/n)+" K pour une valeur expérimentale de "+str(Temp[k]+273.15)+" K")