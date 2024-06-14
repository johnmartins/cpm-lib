import cpm.parse as parse
from cpm.models import *


dsm = parse.parse_csv('./test-assets/test-trinity-dsm-5.csv')
dsm_impact = parse.parse_csv('./test-assets/test-trinity-dsm-impact-5.csv')

cpt = ChangePropagationTree(2, 0, dsm_impact, dsm)
cpt.propagate(search_depth=50)
p = cpt.get_probability()
r = cpt.get_risk()

print("P = " + str(p))
print("R = " + str(r))
