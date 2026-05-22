# Engendrer tous les triangles avec la permutation écrite au milieu
# version 2 : on essaie d'économiser le matériau

TAILLE=500
pourcentage=0.05
from math import *
from itertools import permutations

# Entête du fichier SVG.
def debut(c=TAILLE):
    entete="<svg viewBox=\"0 0 "+str(2*c)+" "+str(2*c)+"\" xmlns=\"http://www.w3.org/2000/svg\">\n"
    pied="</svg>\n"
    # Le nom du fichier SVG, 
    image=open("permutationsV2.svg","w")
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
    

def triangle(c=TAILLE,dx=0,dy=0,color="\"red\"", transform="\"\""):
    hauteur=c/2*tan(pi/2-asin(2/3))
    return "<polygon points=\""+str(dx)+" "+str(c+dy)+" ,"+str(c/2+dx)+" "+str(c-hauteur+dy)+" , "+str(c+dx)+" "+str(c+dy)+"\" fill=\"none\" stroke="+color+" transform="+transform+"/>\n"

def triangle_envers(c=TAILLE,dx=0,dy=0,color="\"red\"", transform="\"\""):
    hauteur=c/2*tan(pi/2-asin(2/3))
    return "<polygon points=\""+str(dx)+" "+str(dy)+" ,"+str(c/2+dx)+" "+str(hauteur+dy)+" , "+str(c+dx)+" "+str(dy)+"\" fill=\"none\" stroke="+color+" transform="+transform+"/>\n"



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
    epsilon=5
    epsy=5
    image=debut()
    for u in range(24):
         i=u//4
         j=u%4
         ax=taille*i
         ay=taille*j
         if u%2==0:
          image.write(triangle(c=taille,color="\"green\"",dx=ax+i*epsilon,dy=ay/2))
          image.write("\n")
          image.write(texte(les_permuts[6*j+i],dx=ax+taille*0.25+i*epsilon,dy=ay/2+taille*0.87))
          
         else :
          image.write("\n")
          image.write(triangle_envers(c=taille,color="\"green\"",dx=ax+taille/2+i*epsilon,dy=ay/2-taille/2+epsy))
          image.write("\n")
          image.write(texteInverse(les_permuts[6*j+i],dx=taille+ax-taille*0.00+i*epsilon,dy=ay/2-taille+taille*0.67))
         
         
    fin(image)
    
  


