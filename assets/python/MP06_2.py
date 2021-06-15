"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Masse en eau du calorimètre

Tf=5.7
Tc=22.54
mf=47
mc=124.7
#Tm=19.5

T2=19.576
t2=56

T1=19.496
t1=35

pente= (T2 - T1)/(t2-t1)

T3=19.477 #Température minmiale
t3=30

t4=15 #Instant où l'eau est versée

Treel=T3-pente*(t3-t4)

Tm=Treel


mu  = mf*(Tm-Tf)/(Tc-Tm) -mc


#Incertitudes
dm = 0.1
dT = 0.1

N=1000
dmf=np.zeros(N)
dmc=np.zeros(N)
dTm=np.zeros(N)
dTf=np.zeros(N)
dTc=np.zeros(N)
Y=np.zeros(N)
for i in range(N):
    dmf[i]=mf+dm*np.random.randn()
    dmc[i]=mc+dm*np.random.randn()
    dTm[i]=Tm+dT*np.random.randn()
    dTf[i]=Tf+0.5*dT*np.random.randn()
    dTc[i]=Tc+0.5*dT*np.random.randn()
Y = dmf*(dTm-dTf)/(dTc-dTm) -dmc
dmu = np.std(Y)

print('\nMasse en eau mu = ' + str(mu) + ' +- ' + str(dmu) + ' g\n')


### Enthalpie de vaporisation

ml=102
mg=23.27

Tl=21.91
Tg=0.6

Tm2=13.13

cp=4.18

#Rumford


# (ml + mu)*cp*(Tm2 - Tl) + mg*cp*(Tm2 - Tg) + dH*mg = 0

#Tm2=13
#Attention si Tg <0 : réchauffement jusqu'à 9 : cp glacon.
L=-((ml + mu)*cp*(Tm2 - Tl) + mg*cp*(Tm2 - Tg))/mg

#Incertitudes
N=1000
dml=np.zeros(N)
dmg=np.zeros(N)
dMu=np.zeros(N)
dTm2=np.zeros(N)
dTl=np.zeros(N)
dTg=np.zeros(N)
Y=np.zeros(N)

dm = 0.1
dT = 0.1
for i in range(N):
    dml[i]=ml+dm*np.random.randn()
    dmg[i]=mg+dm*np.random.randn()
    dMu[i]=mu+dmu*np.random.randn()
    dTm2[i]=Tm2+dT*np.random.randn()
    dTl[i]=Tl+dT*np.random.randn()
    dTg[i]=Tg+dT*np.random.randn()
Y = -((dml + dMu)*cp*(dTm2 - dTl) + dmg*cp*(dTm2 - dTg))/dmg
dL= np.std(Y)

print('\nEnthalpie massique de vaporsation L = ' + str(L) + ' +- ' + str(dL) + ' J/g')
# ml=123.7
# mg=21.47
# Tl=21.52
# Tg=0.4
#
# Tm2= 14.22
# dH=-((ml + mu)*cp*(Tm2 - Tl) + mg*cp*(Tg - Tm2))/mg

