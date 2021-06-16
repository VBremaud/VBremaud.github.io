
"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

rendement = 1 # Booléen. A mettre à 1 pour avoir le rendement, à 0 pour avoir les pertes en fonctions de omega
### Point en live

Umotlive=np.array([4])
Uklive=np.array([0.8])
Ilive=np.array([0.790])

incUmotlive=np.array([0.1])
incUklive=np.array([0.05])
incIlive=np.array([0.005])

Uclive=np.array([])
Iclive=np.array([])
Ulive=np.array([])
Ulive=np.array([])
Uklive2=np.array([])


if rendement ==0:
    ylive=Umotlive*Ilive-0.98*(Ilive+1.5)*Ilive
    xlive=Uklive*1000*2*np.pi/60/6
    xliverr= np.array([0.02])
    yliverr=np.array([0.05])

if rendement ==1 :
    ylive= Uclive*Iclive/(Ilive*Ulive)
    xlive=Ulive*Ilive
    xliverr= np.array([1])
    yliverr=np.array([1])

### Données


Umot=np.array([3.58, 5.76, 7.39,8.83,12.33,15.42,18.75,21.95,24.73,27.08,30.05]) #Umot (V)
xdata=np.array([0.320, 1, 1.55, 2.01,3.18,4.20,5.29,6.36,7.29,8.07,9.07]) #Uk (V)
zdata=np.array([0.770, 0.808, 0.825, 0.840,0.866,0.882,0.898,0.911,0.923,0.931,0.941]) #I

if rendement ==0:
    ydata=Umot*zdata-0.98*(zdata+1.5)*zdata #+1.5 pour tenir compte d'offset #Pertes totales fer et méca
    xdata*=1000*2*np.pi/60/6 # Pour tracer les pertes totale fer et méca

Uc=np.array([21.62,21.57,21.50,21.35,21.21,21.03,20.83,20.53])
Ic=np.array([0.442,0.533,0.589,0.685,0.920,1.110,1.295,1.662])
U=np.array([27.17,27.23,27.29,27.38,27.58,27.68,27.78,28.04])
I=np.array([1.37,1.46,1.52,1.61,1.84,2.020,2.200,2.560])
Uk=np.array([8.048,8.031,8.040,8.05,8.066,8.06,8.045,8.065])

if rendement ==1:
    ydata=Uc*Ic/(I*U) #Pour tracer le rendement élec
    xdata=U*I #Pour tracer le rendement élec

rind=0.98
afit=0.22535250987042232
bfit=0.14598431918877197
cfit=0.00011243509140379355

Omega=Uk*1000*2*np.pi/60/6

ydata1=(U*I-(rind*I+1)*I - (afit + bfit*Omega + cfit*Omega**2)*0.48)/(U*I) #Rendement première MCC
xdata1=U*I  #Rendement première MCC


ydata2=(U*I*ydata1-(rind*Ic+1)*Ic - (afit + bfit*Omega + cfit*Omega**2)*0.52)/(U*I*ydata1) #Rendement deuxième MCC
xdata2=U*I*ydata1 #Rendement deuxième MCC
# Tracer rendement en fonction de UI
#En mettant 0.98 aux deux, ça fontionne :)

#On a changé le /2 en 0.48 et 0.52 pour que ça fontionne. Justification ?
### Incertitudes

Umoterr=0.05
Ukerr=0.01
Ierr=np.array([0.005,0.005,0.004,0.0033,0.003,0.0025,0.0025,0.0025,0.0025,0.0025,0.0025])


#yerr=ydata*np.sqrt(zdata**2*Umoterr**2 + (Umot-0.98*2*zdata)**2*Ierr**2)
yerr=np.array([0.01]*len(ydata))

xerrdata=np.array([Ukerr*1000*2*np.pi/60/6]*len(xdata))
yerrdata=np.array(yerr)


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

if rendement ==1:
    ystr='$\eta $'
    xstr='$UI$ [W]'
    titlestr="Rendement en fonction de la puissance d'entrée"

if rendement ==0:
    ystr='$P_{pertes}$ [W]'
    xstr='$\Omega$ [rad/s]'
    titlestr='Pertes totales en fonction de $\Omega$'

### Ajustement

# noise=0*np.random.rand(1,len(yfit))
#
#
# yfit= yfit+ noise
# yfit=yfit[0]
#

def func(x,a,b,c):
    return a+b*x + c*x**2
if rendement ==0:
    popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

if rendement ==0:
    a,b,c=popt
    ua,ub,uc=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1]),np.sqrt(pcov[2,2])
    print("y = a  + b x  + c x^2 \na = " + str(a) + "\nb = " + str(b)+ "\nc = " + str(c))
    print("ua = " + str(ua) + "\nub = " + str(ub) + "\nuc = " + str(uc) )

### Tracé de la courbe

if rendement ==1:
    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',markersize=4,label='Données tot')
    plt.plot(xdata1,ydata1,'o',markersize=4,label='Données mot1')
    plt.plot(xdata2,ydata2,'o',markersize=4,label='Données mot2')
    plt.plot(xdata1,ydata1*ydata2,'o',label='mot1*mot2')
    #plt.plot(xdata1,ydata1**2,'o',label='test')
    if len(xlive)>0:
        plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
    #plt.plot(xfit,func(xfit,a,b,c),label='Ajustement ')
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    #plt.axis([0,75,0,0.6])
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()

if rendement ==0:
    plt.figure(figsize=(10,9))
    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',markersize=4,label='Données en préparation')
    if len(xlive)>0:
        plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
    plt.plot(xdata,func(xdata,a,b,c),label='Ajustement ')
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    #plt.axis([0,75,0,0.6])
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()