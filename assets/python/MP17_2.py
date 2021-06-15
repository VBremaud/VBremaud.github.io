"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')
ftsize=18

### Point en live


Tlive=np.array([42.57]) #en degré celsius
Tliverr=np.array([0.04]) #incertitude de la notice 0.03 + 1 digit


Rlive=np.array([0.285]) #résistance en ohm, montage 4 fils
Rliverr=np.array([0.001]) #incertitude 'visuel' de la résistance lue.



### Données

T=np.array([20.16,25.29,30.20,35.26,40.12,45.11,50.09,55.15,60.02,65.07, 70.01])
Terr= np.array([0.04]*len(T))

R = np.array([0.2635,0.269,0.274,0.280,0.285,0.290,0.295,0.300,0.306,0.3105, 0.316])
Rerr = np.array([0.001]*(len(R)-1)+[0.002])

d=1e-3 #joue sur la valeur brut de la résistivité, à vérifier expérimentalement, paramètre important.>
deltad=0.03 # Mesuré au pied à coulisse
S=np.pi*(d/2)**2 #surface du cuivre en m^2
dS=S*np.sqrt(2)*deltad
L = 12.2 #longueur en mètre noté (ou mesuré connaissant le nombre de spire et le rayon d'une spire)



xdata=T
ydata = R * S / L #résistivité

xlive = Tlive
ylive = Rlive * S / L

### Incertitudes

xerrdata= Terr
yerrdata= Rerr * S / L

xliverr = Tliverr
yliverr = Rliverr * S / L

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

ystr='Résistivité [$\Omega$.m]'
xstr='Température [°C]'
titlestr='Résistivité du cuivre en fonction de la température'

### Ajustement

def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

### Affichage résultats sur l'invite de commande

print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )
print("On trouve alpha0  = " + str(b / (a + b * 20)) + "+-"+ str(ub / (a + b * 20))) #la pente vaut rho0 * alpha0 on divise donc par la résistivité rho0 à 20°C.

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()