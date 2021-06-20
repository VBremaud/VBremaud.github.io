
import xlrd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
def affine(x,a,b):
    return a*x+b
plt.close('all')


'''
DETERMINATION DE l'ORDRE GLOBAL
AUTHOR: TOM PEYROT & BENJAMIN CAR


'''

### Point en live

xlive=np.array([]) # Concentration en javel de la solution (mol/L)
ylive=np.array([]) # kapp mesuré par ajustement de l'absorbance

xliverr=np.array([])
yliverr=np.array([])

#xliverr=[]
#yliverr=[]

### Données
cmère= 0.43 #Concentration en javel (mol/L) déterminée par titrage
cfille=cmère*np.array([3,5,9,12])/20
kapp=np.array([0.00119,0.002876,0.004576,0.00567])

xdata=np.log(cfille)
ydata=np.log(kapp)

### Incertitudes

dcmère = 0.01
dcfille=cfille*(dcmère/cmère) # En supposant que l'incertitude sur le titrage est prépondérante, sinon c'est relou
dkapp=np.array([5e-7,1e-6,3e-6,4e-6])*100 # Incertitudes extraites des ajustements, *100 car sinon, largement sous-estimées ...

xerrdata=dcfille/cfille
yerrdata=dkapp/kapp


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

ystr='ln(kapp)'
xstr='ln([ClO-]_0) (mol/L)'
titlestr='Détermination de l/''ordre global de réaction'
ftsize=18

### Ajustement

def func(x,a,b):
    return a*x +b

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma='True')

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = ax  + b \na= " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,marker='o', color='b',mfc='white',ecolor='g',linestyle='',capsize=8,label='Preparation')
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


### Extraction des paramètres
k = np.exp(popt[1])
uk = np.exp(popt[1])*np.sqrt(pcov[1,1])

print('\nk = ' + str('%.3e'%k) + ' L/mol/s')
print('uk = ' + str('%.1e'%uk) + ' L/mol/s' )
# A comparer à la valeur du Lurin : 2.7e-2


print('Ordre partielle en CLOm='+str(a))
print ('Incertitude associée='+str(ua))

### Verification hypothèses


##% Conseil manip

