#-----------------------------------------------------------------------
# Diagramme binaire
#-----------------------------------------------------------------------
# Renseignements/bugs : Guillaume Dewaele <agreg(at)sci-phy.org>
#-----------------------------------------------------------------------

# Paramètres modifiables

titre = "Diagramme binaire Thymol et Acide Palmitique"

# Espèce 1

E1 = r"$Thy_{ sol}$"  # Nom
M1 = 150.22e-3        # Masse molaire, g/mol
Tf1 = 50            # Température de fusion, °C
DH1 = 17.54e3          # Enthalpie de fusion, kJ/kg
col1 = 'g'             # Couleur sur le graphe

# Espèce 2

E2 = r"$A_{Pal, sol}$" # Nom
E2r = r"$A_{Pal}$"     # Nom (abscisses)
M2 = 265.4e-3        # Masse molaire, g/mol
Tf2 = 62.9            # Température de fusion, °C
DH2 = 51.02e3          # Enthalpie de fusion, kJ/kg
col2 = 'b'             # Couleur sur le graphe

# Solide

col3 = 'r'             # Couleur sur le graphe

# Utiliser fraction massique ?

massique = True

# Annotation liquidus

xsol = [ 0.23, 0.9 ]

# Points supplémentaires
# (fraction, température, err_fraction, err_temperature, couleur)

points = [
  ('k', [ (0, 48.2, 0.05, 4.0),
          (0.231, 45.57, 0.05, 2.0),
          (1, 62, 0.05, 3.0),
          (0.631, 52.3, 0.05, 3.5) ]),
    ('r', [ (0.231, 37.71, 0.05, 2.0),(0.350, 39.4, 0.05, 3.0),(0.631, 35.53, 0.05, 3.5) ]),
  ('b', [ (0.631, 52.3, 0.05, 3.5)])
]

#-----------------------------------------------------------------------

# Bibliothèques utilisées

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import bisect
import matplotlib.pylab as plb

#-----------------------------------------------------------------------

memParams = plb.rcParams

plb.rcParams.update(
  { 'legend.fontsize' : 'medium',
    'axes.labelsize' : 'medium',
    'axes.titlesize' : 'medium',
    'xtick.labelsize' : 'medium',
    'ytick.labelsize' : 'medium',
    'font.size' : 12 })

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    matplotlib.interactive(False)

#-----------------------------------------------------------------------

R = 8.314

def _id(x) :
    return x

def _w(x) :
    return x*M2/(M1+x*(M2-M1))

w = _w if massique else _id

def T1(x) :
    return (Tf1+273.15)/(1-np.log(1-x)*R*(Tf1+273.15)/DH1)-273.15

def T2(x) :
    return (Tf2+273.15)/(1-np.log(x)*R*(Tf2+273.15)/DH2)-273.15

def DeltaT(x) :
    return T1(x) - T2(x)

# Calcul du point E

xE = bisect(DeltaT, 0, 1)
TE = T1(xE)

# Calcul de l'échelle verticale

Tmin = (round(T1(xE)/5)-3)*5
Tmax = (round(max(Tf1,Tf2)/5)+1)*5

# Calcul des fractions molaires pour chaque courbe

X = np.linspace(0.0, 1.0)
X1 = np.linspace(0.0, xE)
X2 = np.linspace(xE, 1.0)

# Tracé

plt.figure(figsize=(10, 8))

plt.fill_between(X, Tmin*np.ones(X.shape), TE*np.ones(X.shape), color=col3, alpha=0.2)
plt.fill_between(w(X1), TE*np.ones(X1.shape), T1(X1), color=col1, alpha=0.2)
plt.fill_between(w(X2), TE*np.ones(X2.shape), T2(X2), color=col2, alpha=0.2)

plt.text(0.5, (TE+Tmin)/2.0, E1+"+"+E2, fontsize=16, ha="center", va="center", color='r')
plt.text(w(xE)/3.0, (3*TE+Tf1)/4.0, "L+"+E1, fontsize=16, ha="center", va="center", color='g')
plt.text((2+w(xE))/3.0, (3*TE+Tf2)/4.0, "L+"+E2, fontsize=16, ha="center", va="center", color='b')
plt.text(w(xE), (2*max(Tf1, Tf2)+min(Tf1, Tf2))/3.0, "L", fontsize=16, ha="center", va="center")

for x in xsol :
    if x < xE :
        plt.annotate("liquidus", (w(x), T1(x)),(w(x)+0.1, T1(x)+2), arrowprops=dict(facecolor='black', alpha=0.3, shrink=0.1), ha='left', va='bottom', alpha=0.5, fontsize=12)
    else :
        plt.annotate("liquidus", (w(x), T2(x)),(w(x)-0.1, T2(x)+2), arrowprops=dict(facecolor='black', alpha=0.3, shrink=0.1), ha='right', va='bottom', alpha=0.5, fontsize=12)

# Point E

plt.plot([w(xE)], [TE], "ko", markersize=8)
plt.text(w(xE)+0.008, TE-2.5, "E", fontsize=12)

# Points

for col, lst in points :
    plt.errorbar([ e[0] for e in lst ],
                 [ e[1] for e in lst ],
                 [ e[3] for e in lst ],
                 [ e[2] for e in lst ],
                 fmt='s', color=col)

# Fignolage

plt.gca().tick_params(right=True, labelright=True)

plt.grid(alpha=0.3)
plt.xlim(0, 1)
plt.ylim(Tmin, Tmax)

plt.ylabel(r"Température $T$ ($°C$)")
plt.xlabel(r"Fraction massique $w$ en "+E2r if massique else r"Fraction molaire $x$ en "+E2r)

plt.title(titre, pad=30)

#-----------------------------------------------------------------------

plb.rcParams.update(memParams)

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    plt.show()