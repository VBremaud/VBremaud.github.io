import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

L=20e-3
a=10e-3
b=10e-3
I=4e-3

### Point en live

Ulive=110e-3-5e-3
Tlive=117

dUlive=1e-3
dTlive=1


xlive=np.array([1/(Tlive+273.15)])
ylive=np.array([np.log(Ulive/I)])


xliverr=np.array([dTlive/(Tlive+273.15)**2])
yliverr=np.array([dUlive/Ulive])
#xlive=[]
#ylive=[]


#xliverr=[]
#yliverr=[]

### Données




U=np.array([67,77,88,101,118,138,161,189,224,265,315,378,454,549,659,807,985,1210,1500,1875,2350])*10**(-3)-5e-3
T=np.array([135,130,125,120,115,110,105,100,95,90,85,80,75,70,65,60,55,50,45,40,35])

dU = np.array([1,1,1,2,2,2,2,3,3,3,4,5,8,8,10,15,15,20,35,35,50])*10**(-3)
dT = np.array([1]*len(dU))
sigma = U *L/(I*a*b)

xdata = 1/(T+273.15)
ydata= np.log(U/I)
###  Attention, mesurer Gamma au RLC mètre !!!!

### Incertitudes

xerrdata= dT/(T+273.15)**2
yerrdata= dU / U



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

ystr='ln($\sigma$) []'
xstr="1/T [1/K]"
titlestr="Conductivité en fonction de l'inverse de la température"

### Ajustement

def func(x,a,b):
    return  a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y =  a + b*x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )



### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
# plt.xlim(-0.025,0.1)
# plt.ylim(-2e-5,9e-5)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()