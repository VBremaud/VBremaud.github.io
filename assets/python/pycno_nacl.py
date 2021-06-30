import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

'''

L'idée est de mesurer une masse volumique précisemment pour en déduire un paramètre de maille.
Matériel nécessaire:
    -pycnomètre
    -eau distillée
    -balance de précision
    -copeaux de cuivre

I] Estimation initiale de la masse volumique de l'eau
'''

#Estimation de la masse du pycnomètre à vide.
m1=33.1150# pm 0.05 g (voir l'incertitude balance)

#Estimation de la masse avec CYCLOHEXANE dedans
m2=72.1922

#3. Déduction de la masse volumique du cyclohexane sachant le volume du pycnomètre.
Vpycno=50.276
mcyclo=m2-m1
rhoCyclo=mcyclo/Vpycno
#print(rhoCyclo)

'''II] Estimation de la masse volumique du Sel
'''
# Mesure de la masse de NaCl introduite dans le pycno
m3=6.88#g
#m3=5.51

#2. Mesure de la masse une fois le pycno rempli
mtot=76.55#g =m3+mcyclo+m1
mcyclo=mtot-m1-m3
Vcyclo=mcyclo/rhoCyclo

#3. Détermination de la masse volumique de NaCl
VNaCl=Vpycno-Vcyclo

rhoNaCl=m3/VNaCl # En g/mL

rho=rhoNaCl/10**6




'''
III] Utilisation du modèle cristallin pour en deduire le paramètre de maille
'''
Na=6.02*1e23
MNa=22.98
MCl=35.45

a=(4*(MNa+MCl)/(rhoNaCl*Na))**(1/3)
a=10**10*a

dm=0.1
dVcyclo=0.01
N=1000

ai=np.zeros(N)
rhoi=np.zeros(N)
m3i=np.zeros(N)
Vcycloi=np.zeros(N)
VNacli=np.zeros(N)

for i in range(N):
    Vcycloi[i]=Vcyclo+dVcyclo*np.random.randn()
    m3i[i]=m3+dm*np.random.randn()
    VNacli[i]=Vpycno-Vcycloi[i]
    rhoi[i]=m3i[i]/VNacli[i]
    ai[i]=10**10*(4*(MNa+MCl)/(rhoi[i]*Na))**(1/3)



## Tracé des résultats avec méthode de MC


plt.close('all')

## Synthèses
aClth=564


ftsize=18
plt.figure(figsize=(12,10))
ax=plt.subplot()
ax.hist(ai, 50, color='darkred', alpha=0.75, label='Chlorure',zorder=2)
ax.axvline(x=aClth,linestyle='--',color='r',label='Value tabulée')
ax.axvline(x=np.average(ai),linestyle='--',color='black',label='Value moyenne')
# ax.hist(RBr, 50, color='navy', alpha=0.75,label='Bromure',zorder=1)
# ax.axvline(x=RBrth,linestyle='--',color='b',label='Tabulé')
# ax.hist(RI, 50, color='darkgreen', alpha=0.75, label='Iodure',zorder=0)
# ax.axvline(x=RIth,linestyle='--',color='g',label='Tabulé')
plt.legend(loc='upper left',fontsize=ftsize)
ax.set_xlabel('Tirage des paramètres de maille (pm)',fontsize=ftsize)
ax.set_ylabel('Nombre de tirage',fontsize=ftsize)
plt.show()