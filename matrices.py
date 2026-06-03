
from numpy import *

rotation=matrix([[0.8125,-0.5239,0.2558],[0.5826,0.7513,-0.31],
                       [-0.0194,0.401,0.9154]])
transpo=matrix.transpose(rotation)
resu=matmul(rotation,transpo)
print(resu)
