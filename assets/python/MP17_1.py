"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')
ftsize=18

'''
-----EXPLICATION DU FONCTIONNEMENT DE LA MACHINE----

Prendre le generateur "ECHOSCOPE GS200"
Sortie 4 voies.

SORTIE 1: trigger, c'est une vraie merde.
SORTIE 2: Fenetre de filtrage (tout ce qui n'est pas dans cette fenetre prend une grosse attenuation) dont les 4 potards reglent les parametres
Typiquement, on peut régmler le delay par rappoort au signal emis, la gauteur de la fenetre une sorte de rampe...


On s'arrange donc pour trigger sur cette fenetre (signal le plus stable) puis on deplace la fenetre de sorte à ne garder que le signal et ses echos.
Le troisieme sortie est le signal emis mais on regarde plutôt le quatrieme qui est son enveloppe bcp plus belle. On peut moyenner;

Pour la sonde, plusieurs options sont possibles selon le mode que l'on veut réaliser. On peut prendre le mode 1/1 ,pour etudier la réflexion. Dans ce cas l'émetteur joue aussi le role de récepteur.
Dans le cas 1/2 (pour l'attenuation dans les fluides) il faurt mettre  la probe 2

Penser à mettree du gel pour adapter l'impedance!!!

Mesures:
'''




## Aluminium


'''
NB: le jour J, mesurer la masse volumique de l'alu en pesant et prenant toutes les mesures. Ici, D=3cm et L=7cm.
Ci dessous arrivée des différents echos (j'en mets que 2 c'est evident)
Pour le module d'young, calculer C et voir wikipedia pour une correction par un coefficient de poisson
'''
L=7e-2
DeltaT=22.4*1e-6

rho=2730
V=(2*L)/DeltaT

Ein=rho*V**2 # On voit que cette mesure surestime le module d'Young, on va appliquer les corrections dues aux coefficients de Poisson.

nu=0.346
EALU=Ein*(1+nu)*(1-2*nu)/(1-nu) # Formule tirée de https://fr.wikipedia.org/wiki/Module_d%27%C3%A9lasticit%C3%A9 entre le module de compressions des ondes P et le module d'Young.


N=1000
dL=1e-3
dT=1e-6
dnu=0.001
LMC=np.zeros(N)
DeltaTMC=np.zeros(N)
VMC=np.zeros(N)
nuMC=np.zeros(N)
EMC1=np.zeros(N)

for i in range(N):
    LMC[i]=L+dL*np.random.randn()
    DeltaTMC[i]=DeltaT+dT*np.random.randn()
    VMC[i]=2*LMC[i]/DeltaTMC[i]
    nuMC[i]=nu+dnu*np.random.randn()
    EMC1[i]=rho*VMC[i]**2*(1+nuMC[i])*(1-2*nuMC[i])/(1-nuMC[i])/1e9

print("Avec la propagation \n")
dV = V * np.sqrt((dL/L)**2+(dT/DeltaT)**2)
dEin = 2 * rho * dV * V
print("Valeur du module d'Young de l'aluminium en GPa:"+str(EALU/1e9)+" +- "+str(dEin/1e9 * (1+nu)*(1-2*nu)/(1-nu))+"\n")

print("Avec MC \n")
print("Valeur du module d'Young de l'aluminium en GPa:"+str(EALU/1e9)+" +- "+str(np.std(EMC1))+"\n")

plt.figure(figsize=(10,9))
ax=plt.subplot()
ax.hist(EMC1, 50, color='darkred', alpha=0.75)
ax.axvline(x=EALU/1e9,linestyle='-',color='black',label="Module d'Young moyen")
ax.axvline(x=EALU/1e9+np.std(EMC1),linestyle='--',color='black',label="Ecart type haut")
ax.axvline(x=EALU/1e9-np.std(EMC1),linestyle='--',color='black',label="Ecart type bas")
ax.set_xlabel('Tirage des modules dYoung (GPa)',fontsize=ftsize)
ax.set_ylabel('Nombre de tirage',fontsize=ftsize)
ax.set_title("Module d'Young de l'Aluminium",fontsize=ftsize)
ax.grid(True)
plt.gca()
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
ax.legend(fontsize=ftsize)
plt.show()

## Plexiglass


L=8e-2
DeltaT=59.5e-6

rho=1180
V=(2*L)/DeltaT
Ein=rho*V**2 # On voit que cette mesure surestime le module d'Young, on va appliquer les corrections dues aux coefficients de Poisson.

nu=0.415
EPlexi=Ein*(1+nu)*(1-2*nu)/(1-nu)


N=1000
dL=1e-3
dT=1e-6
dnu=0.001
LMC=np.zeros(N)
DeltaTMC=np.zeros(N)
VMC=np.zeros(N)
nuMC=np.zeros(N)
EMC2=np.zeros(N)

