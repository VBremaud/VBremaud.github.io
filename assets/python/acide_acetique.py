import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

lamb_h=34.9*10
lamb_acide=4.1*10

### Point en live

ci_live=5

dci_live=0.1

sigma_live=500

dsigma_live=1



xlive=np.array([ci_live-sigma_live/(lamb_h + lamb_acide)])
ylive=np.array([(sigma_live/(lamb_h + lamb_acide))**2])

xlive=np.array([ci_live])
ylive=np.array([sigma_live])



xliverr=np.sqrt((dci_live/ci_live)**2 + (dsigma_live/sigma_live)**2)*xlive
yliverr=np.array([2*sigma_live*dsigma_live/((lamb_h+lamb_acide))**2])


xlive=[]
ylive=[]
xliverr=[]
yliverr=[]

### Données

ci=np.array([0.5,0.1,0.01,0.005])

dci=np.array([0.1]*len(ci))

sigma=np.array([1082,514,159,112])/1000
dsigma=np.array([1]*len(sigma))/1000

xf=sigma/(lamb_acide+lamb_h)

xdata=ci
ydata=1e5*xf**2/(ci-xf)
# xdata=ci-sigma/(lamb_h+lamb_acide)
# ydata=(sigma/(lamb_h+lamb_acide))**2


### Incertitudes

xerrdata=dci
dxf=dsigma/((lamb_h+lamb_acide))
yerrdata=2*dxf*ydata/xf*1e1


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

ystr='$Q$ * 10^5'
xstr="$C_i$ [mol/L]"
titlestr="Détermination du Ka de l'acide acétique"

### Ajustement

def func(x,a):
    return  a

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

residuals = yfit- func(xfit, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((yfit-np.mean(yfit))**2)
r2= 1 - (ss_res / ss_tot)

### Récupération paramètres de fit

a=popt[0]
ua=np.sqrt(pcov[0,0])
print("y =  a \na = " + str(a))
print("ua = " + str(ua))


pKa=-np.log10(a*1e-5)

print("pKa = " + str(pKa))

print("u(pKa) = pKa * u(a)/a = " + str(pKa*ua/a))

### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
plt.plot(xfit,[a]*len(xfit),label='Ajustement ')
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