
"""
@Louis Heitz et Vincent Brémaud

"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live

xlive=[]
ylive=[]

#xlive=[]
#ylive=[]

xliverr=np.array([])
yliverr=np.array([])

#xliverr=[]
#yliverr=[]

### Données


ydata=np.array([2.7,4.02,5.80,7.92,10.63,14.07,17.65,21.25,25,28.6,29.62]) #Ue (V)
xdata=np.array([0.850,1.290,1.880,2.580,3.49,4.62,5.81,7.02,8.26,9.46,9.80]) #Uk (V)


xdata*=1000*2*np.pi/60/6 #Conversion tours/minutes en rad/s
### Incertitudes


xerrdata=np.array([0.01]*len(ydata))
yerrdata=np.array([0.02]*len(xdata))


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

ystr='$E$ [V]'
xstr='$\Omega$ [rad/s]'
titlestr="Détermination de K, constante de couplage électromécanique"

### Ajustement

noise=0*np.random.rand(1,len(yfit))


yfit= yfit+ noise
yfit=yfit[0]

def func(x,a,b):
    return a+b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',markersize=4,label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
#plt.axis([0,3.600,0,5])
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()