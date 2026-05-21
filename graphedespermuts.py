# Construire le graphe des permutations de n éléments
# Dessiner le graphe avec dot/graphviz


from math import *
from itertools import permutations


# Je connaissais pas, c'est Chatgpt qui me l'a dit
# Toutes les permutations de n éléments
def toutes_permutations(n):
    l=[ i+1 for i in range(n)]
    print(l)
    k=list(permutations(l))
    print(len(k))
    return ["".join(map(str,u)) for u in k]

# Retourne vrai si les deux permutations ne différent que par un permutation élémentaire
# de deux termes voisins.
def voisins(a,b):
    # on compte combien de positions diffèrent.
    # Si le résultat est différent de 2 : faux
    # sinon, si les deux indices se suivent : ok
    indices=[]
    for i in range(len(a)):
      if a[i]!=b[i]:
          indices.append(i)
    if len(indices)!=2:
        return False
    return abs(indices[0]-indices[1])==1 
        
        
    
    
        

if __name__=="__main__":
    n=6
    les_permuts= toutes_permutations(n)
    #print(les_permuts)
    fichier=open("permuts"+str(n)+".dot","w")
    fichier.write("digraph permuts{\n")

    for i in range(len(les_permuts)):
        base=les_permuts[i]
        for j in les_permuts[i+1:]:
            if voisins(les_permuts[i], j):
                fichier.write(les_permuts[i]+"->"+j+";\n")
    
    fichier.write("}\n")
    fichier.close()              


