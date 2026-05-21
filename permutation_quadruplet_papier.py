# Engendrer tous les triangles avec la permutation écrite au milieu
# version 3 : en papier avec des languettes et des pointillés
# Pour l'économie de matériau, on bougera les trucs dans Inkscape

TAILLE=640
pourcentage=0.05
from math import *
from itertools import permutations

# Entête du fichier SVG.
def debut(c=TAILLE):
    entete="<svg viewBox=\"0 0 "+str(2*c)+" "+str(2*c)+"\" xmlns=\"http://www.w3.org/2000/svg\">\n"
    pied="</svg>\n"
    # Le nom du fichier SVG, 
    image=open("permutation_Papier.svg","w")
    image.write(entete)
    return image

# Fin du fichier SVG
def fin(image):
    pied="</svg>\n"
    image.write(pied)
    image.close()



# ça peut toujours servir
def ligne(debut,fin,color="\"red\"",transform="\"\""):
     s="<line x1=\""+str(debut[0]+decalx)+"\" y1=\""+str(debut[1]+decaly)+"\" x2=\""+str(fin[0]+decalx)+"\" y2=\""+str(fin[1]+decaly)+"\" stroke="+color+"   transform="+transform+" />\n"
     return s
    

def equilateral(c=TAILLE,dx=0,dy=0,color="\"red\"", transform="\"\""):
    hauteur=c*sqrt(3)/2
    return "<polygon points=\""+str(dx)+" "+str(c+dy)+" ,"+str(c/2+dx)+" "+str(c-hauteur+dy)+" , "+str(c+dx)+" "+str(c+dy)+"\" fill=\"none\" stroke="+color+" transform="+transform+"/>\n"

def equilateral_envers(c=TAILLE,dx=0,dy=0,color="\"red\"", transform="\"\""):
    hauteur=c*sqrt(3)/2
    return "<polygon points=\""+str(dx)+" "+str(dy)+" ,"+str(c/2+dx)+" "+str(hauteur+dy)+" , "+str(c+dx)+" "+str(dy)+"\" fill=\"none\" stroke="+color+" transform="+transform+"/>\n"

# Une ligne pointillée (pour que la découpeuse laser fasse des vrais pointillés)
# on devrait décaler la ligne pour que ça soit pareil aux deux extremités...
def ligne_pointillee(depart,arrivee,couleur="blue"):
    x0=depart[0]
    y0=depart[1]
    x1=arrivee[0]
    y1=arrivee[1]
    decalx=0
    decaly=0
    if x0>x1:
        tmp=x0
        x0=x1
        x1=tmp
        tmp=y0
        y0=y1
        y1=tmp
    distance=sqrt((x0-x1)*(x0-x1)+(y0-y1)*(y0-y1))
    if y1==y0:
        pente=0
    else:
        pente=atan2((y1-y0),(x1-x0))
    mycos=cos(pente)
    mysin=sin(pente)
    # Partie découpée du pointillé
    la=7
    # Partie non découpée du pointillée
    lb=9
    nb=int(distance/(la+lb))
    s=""
    for i in range(nb):
        s+="<line x1=\""+str(int(x0+mycos*(i*(la+lb))+decalx))+"\" y1=\""+str(int(y0+mysin*(i*(la+lb))+decaly))+"\" x2=\""+str(int(x0+mycos*(i*(la+lb)+la)+decalx))+"\" y2=\"" +str(int(y0+mysin*(i*(la+lb)+la)+decaly))+"\" fill=\"none\" stroke=\""+couleur+"\"/>\n"
    return s

def trianglePointille(c=TAILLE,couleur="blue"):
    hauteur=c*sqrt(3)/2
    s=ligne_pointillee((0,c),(c/2,c-hauteur),couleur)
    s+=ligne_pointillee((c/2,c-hauteur),(c,c),couleur)
    s+=ligne_pointillee((c,c),(0,c),couleur)
    return s

def texte(chaine,dx,dy):
    
    return("<text x=\""+str(dx)+"\" y=\""+str(dy)+"\" font-size=\"2em\">"+chaine+"</text>")

def texteInverse(chaine,dx,dy):
    
    return("<text x=\""+str(dx)+"\" y=\""+str(dy)+"\" font-size=\"2em\" text-anchor=\"middle\" transform=\"rotate(180 "+str(dx)+" "+str(dy)+")\">"+chaine+"</text>")
    

# Je connaissais pas, c'est Chatgpt qui me l'a dit
def toutes_permutations(l):
    k=list(permutations(l))
   
    return ["".join(map(str,u)) for u in k]


if __name__=="__main__":
    les_permuts= toutes_permutations([1,2,3,4])
    taille=120
    image=debut()
    decalx=0
    decaly=0
    """
    epsilon=5
    epsy=5
    
    for u in range(24):
         i=u//4
         j=u%4
         ax=taille*i
         ay=taille*j
         if u%2==0:
          image.write(equilateral(c=taille,color="\"green\"",dx=ax+i*epsilon,dy=ay/2))
          image.write("\n")
          image.write(texte(les_permuts[6*j+i],dx=ax+taille*0.23+i*epsilon,dy=ay/2+taille*0.75))
          
         else :
          image.write("\n")
          image.write(equilateral_envers(c=taille,color="\"green\"",dx=ax+taille/2+i*epsilon,dy=ay/2-taille/2+epsy))
          image.write("\n")
          image.write(texteInverse(les_permuts[6*j+i],dx=taille+ax-taille*0.00+i*epsilon,dy=ay/2-taille+taille*0.79))
         
    """
    # le triangle en pointillé
    image.write(trianglePointille(taille,"blue"))
    # les languettes
    # largeur de la languette
    a=15
    c=taille
    hauteur=c*sqrt(3)/2
    u=a*sqrt(2)*cos(5*pi/12)
    v=a*sqrt(2)*sin(5*pi/12)
    print(v)
    # Languette à gauche
    image.write(ligne((0,c),(-u,c-v),"\"green\""))
    image.write(ligne((c/2,c-hauteur),(c/2-v,c-hauteur+u),"\"green\""))
    image.write(ligne((c/2-v,c-hauteur+u),(-u,c-v),"\"green\""))
    # Languette à droite
    image.write(ligne((c,c),(c+u,c-v),"\"green\""))
    image.write(ligne((c/2+v,c-hauteur+u),(c/2,c-hauteur),"\"green\""))
    image.write(ligne((c+u,c-v),(c/2+v,c-hauteur+u),"\"green\""))
    # Languette du bas
    image.write(ligne((0,c),(u,c+v),"\"green\""))
    image.write(ligne((c-u,c+v),(u,c+v),"\"green\""))
    image.write(ligne((c-u,c+v),(c,c),"\"green\""))
    fin(image)
    
  


