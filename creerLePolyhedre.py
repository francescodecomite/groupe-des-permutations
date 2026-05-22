from math import *
import re
#from mathutils import *
#import bpy
# Lire les fichiers off d'un polyèdre, et construire le mesh
# Ouvrir et lire le fichier
def lirePolyedre(nom):
    fichier=open(nom,'r')
    return fichier

l=lirePolyedre("tetrakis_hexahedron.off")
lignes=l.readlines()
print(lignes[2])
caracteristiques=list(map(int,re.findall(r'\d+', lignes[2])))
print(caracteristiques)
coords=[list(map(int,re.findall(r'\d+', l))) for l in lignes[1,caracteristiques[0]]]
print(coords)
"""
#Creation d'un icosaedre avec des aretes de longueur 2
def icosaedre():
    me=bpy.data.meshes.new('icosaedre')
    coords=[]
    faces=[]
    phi=(1+sqrt(5))/2
    coords=[[0,0,0] for i in range(12)]
    coords[0]=[-phi,0,1]
    coords[1]=[phi,0,1] 
    coords[2]=[-phi,0,-1]
    coords[3]=[phi,0,-1]
    coords[4]=[0,1,phi]
    coords[5]=[0,1,-phi]
    coords[6]=[0,-1,phi]
    coords[7]=[0,-1,-phi]
    coords[8]=[1,phi,0]
    coords[9]=[-1,phi,0]
    coords[10]=[1,-phi,0]
    coords[11]=[-1,-phi,0]
    faces.append([4,1,8]) 
    faces.append([10,1,6]) 
    faces.append([4,0,6]) 
    faces.append([6,1,4]) 
    faces.append([8,1,3]) 
    faces.append([3,1,10]) 
    faces.append([4,8,9]) 
    faces.append([2,0,9])
    faces.append([9,0,4 ])
    faces.append([11,10,6 ])
    faces.append([11,0,2])
    faces.append([6,0,11])
    faces.append([5,8,3])
    faces.append([9,8,5])
    faces.append([5,2,9]) 
    faces.append([3,10,7,])
    faces.append([7,10,11])
    faces.append([11,2,7])
    faces.append([7,2,5])
    faces.append([5,3,7])
    me.from_pydata(coords,[],faces)  
    return me
    
#la scene courante
scn=bpy.context.scene
#construire un icosaedre
myMesh=icosaedre()  
# en faire un objet et le mettre en scene
ob = bpy.data.objects.new('icoz', myMesh)
bpy.context.collection.objects.link(ob) 
#bpy.context.scene.objects.link(ob)  
#definir les couleurs des faces
myMesh.vertex_colors.new()
vertexColor = myMesh.vertex_colors[0].data
indice=0
rouge=[1,0,0]
bleu=[0,0,1]
vert=[0,1,0]
jaune=[1,1,0]
orange=[1,0.55,0]
valeur=[rouge,bleu,orange,jaune,orange,vert,vert,rouge,bleu,rouge,jaune,vert,
        bleu,jaune,orange,jaune,orange,bleu,vert,rouge] 
j=0
for poly in myMesh.polygons:
    for idx in poly.loop_indices:
        vertexColor[indice].color=valeur[j]
        indice=indice+1
    j=j+1
"""
