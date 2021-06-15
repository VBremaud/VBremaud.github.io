"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

plt.close('all')

### Valeurs fixées au début de l'expérience
z=np.array([0,15.65,50.55,78.4,109.8])*1e-2 # Ce sont les positions mesurées en prépartion. On considère que la première fourche est la position 0. Pour mesurer correctement, il s'agit d'ajuster les vis sous la plateforme non pas pour que celle ci soit droite mais surotut pour que les fourches optiques soit horizontales. On verifie avec un niveau à bulle. On peut aussi prendre un fil à plomb
dz=np.zeros(len(z))+1e-3 #incertitude de 1 mm sur la position de la fourche optique.
z+=1e-9 # Pour eviter la divergence.

debut=1 # Il faut enlever le premier point car si z(t)=1/2gt^2+vot+z0 alors pour diviser par t, il faut qu'il soit non nul, ce qui exclut le premier point. Physiquement, il faudrait le prendre en compte en mettant l'origine au niveau du depart mais on perdrait surement en precision. Bref.

### Point en live

tlive=np.array([0.120,80.78,200.06,272.13,340.78])*1e-3
dT = 100e-6 #Incertitude sur une mesure d'environ 300 microsecondes


if len(tlive) >0 :
    tlive=tlive-tlive[0]+1e-9 # Pour eviter la divergence.
    dtlive=np.zeros(len(tlive))+np.sqrt(2)*dT # Racine pour la propagation sur la difference de deux mesures.

    xdata=tlive
    ydata=z/tlive

    xerrdata=dtlive
    yerrdata=z*np.sqrt((dz/z)**2+(dtlive/tlive)**2)

    ystr='z/t [m/s]'
    xstr='t [s]'
    titlestr='Extraction de la valeur de g'
    ftsize=18

    def func(x,a,b):
        return a*x+b

    popt, pcov = curve_fit(func, xdata[debut:], ydata[debut:],sigma=yerrdata[debut:],absolute_sigma=True)
    alive,blive=popt
    ualive,ublive=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

    plt.figure(figsize=(10,9))
    xtest = np.linspace(np.min(xdata),np.max(xdata),100)

    plt.errorbar(xdata[1:],ydata[1:],yerr=yerrdata[1:],xerr=xerrdata[1:],fmt='o',label='Données')
    plt.plot(xtest,func(xtest,*popt),label='Ajustement ')
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()

    glive=2*alive
    dglive=2*ualive
    chi2red = np.mean((ydata[debut:] - func(xdata[debut:], *popt))**2/yerrdata[debut:]**2)

    print("y = ax  + b \na= " + str(alive) + "\nb = " + str(blive))
    print("ua = " + str(ualive) + "\nub = " + str(ublive) )

    print("glive = " + str(glive) + " +- "+ str(dglive) + " m/s^2")
    print("chi2 = "+ str(chi2red))



### Données

#mesure 1:
t1= np.array([0.120,80.78,200.06,272.13,340.78])*1e-3
t1=t1-t1[0]+1e-9
dT1 = 300e-6
dt1=np.zeros(len(t1))+np.sqrt(2)*dT1

xdata1=t1
ydata1=z/t1
yerrdata=z*np.sqrt((dz/z)**2+(dt1/t1)**2) #identique pour les autres pour faire simple

popt, pcov = curve_fit(func, xdata1[debut:], ydata1[debut:],sigma=yerrdata[debut:],absolute_sigma=True)
a1,b1=popt
ua1,ub1=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

#mesure 2:
t2=np.array([0,80.26,199.34,271.86,339.37])*1e-3
t2=t2-t2[0]+1e-9
xdata2=t2
ydata2=z/t2
popt, pcov = curve_fit(func, xdata2[debut:], ydata2[debut:],sigma=yerrdata[debut:],absolute_sigma=True)
a2,b2=popt
ua2,ub2=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

#mesure 3:
t3=np.array([0,80.16,198.34,272.86,339.77])*1e-3
t3=t3-t3[0]+1e-9
xdata3=t3
ydata3=z/t3
popt, pcov = curve_fit(func, xdata3[debut:], ydata3[debut:],sigma=yerrdata[debut:],absolute_sigma=True)
a3,b3=popt
ua3,ub3=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

#mesure 4:
t4=np.array([0,80.36,198.24,272.96,339.67])*1e-3
t4=t4-t4[0]+1e-9
xdata4=t4
ydata4=z/t4
popt, pcov = curve_fit(func, xdata4[debut:], ydata4[debut:],sigma=yerrdata[debut:],absolute_sigma=True)
a4,b4=popt
ua4,ub4=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

#mesure 5:
t5=np.array([0,80.76,199.14,271.86,340.27])*1e-3
t5=t5-t5[0]+1e-9
xdata5=t5
ydata5=z/t5
popt, pcov = curve_fit(func, xdata5[debut:], ydata5[debut:],sigma=yerrdata[debut:],absolute_sigma=True)
a5,b5=popt
ua5,ub5=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])

g=np.array([a1,a2,a3,a4,a5])*2
dg=np.array([ua1,ua2,ua3,ua4,ua5])*2


### Traitements

x=np.array([0,1,2,3,4]) #numéro des expériences à changer si besoin




### Noms axes et titre

ystr='g [m/s^2]'
xstr="Numéro de l'expérience []"
titlestr='Mesure statistique de g'
ftsize=18


### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(x,g,yerr=dg,fmt='o',label='Données préparation')
if len(tlive) >0 :
    plt.errorbar(len(x),glive,yerr=dglive,marker='s',color='k',mfc='darkred',ecolor='k',linestyle='',markersize=10,capsize=1,label='Point ajouté')
    g=np.concatenate((g,np.array([glive])))
    dg=np.concatenate((dg,np.array([dglive])))
    ar=np.concatenate((x,np.array([len(x)])))

plt.plot(ar,np.zeros(len(ar))+np.mean(g), color='black', linestyle='--',label='Moyenne ')
plt.fill_between(ar,np.mean(g)-np.std(g)/np.sqrt(len(g)),np.mean(g)+np.std(g)/np.sqrt(len(g)), color='yellow', alpha=0.5, label='Incertitude Stat')
plt.axhline(y=np.mean(g)-np.std(g)/np.sqrt(len(g)),color='k')
plt.axhline(y=np.mean(g)+np.std(g)/np.sqrt(len(g)),color='k')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()

print("\nMesure statistique de g")
print("g = " + str(np.mean(g)) + " +- "+ str(np.std(g)/np.sqrt(len(g))) + " m/s^2")









