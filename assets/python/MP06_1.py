"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')


manip = 0 #0 = isothermes d'andrews, 1= pression de vapeur saturante en fonction de T, 2=chaleur latente

liste_couleur=['b','c','g','r','m','y','k']

### Données

Temp=np.array([47.1,30]) # En degré celcius
dTemp = np.array([0.1,0.2])

P1=np.array([10.25,10.75,11.25,12,13,14,15,16.5,18,20,22.5,25.5,28.75,32.75,36,41.5]) #En Bar
V1=np.array([3.85,3.7,3.5,3.25,3,2.75,2.5,2.25,2,1.75,1.5,1.25,1,0.75,0.5,0.25]) #En millilitre

P2=np.array([10.25,10.75,11.25,12,13,14,15,16.5,18,20,22.5,25.5,28.75,32.75,36,41.5])/2 #En Bar
V2=np.array([3.85,3.7,3.5,3.25,3,2.75,2.5,2.25,2,1.75,1.5,1.25,1,0.75,0.5,0.25])/2 #En millilitre

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

ydata=P/10**5 #en bar
xdata=V*10**6 #en mL



### Incertitudes

xerrdata=[]
yerrdata=[]
for k in range(len(P)):
    yerrdata.append(np.array([dP/1e5]*len(P[k])))
    xerrdata.append(np.array([dV*1e6]*len(V[k])))
xerrdata=np.array(xerrdata)
yerrdata=np.array(yerrdata)

# for k in range(len(P)):
#     xerrdata = np.array([np.array([dV]*len(xdata[0]))]*len(P))*10**6
# yerrdata = np.array([np.array([dP]*len(ydata[0]))]*len(P))/10**5

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

ystr='$P$ [Bar] '
xstr='$V$ [mL]'
titlestr="Isothermes d'Andrews"
ftsize=18

### Ajustement

def func(x,a,b):
    return a + b*x

popt,pcov=[],[]
for k in range(len(Temp)):
    debut=0
    fin=len(xfit[k])
    xfitk=xfit[k][debut:fin]
    yfitk=yfit[k][debut:fin]
    yerrk=yerr[k][debut:fin]
    poptk, pcovk = curve_fit(func, xfitk, yfitk,sigma=yerrk,absolute_sigma=True)
    popt.append(poptk)
    pcov.append(pcovk)

### Récupération paramètres de fit
"""
for k in range(len(Temp)):
    a,b=popt[k]
    ua,ub=np.sqrt(pcov[k][0,0]),np.sqrt(pcov[k][1,1])
    print("Pour T = " + str (Temp[k]) + '°C, on trouve : \n')
    print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
    print("ua = " + str(ua) + "\nub = " + str(ub) +'\n \n')
"""
### Tracé de la courbe

plt.figure(figsize=(10,9))
for k in range(len(Temp)):
    a,b=popt[k]
    T=Temp[k]
    col=liste_couleur[k]
    lab="T = " + str(T) + "°C"
    plt.errorbar(xdata[k],ydata[k],yerr=yerrdata[k],xerr=xerrdata[k],fmt='o',c=col,label=lab)
    #plt.plot(xfit[k],func(xfit[k],a,b),c=col)

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


### Psat(T)


Psat = np.array([30]) #à compléter
dPsat = np.array([1]) #à partir de la variation de Psat sur le plateau

Psatlive = np.array([35])
dPsatlive = np.array([1])
Templive = np.array([Temp[-1]])
dTemplive = np.array([dTemp[-1]])

xdata=Temp[:-1]
xerrdata=dTemp[:-1]

ydata=Psat
yerrdata=dPsat

xlive = np.array([])
xliverr = np.array([])
if len(Psatlive)>0:

    xlive=Templive
    xliverr=dTemplive

    ylive=Psatlive
    yliverr=dPsatlive

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

ystr='$P_{sat}$ [Bar]'
xstr='T [°C]'
titlestr='Pression de vapeur saturante en fonction de T'
ftsize=18

### Ajustement

def func(x,a,b):
    return a+ b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

print("\n"+titlestr)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

if manip==1:

    plt.figure(figsize=(10,9))
    xtest = np.linspace(np.min(xfit),np.max(xfit),100)

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

pente = b
dpente = ub

### Chaleur latente


vg = np.array([1.5])*1e-3
vl = np.array([0.5])*1e-3
dv = np.array([0.1])*1e-3* np.sqrt(2)

vglive = np.array([1])*1e-3
vllive = np.array([0.5])*1e-3
dvlive = np.array([0.1])*1e-3* np.sqrt(2)

ydata = pente * 10**5 * (Temp[:-1]+273.15)*(vg-vl)/1000
yerrdata = ydata * np.sqrt((dpente/pente)**2+(dTemp[:-1]/(Temp[:-1]+273.15))**2+(dv/(vg-vl))**2)

xdata = Temp[:-1]
xerrdata = dTemp[:-1]

xlive = np.array([])
xliverr = np.array([])
if len(vglive)>0:

    xlive=Templive
    xliverr=dTemplive

    ylive=pente * 10**5 * (Templive+273.15)*(vglive-vllive)/1000
    yliverr=ylive * np.sqrt((dpente/pente)**2+(dTemplive/(Templive+273.15))**2+(dvlive/(vglive-vllive))**2)

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

ystr='L [kJ/mol]'
xstr='T [°C]'
titlestr='Chaleur latente en fonction de la température avec Clapeyron'
ftsize=18

### Ajustement

def func(x,a,b):
    return a+ b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

print("\n"+titlestr)
a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

if manip==2:

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