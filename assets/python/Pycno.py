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
m1=33.409# pm 0.05 g (voir l'incertitude balance)

#Estimation de la masse avec CYCLOHEXANE dedans
m2=72.1922

#3. Déduction de la masse volumique du cyclohexane sachant le volume du pycnomètre.
Vpycno=50.398#
#mcyclo=m2-m1
rhoCyclo=0.777#mcyclo/Vpycno
print(rhoCyclo)

'''II] Estimation de la masse volumique de KCl
'''
# Mesure de la masse de NaCl introduite dans le pycno
m3=2.6329#g

#m3=5.51

#2. Mesure de la masse une fois le pycno rempli
mtot=74.065#g =m3+mcyclo+m1
mcyclo=mtot-m1-m3
Vcyclo=mcyclo/rhoCyclo

#3. Détermination de la masse volumique de NaCl
VKCl=Vpycno-Vcyclo

rhoKCl=m3/VKCl # En g/mL

rho=rhoKCl/10**6

Na=6.02*1e23
MK=39.1
MCl=35.45


a=(4*(MK+MCl)/(rhoKCl*Na))**(1/3)
a=10**10*a

print(a)

N=1000
dm=0.05
drho=0.01
RK=138
RCl=np.zeros(N)

for i in range(N):
    RCl[i]=((4*(MK+MCl)/((m3+dm*np.random.randn())/(Vpycno-((mtot+dm*np.random.randn())-(m1+dm*np.random.randn())-(m3+dm*np.random.randn()))/(rhoCyclo))*Na))**(1/3)*10**10)/2-RK





##II] Estimation de la masse volumique du KI

#Estimation de la masse du pycnomètre à vide.
m1=33.47# pm 0.05 g (voir l'incertitude balance)




rhoCyclo=0.777#mcyclo/Vpycno

m3=2.319#g


#2. Mesure de la masse une fois le pycno rempli
mtot=74.322#g =m3+mcyclo+m1
mcyclo=mtot-m1-m3
Vcyclo=mcyclo/rhoCyclo

#3. Détermination de la masse volumique de NaCl
VKI=Vpycno-Vcyclo

rhoKI=m3/VKI # En g/mL

rho=rhoKI/10**6

Na=6.02*1e23
MK=39.1
MI=126.9


a=(4*(MK+MI)/(rhoKI*Na))**(1/3)
a=10**10*a

print(a)

N=1000
dm=0.05
drho=0.01
RK=138
RI=np.zeros(N)

for i in range(N):
    RI[i]=((4*(MK+MI)/((m3+dm*np.random.randn())/(Vpycno-((mtot+dm*np.random.randn())-(m1+dm*np.random.randn())-(m3+dm*np.random.randn()))/(rhoCyclo))*Na))**(1/3)*10**10)/2-RK




##II] Estimation de la masse volumique du Sel

# Mesure de la masse de KBr introduite dans le pycno
m1=33.44# pm 0.05 g (voir l'incertitude balance)
dm=0.05



m3=1.7404#g
#m3=5.51

#2. Mesure de la masse une fois le pycno rempli
mtot=73.91#g =m3+mcyclo+m1
mcyclo=mtot-m1-m3
Vcyclo=mcyclo/rhoCyclo

#3. Détermination de la masse volumique de NaCl
VKBr=Vpycno-Vcyclo

rhoKBr=m3/VKBr # En g/mL

rho=rhoKBr/10**6

Na=6.02*1e23
MK=39.1
MBr=79.9


a=(4*(MK+MBr)/(rhoKBr*Na))**(1/3)
a=10**10*a
N=10
dm=0.05
RK=138


N=1000
RBr=np.zeros(N)

for i in range(N):
    RBr[i]=((4*(MK+MBr)/((m3+dm*np.random.randn())/(Vpycno-((mtot+dm*np.random.randn())-(m1+dm*np.random.randn())-(m3+dm*np.random.randn()))/(rhoCyclo))*Na))**(1/3)*10**10)/2-RK




## Tracé des résultats avec méthode de MC


plt.close('all')

## Synthèses
RClth=181
RBrth=196
RIth=220


plt.figure()
ax=plt.subplot()
ax.hist(RCl, 50, color='darkred', alpha=0.75, label='Chlorure',zorder=2)
ax.axvline(x=RClth,linestyle='--',color='r',label='Tabulé')
ax.hist(RBr, 50, color='navy', alpha=0.75,label='Bromure',zorder=1)
ax.axvline(x=RBrth,linestyle='--',color='b',label='Tabulé')
ax.hist(RI, 50, color='darkgreen', alpha=0.75, label='Iodure',zorder=0)
ax.axvline(x=RIth,linestyle='--',color='g',label='Tabulé')
plt.legend(loc='upper left')
ax.set_xlabel('Tirage des rayons ionique (pm)')
ax.set_ylabel('Nombre de tirage')
plt.show()