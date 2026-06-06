# On va lire tous les triangles du fiochier OFF,
# et pour chaque triangle, on va construire la transformation
# On va sauver les 16 valeurs dans un fichier.

import numpy as np
import sys
import re
from math import *


def lirePolyedre(poly="tetrakis_hexahedron"):
    # Lire les données du polyhèdre (ici Tetrakis hexaèdre)
    # et en extraire les triangles pour plus tard connaître la transformation
    # qui les engendre
    l=open("C:/Users/Francesco/Documents/GitHub/"+poly+".off",'r')
    
    lignes=l.readlines()
    print(lignes[2])
    caracteristiques=list(map(int,re.findall(r'\d+', lignes[2])))
    print(caracteristiques)
    coords=[]
    for i in range(3,caracteristiques[0]+3): 
     couper=list(map(float,re.findall(r'[-]*\d*\.\d+', lignes[i])))
     coords.append(couper)
    print(coords)
    print("\n")

    # coords est une liste qui contient tous les sommets du polyèdre.
    # l'ordre est utilisé par la liste des faces pour associer trois sommets à chaque face
    
    faces=[]
    for i in range(caracteristiques[0]+3,caracteristiques[0]+3+caracteristiques[1]):
        faces.append(list(map(int,re.findall(r'\d+', lignes[i])))[1:])
    print(faces)
    #faces contient toutes les faces
    
    return coords,faces

def distance(p1,p2):
    sum=0
    for i in range(3):
        sum+=(p1[i]-p2[i])*(p1[i]-p2[i])
    return sqrt(sum)

if __name__=="__main__":
    u,v=lirePolyedre()
    print(u)
    print("\n")
    
    for triangle in v: 
        print("1 \t\t",triangle)
        p1=u[triangle[0]]
        p2=u[triangle[1]]
        p3=u[triangle[2]]

        d0=distance(p1,p2)
        d1=distance(p1,p3)
        d2=distance(p3,p2)

        print(d0)
        print(d1)
        print(d2)
        # Une seule distance vaut sqrt(2), c'est la distance entre les deux points
        # de la base du triangle isocele
        # On va inverser l'ordre des points pour toujours parler du même
        # triangle
        # Mais ça marche pas, le triangle pourrait être à l'envers.
        # Putain le bordel. Sens de rotation du parcours des points.
        # Si il n'y a pas de distinction entre les faces , c'est pas grave
        # Quid des triangles non isocèles, et des polygones
        # non triangulaires ?
        # Pour le moment, on ne s'occupe que des isoceles du tetrakis hexaèdre

        

        if d1>d0:
            temp=triangle[2]
            triangle[2]=triangle[1]
            triangle[1]=triangle[0]
            triangle[0]=temp
            print("2 \t\t ",triangle)
        elif d2>d0 :
            temp=triangle[0]
            triangle[0]=triangle[1]
            triangle[1]=triangle[2]
            triangle[2]=temp
            print("3 \t\t ",triangle)
       

    



















sys.exit(0)

A=np.array((-0.7,0.7,-0.7))
B=np.array((0.7,-0.7,0.7))
C=np.array((0.0,1.06,0.0))

Aprime = np.array([0.383967774468709, -0.457122008769346, 1.489277869851005])
Bprime = np.array([2.616032225531291, -1.142877991230654, 2.910722130148995])
Cprime = np.array([0.944699164644112, -0.003743029127177, 2.625592486757558])


def frame(A, B, C):
    e1 = B - A
    e1 = e1 / np.linalg.norm(e1)

    v = C - A
    v = v - np.dot(v, e1) * e1
    e2 = v / np.linalg.norm(v)

    e3 = np.cross(e1, e2)

    return np.column_stack((e1, e2, e3))

Q  = frame(A,  B,  C)
Qp = frame(Aprime, Bprime, Cprime)

R = np.matmul(Qp,Q.T)
t = Aprime - np.matmul(R,A)
print(t)



print(Q)
print(np.linalg.det(R))
print(np.linalg.norm(R.T @ R - np.eye(3)))

