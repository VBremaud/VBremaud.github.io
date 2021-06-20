import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def linear(x,a,b):
    return a*x+b

def expo(x,a,b):
    return a*np.exp(20000*b/x)
def poly(x,a,b,c):
    return a*x**2+b*x+c


import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
def linear(x,a,b):
    return a*x+b


plt.close('all')


### Point en live


xlive=np.array([])# Température mesurée en live
ylive=np.array([])# Resistance mesurée en live


xliverr=0.003*xlive+0.5
yliverr=np.array([0.3])

#xliverr=[]
#yliverr=[]

### Données
# Premeire tresistance infini
R=np.array([1000000,1000,800,600,400,300,200,100,50,10,5,1])
VZinc=np.array([-1.024,-1.013,-1.011,-1.007,-1,-0.992,-0.98,-0.952,-0.922,-0.868,-0.863,-0.852])
Vfer=np.array([-0.523,-0.532,-0.533,-0.536,-0.542,-0.548,-0.558,-0.588,-0.637,-0.720,-0.729,-0.740])
Ir=np.array([0,0.47,0.587,0.769,1.11,1.43,1.990,3.24,4.69,7.25,7.60,8.15]) # Tension aux bornes de la resistance
#Sans branchement,


xdata=Ir
ydata=VZinc
### Incertitudes
dI=np.zeros(len(Ir))+0.01
dVZinc=np.zeros(len(VZinc))+0.01

xerrdata=dI
yerrdata=dVZinc


if len(xliverr) >0 :
    xerr=np.concatenate((xerrdata,xliverr))
    yerr=np.concatenate((yerrdata,yliverr))


if len(xliverr)== 0 :
    xerr=xerrdata
    yerr=yerrdata

### Données fit


debut=0
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

ystr='Resistance (Ohm) '
xstr='Température thermomètre référence (degré)'
titlestr='Calibrage dune sonde de platine RPT100'
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x + b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,marker='o', color='b',mfc='white',ecolor='g',linestyle='',capsize=8,label='Preparation')
plt.errorbar(Ir,Vfer,yerr=dVZinc,xerr=xerrdata,marker='o', color='k',mfc='white',ecolor='g',linestyle='',capsize=8,label='Preparation')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,marker='o', markersize=8, color='k',mfc='darkred',ecolor='k',linestyle='',capsize=8,label='Point ajouté')
plt.plot(xfit,func(xfit,*popt), color='r', linestyle='-',label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()


### Extraction des paramètres du capteur

# Verification du fonctionnemen d'une PT100

print('Valeur de la resistance pour 0 degré')
print(b)
print(ub) # Bon c'est quand même pas loin

# Sensibilité
print('Sensibilité en Ohm/degre')
print(a)
print(ua)

### Verification hypothèses

'''

# L'ordonnée à l'origine est cohérente avec une PT1OO mais l'incertitude ne permet pas de rentrer dans le 100 exactement.
#Deux possibilité: problèmes d'équilibre thermique. On a pas composé l'auto-échauffement par effet Joule donc on trouve une temp un peu trop haute.

#Pour le coefficient directeur on retrouve également une sensibilité relative de l'ordre de celle attendue de 3.9e-3 C^{-1}, voir p341 Jolidon.


'''


##% Conseil manip

'''
Voir CR+Arnaud
'''








































