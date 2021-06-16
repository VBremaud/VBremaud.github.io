import matplotlib.pyplot as plt
import numpy as np


# En preparation utiliser la macro IGOR
# Acquerir le signal de l'oscillo sur une bonne base de temps sans moyenner. Simplement faire le spectre et venir regarder la bande
# Choisir les deux curseurs entre des pics (de façon symetrique) et utiliser la fonction POWER Ration CH1. Cette macro va calculer
# Completement tout seul la fraction de pusisance englobée entre les deux curseurs. On englobe plus. Lorsque l'on depasse, on prend le pic d'avant:


### En direct

GdB=np.array([2.5,-2.5,-13.75,-29.38,-46.87])
N_pic=np.array([0,1,2,3,4])
Veff2=10**(GdB/10)



### Traitement


E=0
for i in range(len(GdB)):
    if i==0:
        E+=Veff2[i]
    else:
        E+=2*Veff2[i]


Efrac=[]
for i in range(len(GdB)):
    if i==0:
        Efrac.append(Veff2[0])
    else:
        print(Veff2[1:i+1])
        Efrac.append(Veff2[0] + 2*sum(Veff2[1:i+1]))

Efrac=np.array(Efrac)/E


dEfrac=0.01

### Affichage
xstr='Numéro du pic'
ystr=r'Fraction de la pusisance totale'
titlestr='Détermination de la  bande de Carson'

xplot=np.linspace(-0.1,4.5,5)
ftsize=18

plt.figure(figsize=(10,9))
plt.errorbar(N_pic,Efrac,yerr=[dEfrac]*len(Efrac),fmt='o',label='Energie sommée')
plt.plot(xplot,[0.98]*len(xplot),'--',label="98% de l'énergie totale")
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


