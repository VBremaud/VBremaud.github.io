'''

@author : Louis Heitz, Vincent Brémaud


'''

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

grossissement = 33e-2/18e-3

### Point en live

hlive=34.8e-2
Blive=400e-3

dhlive=0.1e-2
dBlive=1e-3

hlive=hlive/grossissement
dhlive=dhlive/grossissement

xlive=np.array([Blive**2])
ylive=np.array([hlive**2])

xliverr=np.array([2*dBlive*Blive])
yliverr=np.array([dhlive])


### Données

m_Fe=12.80 #En gramme

meau=50 #g

mtot=m_Fe+meau
tm=m_Fe/mtot

tm*=1/3
# 42 cm <-> 4 mL

I=np.array([0,200.8,402,594,812,1041,1206,1405,1604,1833,2010,2252])*1e-3

h_ecran=np.array([34.2,34.3,34.5,34.7,34.9,35.1,35.3,35.6,35.8,36.2,36.7,37.5])*1e-2

grossissement = 33e-2/18e-3 #18 graduations

h=h_ecran/grossissement

h-=h[0]


Itab=np.array([4,154,379,585,734,985,1250,1550])*1e-3 # En ampere

Btab=np.array([30,94,203,309,383,500,592,710])*1e-3 # Notez le champ rémanent de 39 mT


def func(x,a,b):
    return a + b*x

uB=[5e-3]*len(Btab)
popt2,pcov2 = curve_fit(func, Itab, Btab,sigma=uB,absolute_sigma=True)

a2,b2=popt2

B = a2 + b2*I

xdata=B**2
ydata= h

plt.figure()
plt.plot(Itab,Btab,'o')
plt.show()

mu0=4*np.pi*1e-7

s=4e-7/(42e-2/grossissement)

S=30e-7/(2.4e-2)


### Incertitudes

xerrdata=np.array(b2*2*5e-3*I)
yerrdata=np.array([1e-3/grossissement]*len(ydata))




### Données fit


debut=2
fin=8

if len(xlive) >0 :
    xlive=np.array(xlive)
    ylive=np.array(ylive)
    xfit=np.concatenate((xdata[debut:fin],xlive))
    yfit=np.concatenate((ydata[debut:fin],ylive))


if len(xlive) == 0 :
    xfit=xdata[debut:fin]
    yfit=ydata[debut:fin]


if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata[debut:fin],xliverr))
    yerr=np.concatenate((yerrdata[debut:fin],yliverr))


if len(xliverr)== 0 :
    xerr=xerrdata[debut:fin]
    yerr=yerrdata[debut:fin]
### Noms axes et titre

ystr='$h$ [m]'
xstr='$B^2$ [$T^2$]'
titlestr='Variation de hauteur en fonction du champ magnétique appliqué'

### Ajustement

def func(x,a,b):
    return a+ b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr,absolute_sigma=True)



### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

rhosol=1000*(12.8 + 50)/(50)
g=9.81

chisol=b*2*mu0*rhosol*g*(1+s/S)

Msel=278 # g/mol
rhosel=1.895 # g / cm3

chiseltab=1.12e-2 + 10200*1e-6  #cm3/mol
chiseltab*=rhosel/Msel

rhosel=1895
chieau=-9e-6
rhoeau=1000
chisel=rhosel*chisol/(rhosol*tm)#E+(1-1/tm)*(rhosel*chieau/rhoeau)

N=1000
dchisol=chisol*ub/b
dtm=0.01

tmi=np.zeros(N)
chisoli=np.zeros(N)
chiseli=np.zeros(N)
for i in range(N):
    chisoli[i]=chisol+dchisol*np.random.randn()
    tmi[i]=tm + dtm*np.random.randn()

chiseli=rhosel*chisoli/(rhosol*tmi)

plt.figure()
plt.hist(chiseli, 50, color='salmon',edgecolor='darkred', alpha=0.75)
plt.show()
uchisel=np.std(chiseli)
print('Soit chi sel=( '+ str(chisel*1e3) + ' +- ' + str(uchisel*1e3) + ' ) x 10^(-3)')
### Tracé de la courbe

plt.figure(figsize=(12,9))
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