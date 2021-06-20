import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ftsize=18

lamb_h=34.9
lamb_acide=4.1

### Point en live

xlive=[]
ylive=[]


xliverr=[]
yliverr=[]

### Données

V=np.array([0,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.35,1.5,1.7,1.9,2,2.2,2.45,2.6,3,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.55,4.65,4.8,4.9,5,5.1,5.35,5.5,5.7,6,6.3,6.5,7,7.6,8,8.5,9,9.45,10.5,11.5,12.5,13.55,14,14.5,14.6,14.7,14.8,15,15.1,15.2,15.3,15.4,15.5,15.6,15.75,15.95,16.1,16.22,16.4,16.5,16.6,16.7,16.8,17,17.2,17.4,17.6,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23.05,23.5,24.05,24.5,25])
pH=np.array([2.21,2.23,2.25,2.26,2.28,2.30,2.32,2.34,2.36,2.39,2.4,2.43,2.47,2.51,2.56,2.66,2.70,2.81,3.04,3.19,3.76,3.89,3.95,4.02,4.03,4.05,4.07,4.08,4.10,4.11,4.12,4.13,4.14,4.15,4.16,4.16,4.17,4.18,4.18,4.19,4.19,4.2,4.21,4.2,4.21,4.23,4.24,4.26,4.28,4.30,4.32,4.33,4.35,4.4,4.45,4.52,4.63,4.70,4.82,4.84,4.96,4.99,5.09,5.22,5.42,5.54,5.8,6.04,6.27,6.53,7.33,8.01,8.42,8.79,8.94,9,9.14,9.22,9.42,9.52,9.66,9.72,9.88,10,10.10,10.19,10.35,10.68,10.98,11.22,11.36,11.47,11.57,11.64,11.7,11.75,11.80])

# xdata=ci-sigma/(lamb_h+lamb_acide)
# ydata=(sigma/(lamb_h+lamb_acide))**2

xdata=V
ydata=pH

### Incertitudes

yerrdata=[]
for yi in ydata:
    if yi < 7 :
        yerrdata.append(0.01)
    if yi > 7 :
        yerrdata.append(0.02)

yerrdata=np.array(yerrdata)
xerrdata=np.array([0.05]*len(xdata))


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

ystr='pH'
xstr="Volume versé [mL]"
titlestr="Titrage des ions Al 3+ par la soude "

### Ajustement

def func(x,a,b):
    return  a + b*x

popt, pcov = curve_fit(func, xfit, yfit,sigma=yerr[debut:fin],absolute_sigma=True)

residuals = yfit- func(xfit, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((yfit-np.mean(yfit))**2)
r2= 1 - (ss_res / ss_tot)

### Récupération paramètres de fit

a,b=popt
ua,ub=np.sqrt(pcov[0,0]),np.sqrt(pcov[1,1])
print("y =  a + b*x \na = " + str(a) + "\nb = " + str(b))
print("ua = " + str(ua) + "\nub = " + str(ub) )
print("r2 = " + str(r2))


### Tracé de la courbe

plt.figure(figsize=(10,9))
plt.errorbar(xdata,ydata,yerr=yerrdata,xerr=xerrdata,fmt='o',label='Données')
if len(xlive)>0:
    plt.errorbar(xlive,ylive,yerr=yliverr,xerr=xliverr,fmt='o',label='Point ajouté')
# plt.plot(xfit,func(xfit,a,b),label='Ajustement ')
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