import bpy
import math
import random
import re
import bmesh
from math import *
# On va lire une courbe quelconque (sous forme d'une liste de points, le centroide etant assimile au centre)
# On la reduit par rapport a son centroide

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
    
    vr[i]=0.68+0.32*valueRed
    vg[i]=0.32+0.68*valueGreen
    vb[i]=0.19+0.81*valueBlue
    gris.append(makeMaterial('gris'+str(i)+'x',(vr[i],vg[i],vb[i],0),(0,0,0),1))   


        
for i in range(NBGRIS+1):        
    print('gris'+str(i)+'x'," ***************** ",bpy.data.materials.find('gris'+str(i)+'x'))        
print("fin") 
nacres=[]
for i in range(20):
    nacres.append(makeMaterial('nacres'+str(i)+'x',(0.7+0.15*random.random(), 0.7+0.15*random.random(),0.7+0.15*random.random(),0),(1,1,1),1)) 
    #nacres.append(makeMaterial('nacres'+str(i)+'x',(0, 0,1),(1,1,1),1)) 

#for i in range(20):
#    print('nacres'+str(i)+'x'," ",bpy.data.materials.find('nacres'+str(i)+'x'))    

def read_data(name):
    global scale
    fichier=open(name,'r')
    coordonnees=[]
    listOfLines=fichier.readlines()
    for i in range(len(listOfLines)):
        catena=listOfLines[i]; 
        chaine=re.findall( r'[+-]?\d+\.*\d*', catena)
        point=(float(chaine[0]),float(chaine[1]),float(chaine[2]))
        #print(i," ",catena,end="")
        #print("\t",point)
        coordonnees.append(point)
    return coordonnees



