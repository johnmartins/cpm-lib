import cpm.parse as parse
from cpm.models import *


dsm = parse.parse_csv('./test-assets/test-trinity-dsm-5.csv')

cpt = ChangePropagationTree(0, 2, dsm, dsm)
risk = cpt.propagate(search_depth=5)

print(risk)

"""
Correct example with 0.5 impacts and probs
Le = 0.5
Ie = 0.5

L_abc_or_abec = 1 - ( 1 - Le * Le ) * ( 1 - Le * Le * Le )
print(L_abc_or_abec)

L = 1 - (1 - L_abc_or_abec) * (1 - L_abc_or_abec)
print(L)

L = Le*(1-(1-Le*Le)*(1-Le))
print(L)
print(f'Likelihood = {(1 - (1 - L) * (1 - L))}')

R = Le*(1-(1-Le*Le*Ie)*(1-Le*Ie))
print(R)
print(f'Risk = {(1 - (1 - R) * (1 - R))}')

I = R/L
print(f'Impact = {(1 - (1 - I) * (1 - I))}')

"""

"""
correct example with varying impacts
Le = 0.5
Ibc = 0.4
Iec = 0.7

L = Le*(1-(1-Le*Le)*(1-Le))
print(L)
print(f'Likelihood = {(1 - (1 - L) * (1 - L))}')

Re = Le*(1-(1-Le*Le*Ibc)*(1-Le*Iec))
Rb = Le*(1-(1-Le*Le*Iec)*(1-Le*Ibc))
print(f'Risk = {(1 - (1 - Re) * (1 - Rb))}')
"""



