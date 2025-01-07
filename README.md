[![DOI](https://zenodo.org/badge/808499164.svg)](https://zenodo.org/doi/10.5281/zenodo.13340868)

# Change Prediction Library
This library is intended to assist in the calculation of 
change prediction/propagation (Clarkson et al., 2004) in a system.
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
dsm_likelihood = parse.parse_csv('./dsm-likelihoods.csv')
dsm_impact = parse.parse_csv('./dsm-impacts.csv')

# Calculate the risk of change propagating 
# from sub-system 3, to sub-system 0
start_index = 3
target_index = 0
cpt = ChangePropagationTree(start_index, target_index, dsm_impact, dsm_likelihood)
cpt.propagate(search_depth=4)
risk = cpt.get_risk()
probability = cpt.get_probability()

```

In this example, assuming a 4x4 DSM with the columns: A, B, C, and D, with
the respective indices 0, 1, 2, and 3,
the code above will calculate the risk of propagation from sub-system 
D to sub-system A.

The search depth determines the maximum length of change propagation. It is recommended by
Clarkson et al., 2004 to keep this at 4 or lower. 
Higher values will be computationally expensive and produce uninteresting results.

Granted the functions above, it is also possible to create CPM DSMs by running the
CPM algorithm on all the elements of a matrix that contains likelihoods 
and a second matrix that contains impacts. Here is an example:

```python
from typing import Union
from cpm.parse import parse_csv
from cpm.models import ChangePropagationTree

# Run change propagation on entire matrix

# Create DSMs for Impacts and Likelihoods
dsm_i = parse_csv('dsm-impacts.csv')
dsm_l = parse_csv('dsm-likelihoods.csv')

# Create a matrix in which the results can be stored
res_mtx: list[list[Union[float, str]]] = []
for i, icol in enumerate(dsm_l.columns):
    res_mtx.append([icol])

    for j, jcol in enumerate(dsm_l.columns):
        # Run change propagation on each possible pairing
        cpt = ChangePropagationTree(j, i, dsm_impact=dsm_i, dsm_likelihood=dsm_l)
        cpt.propagate(search_depth=4)
        # Store results in matrix
        res_mtx[i].append(cpt.get_risk())

# Create CSV string
delimiter = "; "
csv = "\t"+delimiter
csv += delimiter.join(dsm_l.columns) + "\n"
for line in res_mtx:
    csv_line = delimiter.join(map(str, line))

    csv_line += "\n"
    csv += csv_line

# Write to file
with open("cpm.csv", "w") as file:
    file.write(csv)

print(csv)
```

## Expected CSV format
The CSV files are expected to have a header on the first row and the first column. 
Here is an example with 4 sub-systems. The direction of propagation is 
the same as in Clarkson et al., 2004: Columns are instigators of change, 
and rows are the receivers. So, in the example below, the potential interaction 
between C and B is bi-directional, while change can also propagate from D to C.

|       | **A** | **B** | **C** | **D** |
|-------|-------|-------|-------|-------|
| **A** | A     |       |       |       |
| **B** |       | B     | 0.5   |       |
| **C** |       | 0.5   | C     | 0.5   |
| **D** |       |       |       | D     |

## Changing DSM directionality
If it is desirable to instead have instigation occur from rows to columns,
then it is possible to instantiate the DSMs with this as a keyword attribute:
```
dsm = DSM(matrix=data, columns=column_names, instigator="row")
```
The default is `instigator='column`.
This can also be utilized when parsing a CSV-file, like this:

```
dsm = parse_csv(filepath, instigator='row')
```

Note that changing instigator will completely change the results of propagation.

## References
Clarkson, P. J., Caroline, S., & Claudia, E. (2004). Predicting Change Propagation in Complex Design. Journal of Mechanical Design, 126(5), 788–797. https://doi.org/10.1115/1.1765117

