
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
plt.close('all')


'''
LECTURE D'UN FICHIER DU SPECTRO
AUTHOR: TOM PEYROT & BENJAMIN CAR

'''

def linear(x,a,b):
    return a*x+b

''' Importation fichier xlsc '''

document1 = xlrd.open_workbook("Solution 3.xlsx")

feuille_1 = document1.sheet_by_index(0)
cols = feuille_1.ncols
rows = feuille_1.nrows
X = []
Y= []

for r in range(18, rows-100):
    X += [feuille_1.cell_value(rowx=r, colx=0)]
    Y += [feuille_1.cell_value(rowx=r, colx=1)]



''' Détermination ordre partiel en Eb '''
X1 = np.log(1)+X
Y1=np.log(Y)

popt1,pcov1=curve_fit(linear,X1,Y1)
fit=linear(X1,*popt1)

ss_res = np.sum((Y1-fit)**2)
ss_tot = np.sum((Y1-np.mean(Y1))**2)
R2 = 1-ss_res/ss_tot

plt.figure()
size=14
ax=plt.subplot(132)
ax.set_title('Suivi cinétique de la décoloration',fontsize=18)
ax.plot(X1, Y1,marker='o',linestyle='',color='b', label = "Points expérimentaux")
ax.plot(X1,fit,'r--',label='Ajustement linéaire, \n R² = '+str('%.5f'%R2))
ax.legend(loc="upper right",fontsize=size)
ax.set_xlabel(r"temps (s)", fontsize=size)
ax.set_ylabel(r"ln[A]", fontsize=size)
plt.show()


print('\nkapp : ', popt1[0])
print('u(kapp) : ',np.sqrt(pcov1[0,0]))
print('\nR2 : ', R2)

# Le simple fait que ce soit une droite donne l'ordre 1 en Erythrosine.
# Le rapport des constantes donne l'ordre en Clo-.

#%% Tentatives d'ajustement différents : Ordre 0

X0 = np.log(1)+X
Y0=np.log(1)+Y

popt0,pcov0=curve_fit(linear,X0,Y0)
fit=linear(X0,*popt0)

ss_res = np.sum((Y0-fit)**2)
ss_tot = np.sum((Y0-np.mean(Y0))**2)
R2 = 1-ss_res/ss_tot

ax=plt.subplot(131)
ax.plot(X0, Y0,marker='o',linestyle='',color='b', label = "Points expérimentaux")
ax.plot(X0,fit,'r--',label='Ajustement linéaire,\n R² = '+str('%.5f'%R2))
ax.legend(loc="upper right",fontsize=size)
ax.set_xlabel(r"temps (s)", fontsize=size)
ax.set_ylabel(r"[A]", fontsize=size)
plt.show()

# print('\nkapp : ', popt0[0])
# print('u(kapp) : ',np.sqrt(pcov0[0,0]))
# print('\nR2 : ',R2)

#%% Tentatives d'ajustement différents : Ordre 2

X2 = np.log(1)+X
Y2=1/(np.log(1)+Y)

popt2,pcov2=curve_fit(linear,X2,Y2)
fit=linear(X2,*popt2)

ss_res = np.sum((Y2-fit)**2)
ss_tot = np.sum((Y2-np.mean(Y2))**2)
R2 = 1-ss_res/ss_tot

ax=plt.subplot(133)
ax.plot(X2, Y2,marker='o',linestyle='',color='b', label = "Points expérimentaux")
ax.plot(X2,fit,'r--',label='Ajustement linéaire,\n R² = '+str('%.5f'%R2))
ax.legend(loc="upper right",fontsize=size)
ax.set_xlabel("temps (s)", fontsize=size)
ax.set_ylabel("1/[A]", fontsize=size)
plt.show()


# print('\nkapp : ', popt2[0])
# print('u(kapp) : ',np.sqrt(pcov2[0,0]))
# print('\nR2 : ',R2)