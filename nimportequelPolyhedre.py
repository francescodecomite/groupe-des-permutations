from math import *
import re
from mathutils import *
import bpy
import bmesh
from random import *
# Lire les fichiers off d'un polyèdre, et construire le mesh
# Ouvrir et lire le fichier
def lirePolyedre(nom):
    fichier=open(nom,'r')
    return fichier


def makeMaterial(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    #mat.diffuse_shader = 'LAMBERT' 
    #mat.diffuse_intensity = 0.5
    mat.specular_color = specular
    #mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0
    #mat.mirror_color=(1,1,1)
    #mat.alpha = alpha
    #mat.ambient = 0.1
    #mat.use_cubic=True
    return mat


for material in bpy.data.materials:
    material.user_clear()
    bpy.data.materials.remove(material)

NBGRIS=50
gris=[]
vr=[0 for i in range(NBGRIS+1)]
vg=[0 for i in range(NBGRIS+1)]
vb=[0 for i in range(NBGRIS+1)]
print("debut")

for i in range(NBGRIS+1):
    """
    valueRed=1/(1+exp(-2*(2*(1-(i+0.0)/NBGRIS)-1)))
    valueGreen=1/(1+exp(-15*(2*(1-(i+0.0)/NBGRIS)-1)))
    valueBlue=1/(1+exp(-15*(2*(1-(i+0.0)/NBGRIS)-1)))
    
    """
    valueRed=1-(i+0.0)/NBGRIS
    valueGreen=1-(i+0.0)/NBGRIS
    valueBlue=1-(i+0.0)/NBGRIS
    
    vr[i]=random()
    vg[i]=random()
    vb[i]=random()
    gris.append(makeMaterial('gris'+str(i)+'x',(vr[i],vg[i],vb[i],0),(0,0,0),1)) 
    
   
def tetrakis():
    # Lire les données du polyhèdre (ici Tetrakis hexaèdre)
    # et en faire un mesh pour Blender
    l=lirePolyedre("C:/Users/Francesco/Documents/GitHub/pentagonal_hexecontahedron.off")
    me=bpy.data.meshes.new('tetrakis_hexeaedre')
    lignes=l.readlines()
    print(lignes[2])
    caracteristiques=list(map(int,re.findall(r'\d+', lignes[2])))
    print(caracteristiques)
    coords=[]
    for i in range(3,caracteristiques[0]+3): 
     couper=list(map(float,re.findall(r'[-]*\d*\.\d+', lignes[i])))
     print(couper)
     coords.append(couper)
    print(coords)
    print("\n")
    faces=[]
    for i in range(caracteristiques[0]+3,caracteristiques[0]+3+caracteristiques[1]):
        faces.append(list(map(int,re.findall(r'\d+', lignes[i])))[1:])
    print(faces)
    me.from_pydata(coords,[],faces)  
    
    
    for i in range(NBGRIS+1):
        maty=bpy.data.materials.get("gris"+str(i)+'x')
        if(maty==None):
         me.materials.append(gris[i])  
        else:
         me.materials.append(maty)   
         
    bm = bmesh.new()
    bm.from_mesh(me)
    #bm.normal_update()
    #bm.faces.ensure_lookup_table() 
    
    for f in bm.faces:
     num=randint(0,20)    
     maty=me.materials.get('gris'+str(num)+'x')
     v=list(me.materials)
     pos=v.index(maty)
     
     f.material_index=pos
    

    bm.to_mesh(me)
    return me
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
"""    
#la scene courante
scn=bpy.context.scene
#construire un icosaedre
myMesh=tetrakis()  
# en faire un objet et le mettre en scene
ob = bpy.data.objects.new('tetrakis', myMesh)
bpy.context.collection.objects.link(ob) 
#bpy.context.scene.objects.link(ob)  
#definir les couleurs des faces