def coquillage(nbTours,nbToursInternes,nbCerclesParTour,donnees,rayon,rapport,elevation,name):
    """
    On va dire que l'interieur ne fait qu'un tour
    """
    
    obs = bpy.data.objects
    noObj=True
    print("les objets ",obs)
    if(len(obs)>1):
        nbObj=False
    for ob in obs:
     print ("nom de l objet ",ob.name)
    
    
    bpy.ops.object.select_pattern(pattern="messi*")
    bpy.ops.object.delete()
    obs = bpy.data.objects
    print(list(obs))
    print(bpy.data.materials)
    for mat in bpy.data.materials:
        print(mat)
    print("les objets apres ",obs)
    
    
    coef=0.095 #0.12
    
   
    rapInterne=0.8
    zzero=elevation
    me=bpy.data.meshes.new(name)
    nbPointsParCercle=len(donnees)
    
    # Pour creer un bord arrondi entre la face interne et la face externe
    nbSubdiv=30
    
    coord=[(0,0,0) for i in range(nbPointsParCercle*(nbTours*nbCerclesParTour+1)+1+(nbToursInternes*nbCerclesParTour+1)*nbPointsParCercle+1+nbSubdiv*nbPointsParCercle)]
    #Indice du debut du bord arrondi
    Cval=nbPointsParCercle*(nbTours*nbCerclesParTour+1)+1+(nbToursInternes*nbCerclesParTour+1)*nbPointsParCercle+1
    faces=[]
   
    r0=rayon                                                                                 
    z0=zzero
    #radi0=coef*sqrt(r0*r0+z0*z0)*(rapport-1)/(rapport+1)
    positionInitiale=(0,r0,z0)
    print("Position initiale ",positionInitiale)    
    rapportz=rapport*1.15  #0.6
    
    # pour des crenelures internes
    nbCrenelures=30
    amplitude=0.01
    
    for i in range(nbTours*nbCerclesParTour+1):
        #tours=(i+0.0)/nbCerclesParTour
        #calculer les coordonnées des nbPointsparCercle points
        theta=2*i*pi/nbCerclesParTour
        # La position de la spirale en coordonnees cylindriques
        r=rayon*pow(rapport,theta/(2*pi))                                      
        z=zzero*pow(rapportz,theta/(2*pi))
        
        # la spirale en coordonnees cartesiennes
        position=(r*sin(theta),r*cos(theta),z)
       
        # Le rapport de proportionnalite de la courbe (avant, c'etait le rayon
        # du cercle pour avoir des cercles tangents apres un tour complet)
        # on peut jouer sur la tangence avec la valeur de coef
        radi=coef*sqrt(r*r+z*z)*(rapport-1)/(rapport+1)
       
        
        for j in range(nbPointsParCercle):
            #expansion des points de la courbe 
            # C'est comme si la courbe etait à l'origine (le centroide sur (0,0,0))
            nx=radi*donnees[j][0]
            ny=radi*donnees[j][1]
            nz=radi*donnees[j][2]
            
          
                   
            
            # rotation / translation des points trouvés à l'étape précédente
            x=nx*cos(theta)+ny*sin(theta) +position[0]
            y=-nx*sin(theta)+ny*cos(theta) +position[1]
            z=nz +position[2]
            
           
            coord[i*nbPointsParCercle+j]=(x,y,z)      
            #if(i==0):
            #    print(j," ",coord[j])   
             
    # Construire les faces
    for i in range(nbTours*nbCerclesParTour):
        # Créer les faces du cercle i au cercle i+1
        # les points du cercle i vont de i*nbPointsparCercle(=u) à u+nbPointsparCercle-1
        for j in range(nbPointsParCercle):
            coin1=i*nbPointsParCercle+j
            coin2=i*nbPointsParCercle+(j+1)%nbPointsParCercle
            coin3=(i*nbPointsParCercle+nbPointsParCercle)+j
            coin4=i*nbPointsParCercle+nbPointsParCercle+(j+1)%nbPointsParCercle
            faces.append([coin1,coin2,coin3])
            faces.append([coin2,coin4,coin3])
    A=nbPointsParCercle*(nbTours*nbCerclesParTour+1)  
    A0=len(faces) 
    print("A0 ",A0)
    
    # Fermer le bas
    print("Position initiale V 2",positionInitiale)
    coord[A]=positionInitiale
    for j in range(nbPointsParCercle):
        coin1=j
        coin2=(j+1)%nbPointsParCercle
        faces.append([coin1,A,coin2])
    A=A+1
    
    #l'angle de départ pour la partie interne
    thetadepart=(nbTours-nbToursInternes)*2*pi 
    r0=rayon*pow(rapport,thetadepart/(2*pi))                         
    z0=zzero*pow(rapportz,thetadepart/(2*pi))
    # La position de la spirale
    positionSpirale=(r0*sin(thetadepart),r0*cos(thetadepart),z0) 
    
    
    # la proportionnalite (comme pour les faces externes)
    radi0=coef*sqrt(r0*r0+z0*z0)*(rapport-1)/(rapport+1)
   
    
   
    positionInterne=positionSpirale
    for i in range(nbToursInternes*nbCerclesParTour+1):
        #calculer les coordonnées des nbPointsparCercle points
        theta=thetadepart+2*i*pi/nbCerclesParTour
        r=rayon*pow(rapport,theta/(2*pi))                                        
        z=zzero*pow(rapportz,theta/(2*pi))
        radi=coef*sqrt(r*r+z*z)*(rapport-1)/(rapport+1)
        
        # Position de la spirale
        position=(r*sin(theta),r*cos(theta),z)
        
       
        
        for j in range(nbPointsParCercle):
            dx=donnees[j][0]
            dy=donnees[j][1]
            dz=donnees[j][2]
            l=radi*sqrt(dx*dx+dy*dy+dz*dz)
            rapInterne=1-0.3/l                                  #epaisseur
            
            
            
            
            nx=rapInterne*radi*donnees[j][0]
            ny=rapInterne*radi*donnees[j][1]
            nz=rapInterne*radi*donnees[j][2]
            
            """
            # Creation des crenelures internes
            ajout=0
            if(j<nbPointsParCercle/2):
             valAngle=cos(nbCrenelures*pi*(j+0.0)/nbPointsParCercle)
             ajout=amplitude*valAngle
             if(ajout>0):
              ajout=0
            angle=atan2(nz,ny)
                
            ny=ny+ajout*cos(angle)
            nz=nz+ajout*sin(angle)
            """
            
            
            # rotation des points trouvés à l'étape précédente
            x=nx*cos(theta)+ny*sin(theta)+position[0]
            y=-nx*sin(theta)+ny*cos(theta)+position[1]
            z=nz +position[2]
            coord[A+i*nbPointsParCercle+j]=(x,y,z)
    
    # Construire les faces
    for i in range(nbToursInternes*nbCerclesParTour):
        # Créer les faces du cercle i au cercle i+1
        # les points du cercle i vont de i*nbPointsparCercle(=u) à u+nbPointsparCercle-1
        for j in range(nbPointsParCercle):
            coin1=A+i*nbPointsParCercle+j
            coin2=A+i*nbPointsParCercle+(j+1)%nbPointsParCercle
            coin3=A+(i*nbPointsParCercle+nbPointsParCercle)+j
            coin4=A+i*nbPointsParCercle+nbPointsParCercle+(j+1)%nbPointsParCercle
            faces.append([coin1,coin3,coin2])
            faces.append([coin2,coin3,coin4])
            
    # Fermer le bas interne
    B=nbPointsParCercle*(nbTours*nbCerclesParTour+1)+1+(nbToursInternes*nbCerclesParTour+1)*nbPointsParCercle
    
    
    coord[B]=positionInterne
    for j in range(nbPointsParCercle):
        coin1=A+j
        coin2=A+(j+1)%nbPointsParCercle
        faces.append([coin1,coin2,B])
    print("nombre de faces ", len(faces))
    # fermer le bord superieur
    A=A-nbPointsParCercle-1
    B=B-nbPointsParCercle              
    
    # creer un bord arrondi 
    # on est aidés car le dernier bord c'est sur le zero des X
    
    ampli=1
    distance=[0.0 for i in range (nbPointsParCercle)]
    
    for j in range(nbPointsParCercle):
     distance[j]=0.5*sqrt((coord[A+j][0]-coord[B+j][0])**2+ (coord[A+j][1]-coord[B+j][1])**2+(coord[A+j][2]-coord[B+j][2])**2)      
    
    
    for k in range(nbSubdiv-1):
        coefka=(nbSubdiv-k-1.0)/nbSubdiv
        coefkb=(k+1.0)/nbSubdiv
        #coefkas=sin(2*(k+1)*pi/nbSubdiv)
        #coefkbs=sin(2*(nbSubdiv-k-1.0)*pi/nbSubdiv)
        kk=k+1
        if(k>=(nbSubdiv-2)/2):
         #coefx=coefka
         kk=nbSubdiv-1-k
        #else:
        # coefx=coefkb
        print(k," ",kk," ",sin(pi*kk/nbSubdiv))
        for j in range(nbPointsParCercle):
         #u=distance[j]**2-(distance[j]-(kk+1)/nbSubdiv)**2  
         #u=(distance[j]**2)*kk*kk/(nbSubdiv*nbSubdiv)
         #u=distance[j]*sqrt((2-kk/nbSubdiv)*kk/nbSubdiv)
         #u=distance[j]*sqrt((2-kk/nbSubdiv)*kk/nbSubdiv)
         u=distance[j]*sin(pi*kk/nbSubdiv)
         #disty=coefx*distance[j]
        
        
         
         altitude=u*ampli
        
         #coord[Cval+j+k*nbPointsParCercle]=(altitude+(coefka*coord[A+j][0]+coefkb*coord[B+j][0]),coefka*coord[A+j][1]+coefkb*coord[B+j][1],coefka*coord[A+j][2]+coefkb*coord[B+j][2])
         coord[Cval+j+k*nbPointsParCercle]=(altitude,coefka*coord[A+j][1]+coefkb*coord[B+j][1],coefka*coord[A+j][2]+coefkb*coord[B+j][2])
         
    # premiere ligne
    for j in range(nbPointsParCercle): 
     coin1=A+j
     coin2=A+(j+1)%nbPointsParCercle
     coin3=Cval+j
     coin4=Cval+(j+1)%nbPointsParCercle
     faces.append([coin1,coin2,coin3])
     faces.append([coin2,coin4,coin3])    
    #print("nombre de faces ", len(faces))
    
    #derniere ligne
    for j in range(nbPointsParCercle):
     coin1=Cval+j+(nbSubdiv-2)*nbPointsParCercle
     coin2=Cval+(j+1)%nbPointsParCercle+(nbSubdiv-2)*nbPointsParCercle
     coin3=B+j
     coin4=B+(j+1)%nbPointsParCercle
     faces.append([coin1,coin2,coin3])
     faces.append([coin2,coin4,coin3])    
    #print("nombre de faces ", len(faces))
    
    
    #et puis les lignes du milieu
    for k in range(nbSubdiv-2):
        for j in range(nbPointsParCercle): 
            coin1=Cval+j+k*nbPointsParCercle
            coin2=Cval+(j+1)%nbPointsParCercle+k*nbPointsParCercle
            coin3=Cval+j+(k+1)*nbPointsParCercle
            coin4=Cval+(j+1)%nbPointsParCercle+(k+1)*nbPointsParCercle
            faces.append([coin1,coin2,coin3])
            faces.append([coin2,coin4,coin3])    
        #print(k, " nombre de faces ", len(faces))
            
   
    
    # Et hop, c'est la fin, on fabrique le mesh
    me.from_pydata(coord,[],faces)   
    me.update(calc_edges=True) 
    #print(me.validate(verbose=True))
    
    
    
    
    # On met des couleurs 
    # de 0 a 19 : les nacres
    
    if(True):
      print("Booleen ",noObj)   
      for i in range(20):
       
        maty=bpy.data.materials.get("nacres"+str(i)+'x')
        if(maty==None):
         print("nacres "+str(i)," pas trouve")      
         me.materials.append(nacres[i])
        else:
         me.materials.append(maty)    
       
      #de 20 a 20+NBGRIS-1 : les nuances de gris  
      for i in range(NBGRIS+1):
        maty=bpy.data.materials.get("gris"+str(i)+'x')
        if(maty==None):
         me.materials.append(gris[i])  
        else:
         me.materials.append(maty)    
         
                 
    print(me.materials.keys())    
        
    # Les donnees calculees 
    # d'apres la disquette de Meinhardt
    # sp511c.prm
    # Figure 5.11e page 87
    # Babylonia japonica
   
        
    LARGEUR=nbPointsParCercle
    KT=450
    KP=12
    KX=1 
    KY=120
    KD=9
    KI=5
    KE=532
    KR=5
    KN=3
    KG=0
    
    K1=3
    K2=2
    K3=0
    K4=1
    DX=3.0 
    DY=0.0
    DZ=0.3
	# DW=a

    DA=0.01*3 #4.05
    RA=0.02*1.65
    BA=0.05*1.7 #0.05*1.15# 0.8 et au dessus
    SA=0.05
    CA=0.0
    AA=1.0 
    GA=1.0
    
    DB=0.01*0.02
    RB=0.002*0.5
    BBval=0.0
    SB=0.0
    CB=0.0
    AB=1.0
    GB=1.0
    
    DC=0.4*0.9*1.3
    RC=0.01*0.5*3
    BC=0.0
    SC=0.0
    CC=0.0
    AC=1.0   
    GC=1.0	
    

    A=[AA for i in range(LARGEUR)]
    S=[0 for i in range(LARGEUR)]
    B=[AB for i in range(LARGEUR)]
    C=[AC for i in range(LARGEUR)]
    ABB=[0 for i in range(LARGEUR)]
    
    
    for k in range(35,180):
        A[k]=5
        S[k]=5
        B[k]=5
        C[k]=5
        ABB[k]=5
    
    #random.seed(1214)
   
    for i in range(LARGEUR):
        S[i]=RA*(1+KR/100.0*(random.random()-0.5))
        A[i]=GA
        B[i]=GB
        C[i]=GC
        ABB[i]=1
        
    DRA=1-RA-2*DA
    DRB=1-RB-2*DB
    DRC=1-RC-2*DC
    
    delay=31

    #Initialisation premiere ligne
      
    motif=[0 for i in range(LARGEUR)]
    # des coups pour rien pour amorcer
    for jj in range(150):
     Abis=[0 for i in range(LARGEUR)]
     Bbis=[0 for i in range(LARGEUR)]
     Cbis=[0 for i in range(LARGEUR)]
     for i in range(LARGEUR):
      Aconcent=A[i]
      Bconcent=B[i]
      Sconcent=S[i] 
      Cconcent=C[i]
      olddecaydiffA=DRA*Aconcent+DA*(A[(i+LARGEUR-1)%LARGEUR]+A[(i+1)%LARGEUR])
      olddecaydiffB=DRB*Bconcent+DB*(B[(i+LARGEUR-1)%LARGEUR]+B[(i+1)%LARGEUR])
      olddecaydiffC=DRC*Cconcent+DC*(C[(i+LARGEUR-1)%LARGEUR]+C[(i+1)%LARGEUR])       
      
      Abis[i]=olddecaydiffA+(Sconcent/Cconcent)*(Aconcent*Aconcent/((1+SA*Aconcent*Aconcent)*Bconcent)+BA)
      Bbis[i]=olddecaydiffB+RB*Aconcent*Aconcent/Cconcent+BBval
      Cbis[i]=olddecaydiffC+RC*Aconcent        
      
     
     for i in range(LARGEUR):
      A[i]=Abis[i]
      B[i]=Bbis[i]
      C[i]=Cbis[i]    
     
      
    AMIN=A[0]
    AMAX=A[0]
    for i in range(LARGEUR): 
        if(A[i]>AMAX):
            AMAX=A[i]
        if(A[i]<AMIN):
            AMIN=A[i]     
    print(AMIN," ",AMAX)           
    for k in range(LARGEUR):
      motif[k]=int(NBGRIS*(A[k]-AMIN)/(AMAX-AMIN))
  
    bm = bmesh.new()
    bm.from_mesh(me)
    #bm.normal_update()
    #bm.faces.ensure_lookup_table()  
    
    
    
    j= 2*nbPointsParCercle 
    for f in bm.faces[:A0+nbPointsParCercle]:
     k=(j//2)%nbPointsParCercle  
     maty=me.materials.get('gris'+str(motif[k])+'x')
     v=list(me.materials)
     pos=v.index(maty)
     
     f.material_index=pos
     #print(k," ",motif[k]," ",maty," ",pos," ",v[f.material_index])
     #f.material_index=pos
     
     j=j+1  
     
     
         
     
     if(j%(2*nbPointsParCercle)==0):
         
         
       
        # Il est temps de passer au schema suivant
        
        for jj in range(delay):
         
         Abis=[0 for i in range(LARGEUR)]
         Bbis=[0 for i in range(LARGEUR)]
         Cbis=[0 for i in range(LARGEUR)]
         for i in range(LARGEUR):
          Aconcent=A[i]
          Bconcent=B[i]
          Sconcent=S[i] 
          Cconcent=C[i]
          olddecaydiffA=DRA*Aconcent+DA*(A[(i+LARGEUR-1)%LARGEUR]+A[(i+1)%LARGEUR])
          olddecaydiffB=DRB*Bconcent+DB*(B[(i+LARGEUR-1)%LARGEUR]+B[(i+1)%LARGEUR])
          olddecaydiffC=DRC*Cconcent+DC*(C[(i+LARGEUR-1)%LARGEUR]+C[(i+1)%LARGEUR])
          
             
          Abis[i]=olddecaydiffA+(Sconcent/Cconcent)*(Aconcent*Aconcent/((1+SA*Aconcent*Aconcent)*Bconcent)+BA)
          Bbis[i]=olddecaydiffB+RB*Aconcent*Aconcent/Cconcent+BBval
          Cbis[i]=olddecaydiffC+RC*Aconcent 
         
         for i in range(LARGEUR):
          A[i]=Abis[i]
          B[i]=Bbis[i]
          C[i]=Cbis[i]
           
        AMIN=A[0]
        AMAX=A[0]
        for i in range(LARGEUR): 
            if(A[i]>AMAX):
                AMAX=A[i]
            if(A[i]<AMIN):
                AMIN=A[i]      
        for k in range(LARGEUR):
            motif[k]=int(NBGRIS*(A[k]-AMIN)/(AMAX-AMIN))
            
         
        
    #Aspect nacre
    for f in bm.faces[A0+nbPointsParCercle+1:]:     
     u=random.randint(0,19)
     maty=me.materials.get('nacres'+str(u)+'x')
     v=list(me.materials)
     pos=v.index(maty)
     #print(u," xxx ",maty, "  ", pos)
     #f.material_index=motif[k]
     f.material_index=pos
     #print(f.material_index," ",v[f.material_index])
     
     #f.material_index=pos
    
    print(me.materials)
   
    bm.to_mesh(me)
    
   
    return me    
 

donnees=read_data("C:/Users/francesco/hubic/recherche/CatalogueRaisonne/NewShapes/babyloniajaponica/japonicatest.txt")
#def coquillage(nbTours,nbToursInternes,nbCerclesParTour,donnees,rayon,rapport,elevation,name):
myMesh=coquillage(4,2,400,donnees,0.22,1.5,-0.6,"shell")

ob = bpy.data.objects.new("messi", myMesh)
scn = bpy.context.scene
scn.collection.objects.link(ob)
print("fini")