for i in range(N):
    LMC[i]=L+dL*np.random.randn()
    DeltaTMC[i]=DeltaT+dT*np.random.randn()
    VMC[i]=2*LMC[i]/DeltaTMC[i]
    nuMC[i]=nu+dnu*np.random.randn()
    EMC2[i]=rho*VMC[i]**2*(1+nuMC[i])*(1-2*nuMC[i])/(1-nuMC[i])/1e9

print("Avec la propagation \n")
dV = V * np.sqrt((dL/L)**2+(dT/DeltaT)**2)
dEin = 2 * rho * dV * V
print('Valeur du module dYoung du plexiglass en GPa:'+str(EPlexi/1e9)+" +- "+str(dEin/1e9 * (1+nu)*(1-2*nu)/(1-nu))+"\n")

print("Avec MC \n")
print('Valeur du module dYoung du plexiglass en GPa:'+str(EPlexi/1e9)+" +- "+str(np.std(EMC2))+"\n")

plt.figure(figsize=(10,9))
ax=plt.subplot()
ax.hist(EMC2, 50, color='navy', alpha=0.75)
ax.axvline(x=EPlexi/1e9,linestyle='-',color='black',label="Module d'Young moyen")
ax.axvline(x=EPlexi/1e9+np.std(EMC2),linestyle='--',color='black',label="Ecart type haut")
ax.axvline(x=EPlexi/1e9-np.std(EMC2),linestyle='--',color='black',label="Ecart type bas")
ax.set_xlabel('Tirage des modules dYoung (GPa)',fontsize=ftsize)
ax.set_ylabel('Nombre de tirage',fontsize=ftsize)
ax.set_title("Module d'Young du Plexiglass",fontsize=ftsize)
ax.grid(True)
plt.gca()
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
ax.legend(fontsize=ftsize)
plt.show()

## Cuivre
L=9e-2
DeltaT=40e-6

rho=8960
V=(2*L)/DeltaT
Ein=rho*V**2 # On voit que cette mesure surestime le module d'Young, on va appliquer les corrections dues aux coefficients de Poisson.

nu=0.33
ECu=Ein*(1+nu)*(1-2*nu)/(1-nu)


N=1000
dL=1e-3
dT=1e-6
dnu=0
LMC=np.zeros(N)
DeltaTMC=np.zeros(N)
VMC=np.zeros(N)
nuMC=np.zeros(N)
EMC3=np.zeros(N)

for i in range(N):
    LMC[i]=L+dL*np.random.randn()
    DeltaTMC[i]=DeltaT+dT*np.random.randn()
    VMC[i]=2*LMC[i]/DeltaTMC[i]
    nuMC[i]=nu+dnu*np.random.randn()
    EMC3[i]=rho*VMC[i]**2*(1+nuMC[i])*(1-2*nuMC[i])/(1-nuMC[i])/1e9

#En propageant simplement
print("Avec la propagation \n")
dV = V * np.sqrt((dL/L)**2+(dT/DeltaT)**2)
dEin = 2 * rho * dV * V
print('Valeur du module dYoung du Cuivre en GPa:'+str(ECu/1e9)+" +- "+str(dEin/1e9 * (1+nu)*(1-2*nu)/(1-nu))+"\n")

print("Avec MC \n")
print('Valeur du module dYoung du Cuivre en GPa:'+str(ECu/1e9)+" +- "+str(np.std(EMC3))+"\n")
plt.figure(figsize=(10,9))
ax=plt.subplot()
ax.hist(EMC3, 50, color='darkgreen', alpha=0.75)
ax.axvline(x=ECu/1e9,linestyle='-',color='black',label="Module d'Young moyen")
ax.axvline(x=ECu/1e9+np.std(EMC3),linestyle='--',color='black',label="Ecart type haut")
ax.axvline(x=ECu/1e9-np.std(EMC3),linestyle='--',color='black',label="Ecart type bas")
ax.set_xlabel('Tirage des modules dYoung (GPa)',fontsize=ftsize)
ax.set_ylabel('Nombre de tirage',fontsize=ftsize)
ax.set_title("Module d'Young du Cuivre",fontsize=ftsize)
ax.grid(True)
plt.gca()
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
ax.legend(fontsize=ftsize)
plt.show()

## Synthèses
plt.figure()
ax=plt.subplot()
ax.hist(EMC1, 50, color='darkred', alpha=0.75, label='Aluminium')
ax.hist(EMC2, 50, color='navy', alpha=0.75,label='Plexyglass')
ax.hist(EMC3, 50, color='darkgreen', alpha=0.75, label='Cuivre')
plt.legend(loc='upper left')
ax.set_xlabel('Tirage des modules dYoung (GPa)')
ax.set_ylabel('Nombre de tirage')
ax.set_title("Synthèse des modules d'Young")
plt.show()

