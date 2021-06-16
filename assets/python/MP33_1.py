"""
@Louis Heitz et Vincent Brémaud

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

L=57.6e-3
Rcircuit=10


dR=0.5
L=57e-3
C=500e-9


### Point en live


Rlive1=20
taulive1=0.00469897
dRlive1=50
dtaulive1=2e-5

Rlive2=2000
taulive2=910*1e-6
dRlive2=50
dtaulive2=5e-6


Rlive1+=Rcircuit
Rlive2+=Rcircuit

xlive1=np.array([1/Rlive1*np.sqrt(L/C)])
ylive1=np.array([taulive1])


xlive2=np.array([1/Rlive2*np.sqrt(L/C)])
ylive2=np.array([taulive2])

# xlive2=np.array([])
# xlive1=np.array([])
#xlive=[]
#ylive=[]

xliverr1=np.array([dRlive1/Rlive1**2])
yliverr1=np.array([1e-7])

xliverr2=np.array([dRlive2/Rlive2**2])
yliverr2=np.array([1e-7])
# xliverr2=np.array([])
# xliverr1=np.array([])
#xliverr=[]
#yliverr=[]

### Données


L=57.6e-3
Rcircuit=10


dR=0.5
L=57e-3
C=500e-9

# Grand Q

R=np.array([0,20,40,60,80,100])+Rcircuit
t1=np.array([1050,1050,1050,1050,1050,1050])*1e-6
y1=np.array([765,735,620,528,441,365])*1e-3

t2=np.array([3120,3120,3120,3120,3120,3120])*1e-6
y2=np.array([630,420,240,149,89,52])*1e-3

Deltat=t2-t1
dT=np.zeros(len(Deltat))+np.sqrt(2)*10e-6 # Lecture de la position du pic.
dy1=np.zeros(len(y1))+5e-3
dy2=2*dy1 # Car il est plus dur, ce pic est plus petit. On estime 2 fois plus d'incertitude.

tau1=(Deltat)/(np.log(y1/y2))
dtau1=tau1*np.sqrt((dT/Deltat)**2+(np.sqrt(2)*dy1/y1)**2)
Q1=1/R*np.sqrt(L/C)
dQ1=dR/R**2

#popt,pcov=curve_fit(linear,Q,tau,sigma=dtau,absolute_sigma=True)

#Petit Q

R2=np.array([2000,4000,6000,8000])+Rcircuit
dR2=50
tau2=np.array([912,1830,2780,3650])*1e-6# Tempps de montée à 63%
dtau2=np.zeros(len(tau2))+5e-6
y2=R2
Q2=1/R2*np.sqrt(L/C)
dQ2=dR2/R2**2



xdata1=Q1
ydata1=tau1

xdata2=Q2
ydata2=tau2
#xdata=xdata/1000

### Incertitudes

xerrdata1=dQ1
yerrdata1=dtau1

xerrdata2=dQ2
yerrdata2=dtau2




if len(xliverr1) >0 :
    xerr1=np.concatenate((xerrdata1,xliverr1))
    yerr1=np.concatenate((yerrdata1,yliverr1))

else:
    xerr1=xerrdata1
    yerr1=yerrdata1


if len(xliverr2) >0 :
    xerr2=np.concatenate((xerrdata2,xliverr2))
    yerr2=np.concatenate((yerrdata2,yliverr2))

else:
    xerr2=xerrdata2
    yerr2=yerrdata2




### Données fit


debut1=0
fin1=len(xdata1)+1

debut2=0
fin2=len(xdata2)+1

if len(xlive1) >0 :
    xfit1=np.concatenate((xdata1[debut1:fin1],xlive1))
    yfit1=np.concatenate((ydata1[debut1:fin1],ylive1))
else :
    xfit1=xdata1[debut1:fin1]
    yfit1=ydata1[debut1:fin1]


if len(xlive2) >0 :
    xfit2=np.concatenate((xdata2[debut2:fin2],xlive2))
    yfit2=np.concatenate((ydata2[debut2:fin2],ylive2))
else:
    xfit2=xdata2[debut2:fin2]
    yfit2=ydata2[debut2:fin2]





### Noms axes et titre

ystr=r'$\tau$ [s]'
xstr='$Q$ '
titlestr="Temps de réponse en fonction du facteur de qualité"

### Ajustement


def func(x,a,b):
    return a+b*x

def func2(x,a,b):
    return a/x+b

popt1, pcov1 = curve_fit(func, xfit1, yfit1,sigma=yerr1[debut1:fin1],absolute_sigma=True)
popt2, pcov2 = curve_fit(func2, xfit2, yfit2,sigma=yerr2[debut2:fin2],absolute_sigma=True)

xplot1=np.linspace(1,35,10000)
xplot2=np.linspace(0.04,0.4,10000)

### Récupération paramètres de fit

a,b=popt1
ua,ub=np.sqrt(pcov1[0,0]),np.sqrt(pcov1[1,1])
print('\n Ajustement à forte valeur de Q\n ')
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

# Pour grand Q :τ = 2Q/ω0
print('\n Soit omega0 = ' + str(2/b) + ' +- ' + str( 2*ub) + ' rad/s')

print('\n Valeur attendue : omega0 = ' + str(np.sqrt(1/(L*C))) + ' rad/s')

c,d=popt2
uc,ud=np.sqrt(pcov2[0,0]),np.sqrt(pcov2[1,1])
print('\n Ajustement à faible valeur de Q\n ')
print("y = c/x  + d \nc = " + str(a) + "\nd = " + str(b))
print("uc = " + str(uc) + "\nud = " + str(ud) +'\n')
#Pour petit Q : τ = 1/(ω0Q)

print('\n Soit omega0 = ' + str(1/c) + ' +- ' + str(uc) + ' rad/s')

print('\n Valeur attendue : omega0 = ' + str(np.sqrt(1/(L*C))) + ' rad/s')
### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata1,ydata1,yerr=yerrdata1,xerr=xerrdata1,fmt='o',markersize=4,label='Données Q > 1/2',c='blue')
plt.errorbar(xdata2,ydata2,yerr=yerrdata2,xerr=xerrdata2,fmt='o',markersize=4,label='Données Q < 1/2',c='red')
if len(xlive1)>0:
    plt.errorbar(xlive1,ylive1,yerr=yliverr1,xerr=xliverr1,fmt='o',label='Point ajouté',c='cyan')
if len(xlive2)>0:
    plt.errorbar(xlive2,ylive2,yerr=yliverr2,xerr=xliverr2,fmt='o',label='Point ajouté',c='green')
plt.plot(xplot1,func(xplot1,*popt1),c='blue')
plt.plot(xplot2,func2(xplot2,*popt2),c='red')
plt.axvline(x=0.5,color='k', linestyle='--',label='Q=1/2')
plt.semilogx()
plt.semilogy()
plt.title(titlestr,fontsize=ftsize)
plt.grid(True,which='both')
plt.xticks(fontsize=ftsize)
#plt.axis([0,3.600,0,5])
#plt.axis([0,xdata[-1]*1.05,0,ydata[-1]*1.05])
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()