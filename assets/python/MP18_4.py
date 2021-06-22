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

lambdlive = np.array([690])*1e-9
dlambdlive = np.array([5e-9])

Photodlive = np.array([438])*1e-3
dPhotodlive = np.array([1e-3])

Pyroliveprep = np.array([4.45])*1e-3 #pas prendre le point en live mais utile dans l'analyse
dPyrolive = np.array([1e-4])

### Données

Manip=1

lambd=10**-9*np.array([600,620,640,660,680,700,720,740,760,780,800,820,840,860,880,900,920,940,960,980,1000,1020,1040,1060,1080,1100,1120,1140,1160,1180,1200])


Pyro=np.array([0.870,3.2,4,4.4,4.5,4.4,4.4,4.2,4,3.7,3.5,3.4,3.5,3.5,3.5,3.4,3.4,3.4,3.3,2.8,2.6,2.5,2.4,2.3,2.2,2.1,2,1.9,1.8,1.8,1.9])*1e-3 # Signal reçu après le monochromateur et hacheur optique à 1Hz
Photod=np.array([69,280,375,416,436,440,450,450,436,421,409,405,406,408,403,382,341,288,226,135,83,45,25,14.6,7.9,3.9,1.7,1.3,6.4,17.4,24.4])*1e-3 # Même signal sur photodiode.
dPyro=np.zeros(len(Pyro))+1e-4
dlambd=np.zeros(len(lambd))+5e-9
dPhotod=np.zeros(len(Photod))+1e-3

if Manip==0:
    plt.figure(figsize=(10,9))
    plt.errorbar(lambd,Pyro,yerr=dPyro,xerr=dlambd,fmt='o',label='Données')
    plt.title('Réponse du pyromètre',fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel("Longueur d'onde [nm]",fontsize=ftsize)
    plt.ylabel("Tension générée par le pyro [mV]",fontsize=ftsize)
    plt.show()

    plt.figure(figsize=(10,9))
    plt.errorbar(lambd,Photod,yerr=dPhotod,xerr=dlambd,fmt='o',label='Données')
    if len(lambdlive)>0:
        plt.errorbar(lambdlive,Photodlive,yerr=dPhotodlive,xerr=dlambdlive,fmt='o',label='Point ajouté')
    plt.title('Réponse de la photodiode',fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel("Longueur d'onde [nm]",fontsize=ftsize)
    plt.ylabel('Tension générée par la photodiode [mV]',fontsize=ftsize)
    plt.show()


if Manip==1:

    U=7e-3# Mesurer la tension obtenue pour une longueur d'onde choisie
    dU=1e-3
    R=1e3# Rentrer la valeur de la resistance choisie sur le calibre de la photodiode
    I=U/R # En deduire le courant
    dI=dU/R
    P=22.5*10**-6# Rentrer la puissance mesurée au puissance metre pour la même ongueur d'onde !! On a ainsi calibré la sensibilité à une longueur d'onde!
    dP=1e-6
    xdata=lambd
    xerrdata = dlambd

    ydata=Photod/Pyro
    MAX = np.max(ydata)
    ydata=ydata/MAX
    ydata=ydata*I/P # VOir commentaire ci dessous

    d1=Photod/Pyro*np.sqrt((dPhotod/Photod)**2+(dPyro/Pyro)**2)
    d2=ydata*I/P*np.sqrt((d1/(Photod/Pyro))**2+(dI/I)**2+(dP/P)**2)
    yerrdata=d2
    '''
    Ce dernier point est un peu complexe mais c'est un peu l'essence du montage. On suppose que le pyromètre possède une reponse spectrale plate sur le domaine spectral étudié. Il permet donc d'avoir acces au spectre de la lampe. On peut donc en divisant le signal obtenu avec la photodiode par celui obtenu sur le pyromètre avoir la caractéristique de la photodiode seule. Seulement, le signal obtenu est completement arbitraire en intensité. En normalisant par le max on a alors une valeur normalisée. Il suffit alors d'avoir une référence pour savoir la sensibilité en A/W. On mesure donc avec un puissance metre la valeur en puissance optique et la tension obtenue à la meme longueur d'onde pour avoir la sensibilité et on multiplie alors.
    '''

    ### Traitements

    xlive = np.array([])
    xliverr = np.array([])
    if len(lambdlive)>0:
        xlive = lambdlive
        xliverr = dlambdlive

        ylive = Photodlive/Pyroliveprep/MAX * I/P
        d1 = Photodlive/Pyroliveprep*np.sqrt((dPhotodlive/Photodlive)**2+(dPyrolive/Pyroliveprep)**2)
        d2 = ylive*I/P*np.sqrt((d1/(Photodlive/Pyroliveprep))**2+(dI/I)**2+(dP/P)**2)
        yliverr = d2

    if len(xliverr) >0 :
        xerr=np.concatenate((xerrdata,xliverr))
        yerr=np.concatenate((yerrdata,yliverr))


    if len(xliverr)== 0 :
        xerr=xerrdata
        yerr=yerrdata

    ### Données fit


    debut=0
    fin=12

    if len(xlive) >0 :
        xlive=np.array(xlive)
        ylive=np.array(ylive)
        xfit=np.concatenate((xdata[debut:fin],xlive))
        yfit=np.concatenate((ydata[debut:fin],ylive))


    if len(xlive) == 0 :
        xfit=xdata[debut:fin]
        yfit=ydata[debut:fin]


    ### Noms axes et titre

    xstr="Longueur d'onde [nm]"
    ystr='Sensibilite spectrale [A/W]'
    titlestr='Caractérisation spectrale de la photodiode'
    ftsize=12

    ### Ajustement

    def func(x,a,b):
        return a*x+b

    popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin+1],absolute_sigma=True)

    ### Récupération paramètres de fit

    a,b=popt
    ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
    print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
    print("ua = " + str(ua) + "\nub = " + str(ub) )

    ### Tracé de la courbe

    plt.figure(figsize=(10,9))
    xtest = np.linspace(np.min(xdata),np.max(xdata),100)

    plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
    plt.plot(xtest,func(xtest,*popt),label='Ajustement ')
    if len(xlive)>0:
        plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
    plt.axvline(x=950e-9,linestyle='--',color='k',label="Longueur d'onde de coupure")
    plt.title(titlestr,fontsize=ftsize)
    plt.grid(True)
    plt.xticks(fontsize=ftsize)
    plt.yticks(fontsize=ftsize)
    plt.legend(fontsize=ftsize)
    plt.xlabel(xstr,fontsize=ftsize)
    plt.ylabel(ystr,fontsize=ftsize)
    plt.show()



    h=6.62*10**-34
    c=3*10**8
    e=1.6e-19

    rend=a*h*c/e # Voir Diffon p158
    drend=ua*h*c/e
    print('Rendement = '+str(rend))
    print('Incertitude associe = '+str(drend))
