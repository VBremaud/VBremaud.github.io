"""
@Louis Heitz et Vincent Brémaud

"""
import matplotlib.pyplot as plt
import numpy as np


# Entrer les valeurs mesurées en live


alpha0=30
beta0=20

alpha=88
beta=62

ualpha=3
ubeta=3

alpha=(alpha-alpha0)*np.pi/180
beta=(beta-beta0)*np.pi/180

L=5.58 # Distance entre les deux gonios. Il pourrait être habile de les rapprocher. A voir, pas sur.
uL=0.05


ualpha*=np.pi/180
ubeta*=np.pi/180

gamma=np.pi-alpha-beta
ugamma=np.sqrt(ualpha**2+ubeta**2)

x=L*np.sin(alpha)/np.sin(gamma)
ux=x*np.sqrt((uL/L)**2+(ualpha*np.cos(alpha)/np.sin(alpha))**2+(ugamma*np.cos(gamma)/np.sin(gamma))**2)


print(' x = ' + str(x) + ' +- ' + str (ux) + ' m')