# Change Propagation Library
This library is intended to assist in the calculation of 
change propagation (Clarkson et al., 2004) in a system.
The library takes to DSMs as an input: one for likelihoods and 
one for impacts. These DSMs should be in a CSV format.
Once the DSMs are loaded, a `ChangePropagationTree` can be
constructed for each possible interaction. The 
`ChangePropagationTree` can then be polled for the 
risk and probability of changes.

## Install

```commandline
pip install cpm-lib
```

## Use
First, create the DSMs using CSV-files as inputs. This is done 
using `cpm.parse.parse_csv()`, which returns a `DSM` created from 
the input CSV. Then, use the DSMs to form a `ChangePropagationTree`. This 
tree will calculate the risk of change propagating 
from one part of the system, to another.
```python
import cpm.parse as parse
from cpm.models import ChangePropagationTree
dsm_likelihood = parse.parse_csv('./dsm-likelihood.csv')
dsm_impact = parse.parse_csv('./dsm-impact.csv')

# Calculate the risk of change propagating 
# from sub-system 0, to sub-system 3
start_index = 3
target_index = 0
cpt = ChangePropagationTree(start_index, target_index, dsm_impact, dsm_likelihood)
risk = cpt.get_risk()
probability = cpt.get_probability()

```

In this example, assuming a 4x4 DSM with the columns: A, B, C, and D, with
the respective indices 0, 1, 2, and 3,
the code above will calculate the risk of propagation from sub-system 
D to sub-system A.

## References
Clarkson, P. J., Caroline, S., & Claudia, E. (2004). Predicting Change Propagation in Complex Design. Journal of Mechanical Design, 126(5), 788–797. https://doi.org/10.1115/1.1765117

