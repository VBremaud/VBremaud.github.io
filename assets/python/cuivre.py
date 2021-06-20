import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18
def linear(x,a,b):
    return a*x+b


''' Piece de monnaie'''
V1=28# 28 mL de HNO3
V2=25# 25mL récupéré
# Le cuivre absorbe a 810 au max. La dillution est faite avec HNO3
c=np.array([0.05,0.02,0.01])
A=np.array([0.822, 0.41,0.243])
popt,pcov=curve_fit(linear,c,A)

Aexp=0.427 # Dilué 100 fois

FIT=linear(c,*popt)
x=(Aexp-popt[1])/popt[0]

plt.figure(figsize=(12,9))
ax=plt.subplot()
ax.grid(True)
ax.plot(c,A,'ro',label='Etalon')
ax.plot(c,FIT,'k--',label='ajustement')
ax.plot(x,Aexp,'bo',label='Point ajouté')
plt.legend(fontsize=ftsize)
ax.set_xlabel('c [mol/L]',fontsize=ftsize)
ax.set_ylabel('A [1]',fontsize=ftsize)
plt.show()

M=63.54
csol=100*x
m=csol*V2*M*1e-3
print('Soit mCu =' + str(m) + ' +- ' + str(m*np.sqrt(pcov[1,1])/popt[1]) + ' g')
