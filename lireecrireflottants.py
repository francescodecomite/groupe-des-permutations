# lire et écrire des flottants dans un fichier
from random import *
from array import array
"""
L=[random() for i in range(16)]


output_file = open('fileFloat.bin', 'wb')
float_array = array('d', L)
float_array.tofile(output_file)
output_file.close()


# convert to bytes, BIG endian, for use by Java
import struct
f = [3.14, 2.7, 0.0, -1.0, 1.1]
b = struct.pack('>'+'f'*len(f), *f)

with open("f.bin", "wb") as file:
    file.write(b)

retour=open('f.bin', 'rb')
k=retour.read()
u=(struct.unpack('>'+'f'*4,k))
"""

# C'est trop le bordel en binaire. Je vais sauver des chaînes et
# les relire
# Par contre ça, ça marche
L=[random() for i in range(16)]
print(L)
output_file = open('fileFloat.txt', 'w')
for u in L:
    output_file.write(str(u)+"\n")
output_file.close()

input_file=open("fileFloat.txt",'r')
for line in input_file:
    u=float(line)
    print(type(u))
    print(line.strip())  # .strip() to remove newline characters
input_file.close()




