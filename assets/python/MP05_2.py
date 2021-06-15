"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')


### Point en live


Tlive=np.array([61.83]) #en degré celsius
Tliverr=np.array([0.04]) #incertitude de la notice 0.03 + 1 digit


Rlivept100 = np.array([123.69]) #résistance en ohm, montage 4 fils
Rliverrpt100 = np.array([0.05]) #incertitude 'visuel' de la résistance lue.

Rlivethermistance = np.array([2876]) #résistance en ohm, montage 4 fils
Rliverrthermistance = np.array([1]) #incertitude 'visuel' de la résistance lue.

Ulivethermocouple = np.array([1.675]) #résistance en ohm, montage 4 fils
Uliverrthermocouple = np.array([0.005]) #incertitude 'visuel' de la résistance lue.

### Données


T=np.array([96.05,90.5,85.07,80.24,74.97,70.58,65.15,60.59,55.08,50.71,44.55,40.37])
Terr= np.array([0.04]*len(T))

Rpt100 = np.array([135.41,133.50,131.71,130.03,127.99,126.41,124.40,122.74,120.68,119.06,116.98,115.55])
Rerrpt100 = np.array([0.05]*len(Rpt100))

Rthermistance = np.array([1094,1261,1467,1711,1981,2260,2668,3075,3662,4195,5065,5835])
Rerrthermistance = np.array([1]*(len(Rpt100)))

Uthermocouple = np.array([3.080,2.825,2.557,2.294,2.023,1.810,1.530,1.312,1.034,0.824,0.732,0.530])
Uerrthermocouple = np.array([0.005]*(len(Rpt100)))


### Pt100

xdata = T
xerrdata= Terr

ydata = Rpt100
yerrdata= Rerrpt100

xlive = np.array([])
xliverr = np.array([])
if len(Rlivept100)>0:
    xlive = Tlive
    xliverr = Tliverr

    ylive = Rlivept100
    yliverr = Rliverrpt100

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

ystr="Résistance [$\Omega$]"
xstr='Température [°C]'
titlestr="Résistance d'une Pt100 en fonction de la température"
ftsize=18

### Ajustement

def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

print("\n"+titlestr)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

### Affichage résultats sur l'invite de commande

print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
xtest = np.linspace(np.min(xdata),np.max(xdata),100)

plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
plt.plot(xtest,func(xtest,*popt),label='Ajustement ')
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

print("Résistance à 0 C : "+str(a)+" +- "+str(ua)+" Ohm")


### Thermistance

xdata = 1/(T+273.15)-1/(273.15+25)
xerrdata= Terr/(T+273.15)**2

ydata = np.log(Rthermistance)
yerrdata= Rerrthermistance/Rthermistance

xlive = np.array([])
xliverr = np.array([])
if len(Rlivethermistance)>0:
    xlive = 1/(Tlive+273.15)-1/(273.15+25)
    xliverr = Tliverr/(Tlive+273.15)**2

    ylive = np.log(Rlivethermistance)
    yliverr = Rliverrthermistance/Rlivethermistance

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

ystr="ln(Résistance/Ohm) []"
xstr='1/Température - 1/T0 [1/°C]'
titlestr="Résistance d'une thermistance en fonction de la température"
ftsize=18

### Ajustement

def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

### Affichage résultats sur l'invite de commande

print("\n"+titlestr)
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
xtest = np.linspace(np.min(xdata),np.max(xdata),100)

plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
plt.plot(xtest,func(xtest,*popt),label='Ajustement ')
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

kb = 1.38e-23
print("Gap = "+str(kb*b/1.6e-19)+" +- "+str(kb*ub/1.6e-19)+" eV")

### Thermocouple

xdata = T
xerrdata= Terr

ydata = Uthermocouple
yerrdata= Uerrthermocouple

xlive = np.array([])
xliverr = np.array([])
if len(Ulivethermocouple)>0:
    xlive = Tlive
    xliverr = Tliverr

    ylive = Ulivethermocouple
    yliverr = Uliverrthermocouple

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

ystr="Tension [mV]"
xstr='Température [°C]'
titlestr="Tension d'un thermocouple en fonction de la température"
ftsize=18

### Ajustement

def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

### Affichage résultats sur l'invite de commande

print("\n"+titlestr)
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
xtest = np.linspace(np.min(xdata),np.max(xdata),100)

plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
plt.plot(xtest,func(xtest,*popt),label='Ajustement ')
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

print("Température d'annulation, de la source froide = "+str(-a/b)+" +- "+str((-a/b)*np.sqrt((ua/a)**2+(ub/b)**2))+" C")




