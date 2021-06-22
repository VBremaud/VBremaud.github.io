"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

rendement=0 #Mettre à 1 pour afficher le graphe en rendement, booléen
#pertes = (1-rendement)

### Point en live


p2live=4.70
p1live=9.70
i2live=210/1000
i1live=70/1000

incp2live=0.01
incp1live=0.01
inci2live=0.1
inci1live=0.1

if rendement ==1 :
    xlive=[p2live]
    ylive=[p2live/p1live]
    xliverr=np.array([incp2live])
    yliverr=np.array([p2live*np.sqrt((incp2live/p2live)**(2) + (incp1live/p1live)**(2))])

else:
    xlive=[p2live]
    ylive=[p1live-p2live]
    xliverr=np.array([incp2live])
    yliverr=np.array([(incp2live**2 + incp1live**2)])
#xlive=[]
#ylive=[]

#xliverr=np.array([])
#yliverr=np.array([])

#xliverr=[]
#yliverr=[]


# rendement=0 #Mettre à 1 pour afficher le graphe en rendement
# pertes = (1-rendement)

### Données

i1=np.array([59.4,69.5,72.6,77.6,85.3,102.4,129.7,172.2,272.3])
p1=np.array([4.89,9.55,10.65,12.28,14.58,19.24,26,36.0,58.2])
i2=np.array([0,199.9,247.4,317.3,415.4,614.8,907.6,1335,2302])
p2=np.array([0,4.58,5.68,7.28,9.46,13.86,20.1,28.8,46.4])

inci1=np.array([0.1,0.1,0.1,0.1,0.2,0.2,0.2,0.2,0.2])
incp1=np.array([0.02,0.02,0.02,0.02,0.02,0.02,0.05,0.05,0.05])
inci2=np.array([0.1,0.1,0.1,0.1,0.2,0.2,0.2,0.2,0.2])
incp2=np.array([0.01,0.01,0.01,0.01,0.02,0.05,0.05,0.05,0.05])

i1*=1/1000
i2*=1/1000

if rendement ==1:
    ydata=p2/p1 #Pour le rendement
    xdata=p2

else:
    ydata=p1-p2 #Pour le calcul des pertes
    xdata=p2

    ydata1=40*i1**2 + 0.72*i2**2 + (ydata[0]-40*i1[0]**2 - 0.72*i2[0]**2) #  R1 I1^2 + R2 I2^2 + Pfer
#Avec Pfer = Pertes en avec courant nul dans la charge, retiré des pertes joules ; terme en parenthèses


#xdata=np.array([134,347,584,900,1367,1698,2277,2636,3077]) #I
#ydata=np.array([0.71,1.47,2,2.47,3,3.330,3.92,4.21,4.61]) #U
#xdata=xdata/1000

#Calibres : i1=0.2 ; i2 =0.5->2 ; u1 =300 ; u2 = 30

### Incertitudes

xerrdata=incp2

if rendement ==1:
    yerrdata=ydata*np.sqrt((incp1/p1)**2 + (incp2/p2)**2)

else :
    yerrdata=np.sqrt((incp2**2 + incp1**2))
# Ajouter incertitudes constructeur
if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata,xliverr))
    yerr=np.concatenate((yerrdata,yliverr))


if len(xliverr)== 0 :
    xerr=xerrdata
    yerr=yerrdata

### Données fit


debut=3
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

ystr='$\eta$ '
xstr='$Pc$ [W]'
if rendement ==1:
    titlestr="Rendement du transformateur"
    ystr='$\eta$ '
    xstr='$Pc$ [W]'
else:
    titlestr="Pertes du transformateur"
    ystr='$P_{pertes} [W]$'
    xstr='$Pc$ [W]'

### Ajustement


def func(x,a,b):
    return a+b*x

#popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

# a,b=popt
# ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
# print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
# print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

if rendement ==1 :

    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',markersize=4,label='Données prises en préparation')
    #plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',markersize=4,label='Données mesurées')
    if len(xlive)>0:
        plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
    #plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    #plt.axis([0,40,0,15])
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()

else:
    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',markersize=4, label='Données mesurées')
    plt.errorbar(xdata,ydata1,yerr=yerrdata,xerr=xerrdata,fmt='o',markersize=4,label='Données calculées')
    if len(xlive)>0:
        plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
    #plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    #plt.axis([0,40,0,15])
    plt.yticks(fontsize=ftsize)
    #plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()