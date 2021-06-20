# -*- coding: utf-8 -*-
"""
Created on Fri May 21 14:34:54 2021

@author: Vincent Brémaud et Louis Heitz
"""
import matplotlib.pyplot as plt
import numpy as np

plt.close('all')

meau = 3454 #masse d'eau introduite (g)
mcal=241 #masse en eau du calorimètre (g)
meth = (34.00-29.2)*0.96 # Masse d'éthanol brulée (g), le coeff 0.96 prend en compte que l'éthanol n'est pas pur
Ti=20.75+273 #Température initiale à 14h10min30
Tf=29.16+273 #Température finale à 14h19min15
t=8*60+45 #Délais entre les deux mesures (s)
ceau = 4185

dmeau = 5
dmcal = 10
dmeth = 0.05
dTi = 0.02
dTf = 0.02
dt=1

#%% Propagation par Monte-Carlo

N=10000
Meau=np.zeros(N)
Mcal=np.zeros(N)
Meth=np.zeros(N)
TI=np.zeros(N)
TF=np.zeros(N)
T=np.zeros(N)

for i in range(N):
    Meau[i]=meau+dmeau*np.random.randn()
    Mcal[i]=mcal+dmcal*np.random.randn()
    Meth[i]=meth+dmeth*np.random.randn()
    TI[i]=Ti+dTi*np.random.randn()
    TF[i]=Tf+dTf*np.random.randn()
    T[i]=t+dt*np.random.randn()

PC_temp=ceau*(Meau+Mcal)*(TF-TI)/Meth*1e-6 #Conversion en MJ/kg
PC_moy = np.mean(PC_temp)
PC_std = np.std(PC_temp)

plt.figure()
n, bins, patches = plt.hist(PC_temp, 100, color='green', edgecolor='darkgreen', alpha=0.75)
plt.xlabel('Pouvoir calorifique (MJ/kg)')
plt.ylabel('Occurrences')
plt.title('Histogramme des valeurs simulées')
plt.axvline(PC_moy,color='r', linestyle='--')
plt.grid(True)
plt.show()

print('\nPC = ' + str('%.3f'%PC_moy + ' MJ/kg'))
print('Incertitude = ' + str('%.1f'%PC_std + ' MJ/kg'))
#A comparer à la valeur théorique 1.367e6/46.07e-3 = 29.67 MJ/kg


'''
Pour vidanger prendre un tuyau.
Mettre le tuyau petit a petit en spiral.
Immerger le tube. Et boucher avec le doigt.
Ressortir et

'''