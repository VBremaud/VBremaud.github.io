"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live

flive=800
Velive=100*1e-3
Vslive=350*1e-3

dflive=1
dVelive=1e-3
dVslive=1e-3

xlive=np.array([(2*np.pi*flive)**2])
ylive=np.array([(Vslive/Velive)**2])
xliverr=np.array([8*np.pi**2*flive*dflive])
yliverr=ylive*np.sqrt((2*dVelive/Velive)**2 + (2*dVslive/Vslive)**2)


xlive=np.array([])
ylive=np.array([])
xliverr=np.array([])
yliverr=np.array([])
### Données
'''

Z=47 # Zero par mesure au reglet en bas
x=np.array([100,80,70,60,50,49,48,46,45,44,43,42,40,30,20])
x=Z-x
U1=np.array([5.022,5.024,5.024,5.024,5.024,5.024,5.024,5.022,5.022,5.022,5.022,5.022,5.022,5.022,5.020]) # Tension excitatrice crête crête
U2=np.array([691,653,527,342,123,96,58,11,20,45,65,85,134,338,523])*1e-3 # Tension au borne de la bobine
R=102.5 #pm RLC metre
Omega=2*np.pi*500


plt.figure()
ax=plt.subplot()
ax.plot(x,U2/(U1*Omega/R),'bo')
ax.set_ylabel('M')
ax.set_xlabel('x(mm)')
'''

x0=47 #Position du zero.
x=np.array([100,80,70,60,50,49,48,46,45,44,43,42,40,30,20])
x-=x0

dx=np.array([0.5]*len(x))

U1=np.array([5.022,5.024,5.024,5.024,5.024,5.024,5.024,5.022,5.022,5.022,5.022,5.022,5.022,5.022,5.020]) #Tension d'entrée, crête à crête

U2=np.array([691,653,527,342,123,96,58,11,20,45,65,85,134,338,523])*1e-3 #Tension aux bornes de la bobine
R=102.5 #pm RLC metre

Omega=2*np.pi*500


dU1=np.array([0.005]*len(U1))
dU2=np.array([0.005]*len(U2))

xdata=x
ydata=U2/(U1*Omega/R)


### Incertitudes

xerrdata=dx

yerrdata=ydata*np.sqrt((dU2/U2)**2 + (dU1/U1)**2)



### Données fit


debut=0
fin=len(xdata)+1

if len(xlive) >0 :
    xlive=np.array(xlive)
    ylive=np.array(ylive)
    xfit=np.concatenate((xdata[debut:fin],xlive))
    yfit=np.concatenate((ydata[debut:fin],ylive))


if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata[debut:fin],xliverr))
    yerr=np.concatenate((yerrdata[debut:fin],yliverr))


if len(xliverr)== 0 :
    xerr=xerrdata[debut:fin]
    yerr=yerrdata[debut:fin]

if len(xlive) == 0 :
    xfit=xdata[debut:fin]
    yfit=ydata[debut:fin]


### Noms axes et titre

ystr=r'$M$ [H] '
xstr='$x$ [cm]'
titlestr='Capteur de position'

### Ajustement

def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr,absolute_sigma=True)


### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
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
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


###Extraction paramètres
#Us^2/Ue^2= (r/R)^2 + L^2 omega^2 / R^2


# A haute fréquence : comportement capacitif !!

r=R*np.sqrt(a)
L=R*np.sqrt(b)
ur=r*0.5*ua/a
uL=L*0.5*ub/b
print('\nSoit r = ' + str(r) + ' +- ' + str(ur) + ' Ohm')
print('\nEt L = ' + str(L) + ' +- ' + str(uL) + ' H')


