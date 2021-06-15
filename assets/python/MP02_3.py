"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')



### Point en live

Dlive=0.4*10
Ulive=1.1

dDlive=0.05*10
dUlive=0.005*2

xlive=np.array([Dlive]) # Poids mesuré en live
ylive=np.array([Ulive]) # Tension en V mesurée en live


xliverr=np.array([dDlive])
yliverr=np.array([dUlive])

#xliverr=[]
#yliverr=[]

### Données

'''
SET DE DONNEE 1, SUSPUCION SATURATION
D=np.array([0,1,2,3,4,5,6,7,8,9,10,11]) # Mesure de la distance entre les deux prismes de parafine.
dD=np.zeros(len(D))+0.5
T=np.array([2.94,2.85,2.55,2.19,1.63,0.907,0.410,0.202,0.125,0.060,0.050,0.007]) # Tension à l'oscillo.

dT=np.array([0.02,0.02,0.02,0.03,0.03,0.03,0.02,0.02,0.01,0.005,0.005,0.005]) # J'aurais tendance à penser que ca sature à 3V
dT=dT/max(T)
T=T/max(T)
'''

# D=np.array([0.5,2,3,4,5,6,7,8,9,10,11]) # Mesure de la distance entre les deux prismes de parafine.
# dD=np.zeros(len(D))+0.5
# T=np.array([1.99,1.71,1.39,0.995,0.682,0.363,0.202,0.119,0.062,0.032,0.013]) # Tension à l'oscillo.
#
# dT=np.zeros(len(T))+0.01 # J'aurais tendance à penser que ca sature à 3V
# dT=dT/max(T)
# T=T/max(T)


D=np.array([0,0.3,0.5,0.65,0.8,1.2])*10#/np.cos(np.pi/3)
dD=np.array([0.05,0.05,0.05,0.05,0.05,0.05])*10#/np.cos(np.pi/3)

U=np.array([1.98,1.47,0.905,0.295,0.170,0])
dU=np.array([0.005,0.005,0.005,0.005,0.005,0.005])*2

ylive=ylive/U[0]
U*=1/U[0]



xdata=D # On veut faire un capteur de force donc on multiplie par g
ydata=U
### Incertitudes


xerrdata=dD
yerrdata=dU


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

xstr='Distance entre les prisme [mm] '
ystr='Tension oscillo [V]'
titlestr="Décroissance de l'onde evanescente"
ftsize=18

### Ajustement

def func(x,B,d):
    return 1/np.sqrt(np.cosh(x/d)**2+B*np.sinh(x/d)**2)

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)
### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = 1/np.sqrt(np.cosh(x/d)**2+B*np.sinh(x/d)**2) \nd= " + str(a) + "\nB = " + str(b))
print("ud = " + str(ua) + "\nuB = " + str(ub) )

### Tracé de la courbe
xfitth=np.linspace(0,25,100)
fitth=func(xfitth,*popt)


plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Preparation')
plt.plot(xfitth,fitth,label='Ajustement ')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,xerr=xliverr,yerr=yliverr,fmt='o',label='Point ajouté')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


### Extraction des paramètres du capteur

#Delta
print('\nSoit delta =' + str(popt[1]) + ' +- ' + str(np.sqrt(pcov[1,1])) + ' mm')



# Retour à la longueur d'onde
d=popt[1]*1e-3
dd=np.sqrt(pcov[1][1])*1e-3
lamb=2.2e-2

angle=60
dangle = 5
n=np.sqrt((1+(lamb/(2*np.pi*d))**2))/np.sin(angle*np.pi/180)

N=1000

D = np.zeros(N)
ANGLE = np.zeros(N)
Y = np.zeros(N)

for i in range(N):
    ANGLE[i] = angle+dangle*np.random.randn()
    D[i] = d + dd*np.random.randn()
    Y[i] = np.sqrt((1+(lamb/(2*np.pi*D[i]))**2))/np.sin(ANGLE[i]*np.pi/180)

nerr = np.std(Y)

print('\nOn en déduit n = ' + str(n)+' +- '+str(nerr))












