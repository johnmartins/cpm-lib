import cpm.parse as parse
from cpm.models import *
import numpy as np

dsm = parse.parse_csv('./test-assets/test-trinity-dsm-3.csv')

cpt = ChangePropagationTree(4, 0, dsm, dsm)
cpt.propagate()
