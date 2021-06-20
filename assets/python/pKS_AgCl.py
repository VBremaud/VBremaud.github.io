import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

### Point en live


Elive=88e-3 #/!\ Se placer après équivalence
Vlive=9.5

dElive=1e-3
dVlive=0.05

V0=20
c=1e-1
c0=2e-2

Clive=(c*Vlive-c0*V0)/(V0+Vlive)




I=(c*Vlive+c0*V0)/(V0+Vlive)
log_gammacl=0.5046*np.sqrt(I)/(1+0.819*np.sqrt(I))


xlive=np.array([np.log(Clive)])
ylive=np.array([Elive])



xliverr=xlive*dVlive/Vlive
yliverr=np.array([dElive])

#xliverr=[]
#yliverr=[]

### Données

E=np.array([443,438,434,430,423,417,407,392,285,144,123,117,109,105,101,95,90,86])*1e-3#20 mL au lieu de 25 dans le Fosset

V_verse=np.array([0,0.5,1,1.5,2,2.5,3,3.55,4,4.5,5.1,5.5,6,6.5,7,8,9,10])

dV_verse=np.zeros(len(V_verse))+0.05
dE=np.zeros(len(E))+1e-3
E_Ag=0.800

E_ECS=0.240

V0=20
c=1e-1
c0=2e-2
C_Cl=(c*V_verse-c0*V0)/(V0+V_verse)

I=(c*V_verse+c0*V0)/(V0+V_verse)
log_gammacl=0.5046*np.sqrt(I)/(1+0.819*np.sqrt(I))

ydata=E
xdata=np.log(C_Cl)



### Incertitudes

xerrdata=xdata*dV_verse/V_verse
yerrdata=dE


if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata,xliverr))
    yerr=np.concatenate((yerrdata,yliverr))


if len(xliverr)== 0 :
    xerr=xerrdata
    yerr=yerrdata

### Données fit


debut=9
fin=len(xdata)+1

if len(xlive) >0 :
    xlive=np.array(xlive)
    ylive=np.array(ylive)
    xfit=np.concatenate((xdata[debut:fin],xlive))
    yfit=np.concatenate((ydata[debut:fin],ylive))


if len(xlive) == 0 :
    xfit=xdata[debut:fin]
    yfit=ydata[debut:fin]


### Noms axes et titre

ystr='$E$ [V] '
xstr='log([$Cl^-$])'
titlestr='Différence de potentiel en fonction du volume versé'

### Ajustement

def func(x,a,b):
    return a+ b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

ln_Ks=np.average((a-(E_Ag-E_ECS))*96500/(8.314*298) + log_gammacl)
uln_Ks=np.std((a-(E_Ag-E_ECS))*96500/(8.314*298) + log_gammacl)

#uln_Ks=ln_Ks*ua/a


print("\nOn trouve pKs = " +str(-ln_Ks/np.log(10) ) +'\nEt u(pKs) = ' + str(uln_Ks/np.log(10)))
### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
# plt.xlim(-0.025,0.1)
# plt.ylim(-2e-5,9e-5)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()