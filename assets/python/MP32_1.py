"""
@Louis Heitz et Vincent Brémaud

"""


import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
def linear(x,a,b):
    return a*x+b


'''
Il n'y a pas particulierement de données ici. Cette première manip est plutôt la pour introduire les grandeurs et parametres pertinents du montage tout en montrant ses capacités experimentales.

I] Description du Setup

1) Deux pendules pesants
a) pendules équilibrés (lorsqu'ils ne sont pas couplés!) pour compenser le moment du poids de la tige (mais pas son moment d'inertie!)
b) On prend des pendules de même moment d'inertie total. Il est possible d'estimer J0 (de la mêe façon que MP01) et on prend alors
la même masse que l'on place au même endroit. NB: Oui, le moment d'inertie de la tige et total depend de l'endroit ou l'on se place.
c)On a un capteur angulaire qui permet de donner une image de l'angle.

II] Couplage entre les deux pendules.

1)

La première manip consiste à estimer le couplage entre les deux pendules. On prend le plus grand couplage en mettant entre les deux mandrins des perceuses la tige en laiton la plus rigide. Q: pourquoi plus rigide=plus de couplage ?
Pour mesurer ce couplage, on bloque un des pendules.

'''

##Mesurer de la constante de couplage

f0=542e-3 # Mesurer la periode à vide
df0=10e-3
f=644e-3 # Mesurer la periode avec couplage et autre pendule bloqué.
df=10e-3
m1=495e-3 # Masse ajoutée sur le pendule
g=9.81
l=43e-2# Longueur entre laxe de rotation et la masse.
dl=1e-2# Longueur entre laxe de rotation et la masse.

C=m1*g*l*((f/f0)**2-1)

'''
Faisons un MonteCarlo pour estimer l'incertitue sur C
'''

N=1000 # Propagation par MonteCarlo pour les incertitudes sur x !
f0sim=np.zeros(N)
fsim=np.zeros(N)
lsim=np.zeros(N)
Csim=np.zeros(N)
for i in range (N):
    f0sim[i]=f0+df0*np.random.randn()
    fsim[i]=f+df*np.random.randn()
    lsim[i]=l+dl*np.random.randn()
    Csim[i]=m1*g*lsim[i]*((fsim[i]/f0sim[i])**2-1)

n, bins, patches = plt.hist(Csim, 50, color='darkblue', alpha=0.75)

plt.axvline(x=C,color='r',linestyle='--')
plt.xlabel('C ($kg.m^2.s^{-2}$)')
plt.ylabel('Nombre doccurences')
plt.title('Histogramme des valeurs de C par méthode MC')
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#plt.xlim(40, 160)
#plt.ylim(0, 0.03)
plt.grid(True)
plt.show()


## Illustration des modes
'''
2) La deuxieme manip très qualitative permet d'illustrer ce qu'il faut illustrer:
- Le mode symétrique
-le mode antisymétrique.
On insiste bien sur le fait que les CI détermine le...conclure theoriquement.

Puis on dit que lorsque les CI sont quelconque, alors l'oscillation se décompose sur ces deux modes propres.
Pour le prouver on va utiliser un outil plus puissant la FFT.

On montre que f0 correspond au cas où les deux pendules oscillent en phase, c'est donc la même formule.
On mesure donc la fréquence antisymetrique '''


fas=724e-3
dfas=10e-3

fasth=f0*np.sqrt(1+2*C/(m1*l*g))
print(fasth) # On verifie bien le modèle dans les barres d'erreur!



'''

Transition sur le montage suivant, (on pouvait pas faire de réponse impulsionnelle ici. On va faire un coulage électronique.)



'''

