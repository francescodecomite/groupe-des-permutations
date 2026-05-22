# Engendrer tous les triangles avec la permutation au milieu
TAILLE=500
pourcentage=0.05
from math import *
from itertools import permutations

# Entête du fichier SVG.
def debut(c=TAILLE):
    entete="<svg viewBox=\"0 0 "+str(2*c)+" "+str(2*c)+"\" xmlns=\"http://www.w3.org/2000/svg\">\n"
    pied="</svg>\n"
    # Le nom du fichier SVG, 
    image=open("permutations.svg","w")
    image.write(entete)
    return image

# Fin du fichier SVG
def fin(image):
    pied="</svg>\n"
    image.write(pied)
    image.close()



# ça peut toujours servir
def ligne(debut,fin,transform="\"\""):
     s="<line x1=\""+str(debut[0])+"\" y1=\""+str(debut[1])+"\" x2=\""+str(fin[0])+"\" y2=\""+str(fin[1])+"\" stroke=\"red\"   transform="+transform+" />\n"
     return s
    

def equilateral(c=TAILLE,dx=0,dy=0,color="\"red\"", transform="\"\""):
    hauteur=c*sqrt(3)/2
    return "<polygon points=\""+str(dx)+" "+str(c+dy)+" ,"+str(c/2+dx)+" "+str(c-hauteur+dy)+" , "+str(c+dx)+" "+str(c+dy)+"\" fill=\"none\" stroke="+color+" transform="+transform+"/>\n"

def triangle(c=TAILLE,dx=0,dy=0,color="\"red\"", transform="\"\""):
    hauteur=c/2*tan(pi/2-asin(2/3))
    return "<polygon points=\""+str(dx)+" "+str(c+dy)+" ,"+str(c/2+dx)+" "+str(c-hauteur+dy)+" , "+str(c+dx)+" "+str(c+dy)+"\" fill=\"none\" stroke="+color+" transform="+transform+"/>\n"


def texte(chaine,dx,dy):
    
    return("<text x=\""+str(dx)+"\" y=\""+str(dy)+"\" font-size=\"2em\">"+chaine+"</text>")
    

# Je connaissais pas, c'est Chatgpt qui me l'a dit
def toutes_permutations(l):
    k=list(permutations(l))
   
    return ["".join(map(str,u)) for u in k]


if __name__=="__main__":
    les_permuts= toutes_permutations([1,2,3,4])
    taille=120
    epsilon=2
    image=debut()
    for i in range(6):
        for j in range(4):
         ax=taille*i
         ay=taille*j
         image.write(triangle(c=taille,color="\"green\"",dx=ax+i*epsilon,dy=ay))
         #image.write(equilateral(c=taille,color="\"green\"",dx=ax,dy=ay))
         image.write("\n")
         image.write(texte(les_permuts[6*j+i],dx=ax+taille*0.25+i*epsilon,dy=ay+taille*0.88))
         
         
    fin(image)
    
  


