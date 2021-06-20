# -*- coding: utf-8 -*-
"""
@authour : Louis Heitz, Vincent Brémaud
"""


import numpy as np
import matplotlib.pyplot as plt

ftsize=18

#%% Mesure de la masse en eau du Calorimètre

M1=100
dM1=2# L'éprouvette utilisée n'était pas plus precise
T1=69
dT1=0.5 # La température peut évoluer et incertitude thermomètre
M2=400
dM2=5# Incertitude à l'éprouvette de 100mL
T2=19
dT2=0.5
Tf=30.7
dTf=0.2
m_ceau=M2*(T2-Tf)/(Tf-T1)-M1


''' Estimation de l'incertitude par la methode de Monte Carlo'''

N=10000
Meau1=np.zeros(N)
Teau1=np.zeros(N)
Meau2=np.zeros(N)
Teau2=np.zeros(N)
Tmelf=np.zeros(N)
mCalo=np.zeros(N)

for i in range(N):
    Meau1[i]=M1+dM1*np.random.randn()
    Teau1[i]=T1+dT1*np.random.randn()
    Meau2[i]=M2+dM2*np.random.randn()
    Teau2[i]=T2+dT2*np.random.randn()
    Tmelf[i]=Tf+dTf*np.random.randn()

mCalo=Meau2*(Teau2-Tmelf)/(Tmelf-Teau1)-Meau1

MC=np.mean(mCalo)
dMC=np.std(mCalo)
print('Masse en eau du calorimetre : '+str(MC) + ' g')
print('Incertitude associée : '+str(dMC))

# n, bins, patches = plt.hist(mCalo, 100, alpha=0.75)
# plt.xlabel('Masse en eau (g)')
# plt.ylabel('Occurrences')
# plt.title('Histogramme des valeurs simulées')
# plt.grid(True)
# plt.axvline(MC,color='r', linestyle='--')
# plt.show()

#%% Mesure de l'enthalpie de réaction

ceau=4.18

c = 0.1 # Concentration de la solution de Cuivre II
dc = 0.001 # Incertitude sur la concentration
v = 0.1 # Volume introduit dans le calorimetre
dv = 0.005 # Incertitude sur le volume.

msol = 0.1 # Masse de la solution. On approxime la masse volumique a celle de l'eau et 100mL =0.1 kg. L'erreur
#majeure réalisée ici consiste a ne pas prendre le chauffage de Zn qui represente 4g. En fait ca ne pose aucun souci car les capacité calorifique du Zinc est toute petite par rapport à celle de l'eau.
dmsol = 0.005
Ti = 22.1 # Température initiale
dTi =0.2 # Incertitude sur la température intiale
Tf = 26.5 # Température finale corrigée des pertes
dTf = 0.2 # Incertitude sur la température finale

'''
N.B Pour estimer la bonne température corrigées des pertes: Regarder le début de la réaction et tracer une frontière verticale. Prolonger la decroissance avec une oblique. Trop chiant sur pythin on le fait à la main. On voit ici qu'on a probablement sous estimé la tempéature finale ce qui est en accord avec le deltarH0 mesuré.
'''
N=10000
C=np.zeros(N)
V=np.zeros(N)
Msol=np.zeros(N)
MCsim=np.zeros(N)
Tfsim=np.zeros(N)
Tisim=np.zeros(N)

for i in range(N):
    C[i]=c+dc*np.random.randn()
    V[i]=v+dv*np.random.randn()
    Msol[i]=msol+dmsol*np.random.randn()
    Tisim[i]=Ti+dTi*np.random.randn()
    Tfsim[i]=Tf+dTf*np.random.randn()

Delta_rH = -1/(C*V)*(Msol+MCsim)*ceau*(Tfsim-Tisim)

DHmean=np.mean(Delta_rH)
DHstd=np.std(Delta_rH)

print('\nEnthalpie standard de réaction : '+str(DHmean) +' kJ/mol')
print('Incertitude associée : '+str(DHstd))

# A comparer à la valeur théorique : - 219 kJ/mol
Htab=-219
plt.figure(figsize=(12,9))
plt.hist(Delta_rH, 100, color='navy', edgecolor='darkred',alpha=0.75)
plt.axvline(x=Htab,color='k',linestyle='--',label='Valeur tabulée')
plt.xlabel('Enthalpie standard de réaction (kJ/mol)',fontsize=ftsize)
plt.ylabel('Occurrences',fontsize=ftsize)
plt.title('Histogramme des valeurs simulées',fontsize=ftsize)
plt.axvline(DHmean,color='r', linestyle='--',label='Valeur moyenne')
plt.legend(fontsize=ftsize)
plt.grid(True)
plt.show()