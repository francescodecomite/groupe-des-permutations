# Lire et écrire des flottants
import struct
from math import *

liste_floats = [pi for i in range(500)]
nb_elements = len(liste_floats)

# --- ÉCRITURE ---
# Le format f'{nb_elements}d' génère par exemple '3d' (pour 3 doubles)
format_liste = f'{nb_elements}d'
octets_liste = struct.pack(format_liste, *liste_floats) # '*' déballe la liste

with open("multi_data.bin", "wb") as fichier:
    fichier.write(octets_liste)

# --- LECTURE ---
# Un double fait 8 octets. Pour 3 doubles, on doit lire 3 * 8 = 24 octets
taille_a_lire = nb_elements * 8

with open("multi_data.bin", "rb") as fichier:
    donnees_lu = fichier.read(taille_a_lire)

# Conversion des octets en liste (convertie en type list car unpack renvoie un tuple)
liste_recuperee = list(struct.unpack(format_liste, donnees_lu))

print(liste_recuperee)  # Affiche : [1.5, 2.75, 3.14159]
