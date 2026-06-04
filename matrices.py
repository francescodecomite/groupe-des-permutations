
from numpy import *
# Un échauffement avec une matrice de rotation
rotation=matrix([[0.8125,-0.5239,0.2558],[0.5826,0.7513,-0.31],
                       [-0.0194,0.401,0.9154]])
transpo=matrix.transpose(rotation)
resu=matmul(rotation,transpo)
print(resu)
# Ok, c'est la matrice identité
# Maintenant on prend les deux triangles, on recherche la translation et la rotation

A=array((-0.7,0.7,-0.7))
B=array((0.7,-0.7,0.7))
C=array((0.0,1.06,0.0))

"""
Aprime=array((0.393,-0.45,1.49))
Bprime=array((2.607,-1.15,2.91))
Cprime=array((0.945,-0.004,2.625))
"""

Aprime = array([0.383967774468709, -0.457122008769346, 1.489277869851005])
Bprime = array([2.616032225531291, -1.142877991230654, 2.910722130148995])
Cprime = array([0.944699164644112, -0.003743029127177, 2.625592486757558])


#Calcul de la matrice de rotation
#Calcul de Q
u=B-A
normeDeU=linalg.norm(u)
e1=u/normeDeU


#ok
# Deuxième vecteur
v=C-A
alpha=dot(v,e1)

#Ok
vperp=v-alpha*e1


normedevperp=linalg.norm(vperp)

e2=vperp/normedevperp

#ok
e3=cross(e1,e2)
# ok
print("\n")
Q=column_stack([e1,e2,e3])


# La matrice est orthogonale, c'est bon

# On fait pareil sur le triangle final
uprime=Bprime-Aprime
normeDeUprime=linalg.norm(uprime)
e1prime=uprime/normeDeUprime
#ok

vprime=Cprime-Aprime
print(vprime)

alpha=dot(vprime,e1prime)
print(" **")
print(alpha)
print(" **")

vperp=vprime-alpha*e1prime
print(vperp)
normedevperp=linalg.norm(vperp)
print(normedevperp)
e2prime=vperp/normedevperp

e3prime=cross(e1prime,e2prime)
print(e3prime)
print(" ")
Qprime=column_stack([e1prime,e2prime,e3prime])
print(Qprime)


resu=matmul(Qprime,Q.T)
r2=Qprime@Q.T

print(resu)
print(r2)

#La translation
t=Aprime-resu@A
print(t)

