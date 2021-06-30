import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats

ftsize=18


### Point en live
Aexp=np.array([0.427])


V1=28# 28 mL de HNO3
V2=25# 25mL récupéré




# if len(Alive)>0:
#     ylive=Ulive+Uref
#     xliverr=np.array(np.sqrt((dV/Vlive)**2 + (dV0/V0fe2)**2+(DC02/C0fe2)**2 + (DC03/C0fe3)**2))
#     yliverr=np.array([0.1])
#
# else:
#     xlive=[]
#     ylive=[]
#     xliverr=np.array([])
#     yliverr=np.array([])

xlive=np.array([])
xliverr=np.array([])


### Données



c=np.array([0.05,0.02,0.01]) #Concentration en cu2+
A=np.array([0.822, 0.41,0.243]) #Absorbance mesurée, à 800 nm

dc=0.001+np.zeros(len(c))
dA=0.01+np.zeros(len(A))

xdata=c
ydata=A

### Incertitudes

xerrdata=dc
yerrdata=dA


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

ystr='$A$'
xstr='$[Cu^{2+}]$ [mol/L] '
titlestr="Courbe d'étalonnage"

### Ajustement

def func(x,a,b):
    return a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True,p0=(0.1,15))

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y = a  + b x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )
#print("r2 = " + str(r_value**2) )

mcu=(Aexp-popt[0])/popt[1]
M=63.54
csol=100*mcu
mcu=csol*V2*M*1e-3
dmcu=mcu*np.sqrt(pcov[0,0])/popt[0]

print('\nSoit mCu = '  +str(mcu[0]) +  ' +- ' + str(dmcu[0]) + ' g')

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(Aexp)>0:
    plt.errorbar((Aexp-popt[0])/popt[1],Aexp,fmt='o',label="Absorbance de l'échantillon")
plt.plot(xfit,func(xfit,  *popt),label='Ajustement linéaire ')
plt.title(titlestr,fontsize=ftsize)
plt.grid(True)
plt.xticks(fontsize=ftsize)
plt.yticks(fontsize=ftsize)
plt.legend(fontsize=ftsize)
plt.xlabel(xstr,fontsize=ftsize)
plt.ylabel(ystr,fontsize=ftsize)
plt.show()