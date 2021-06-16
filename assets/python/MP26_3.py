"""
@Louis Heitz et Vincent Brémaud

"""

import matplotlib.pyplot as plt
import numpy as np
import os

ftsize=18


# Rentrer la valeur du nombre de cannulure-1 des deux longueurs d'onde:

Can=20.
L1mes=535.0*1e-9 # Essayer au maximum de garder ces valeurs de longueur d'onde là ou l'indice est tabulé.
L2mes=588.0*1e-9


N=3000

L1=np.zeros(N)
L2=np.zeros(N)
n=np.zeros(N)
result=np.zeros(N)
sigmaL1=0.3*1e-9
sigmaL2=0.3*1e-9

sigman=0.0
n2=1.5230 #@ 546.1 nm
n1=1.5255 #@ 589.1 nm

for i in range(N):
    L1[i]=L1mes+sigmaL1*np.random.randn()
    L2[i]=(L2mes+sigmaL2*np.random.randn())

result=-(Can-1)/(2*(n2-1)/L2-2*(n1-1)/L1)*1e6
resultt=-(Can-1)/(2.*(n2-1)/L2mes-2.*(n1-1)/L1mes)*1e6


#print('Epaisseur mesuree en micrometre :',resultt)




# the histogram of the data
plt.figure()
plt.hist(result, 50, color='salmon',edgecolor='darkred', alpha=0.75)
plt.axvline(x=np.mean(result),linestyle='--', color='b')
plt.xlabel('Epaisseurs [micrometre]',fontsize=ftsize)
plt.ylabel('Probabilite',fontsize=ftsize)
plt.title('Histogramme des épaisseurs simulees',fontsize=ftsize)
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#plt.xlim(40, 160)
#plt.ylim(0, 0.03)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.grid(True)
#plt.savefig(r'Histogram.pdf')
plt.show()

print('Epaisseur mesurée en micrometre :',np.mean(result))
print('Incertitude estimée en micrometre :',np.std(result))


