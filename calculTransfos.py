# en entrée, une descritpion d'un polyèdre composé de triangles
# uniquement (pas vérifié)
# Calcule les transformations menant d'un triangle de référence au
# triangle courant. Stocke les 16 valeurs dans un fichier,
# qui sera récupéré dans Grasshopper

# La première chose à faire sera de fabriquer le triangle de
# référence à partir du premier triangle lu.
from math import *

def distance(X,Y):
    dx=(X[0]-Y[0])*(X[0]-Y[0])
    dy=(X[1]-Y[1])*(X[1]-Y[1])
    dz=(X[2]-Y[2])*(X[2]-Y[2])
    return sqrt(dx+dy+dz)
    


x="./tetrakis_hexahedron.off"
fichier=open(x,'r')
les_lignes=fichier.readlines()
caracteristiques=les_lignes[2]
a=les_lignes[3:]
print(caracteristiques)
numbers = [int(x) for x in caracteristiques.split()]
sommets=numbers[0]
faces=numbers[1]
aretes=numbers[2]

liste_pro=a[0:sommets]
liste_sommets=[]
for u in liste_pro: 
 liste_sommets.append(list(map(float,u.split())))
 
print(liste_sommets)


liste_pro= a[sommets:sommets+faces]
liste_faces=[]
for u in liste_pro: 
 liste_faces.append(list(map(int,u.split())))

 
liste_pro=a[sommets+faces:]
liste_aretes=[]
for u in liste_pro: 
 liste_aretes.append(list(map(int,u.split())))


# On a tout chargé. On prend le premier triangle et on le place dans le
# plan vertical, avec son 'centre' en 0,0,0
u=liste_faces[0]
print(u)
sommets=[]
for f in u[1:]:
    sommets.append(liste_sommets[f])
# sommet contient le premier triangle
# on calcule les trois distances
A=sommets[0]
B=sommets[1]
C=sommets[2]

dAB=distance(A,B)
dAC=distance(A,C)
dBC=distance(B,C)

print(dAB)
print(dAC)
print(dBC)

# Calcul du centroide : on connait les cotés (sqrt(2) et 3/4sqrt(2))
# le centre est au tiers de la hauteur à partir du grand coté.
# on doit pouvoir s'en tirer
    
  
