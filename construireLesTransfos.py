# On va lire tous les triangles du fiochier OFF,
# et pour chaque triangle, on va construire la transformation
# On va sauver les 16 valeurs dans un fichier.

import numpy as np

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

R = np.mul(Qp,Q.T)
t = Aprime - np.mul(R,A)
print(t)



print(Q)
print(np.linalg.det(R))
print(np.linalg.norm(R.T @ R - np.eye(3)))

