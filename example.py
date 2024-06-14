from typing import Union
from cpm.parse import parse_csv
from cpm.models import ChangePropagationTree


dsm_i = parse_csv('./test-assets/test-trinity-dsm-impact-5.csv')
dsm_l = parse_csv('./test-assets/test-trinity-dsm-likelihood-5.csv')

# Run change propagation on entire matrix
res_mtx: list[list[Union[float, str]]] = []
for i, icol in enumerate(dsm_l.columns):
    res_mtx.append([icol])

    for j, jcol in enumerate(dsm_l.columns):
        cpt = ChangePropagationTree(j, i, dsm_impact=dsm_i, dsm_likelihood=dsm_l)
        cpt.propagate(search_depth=5)
        res_mtx[i].append(cpt.get_risk())

# Write CSV file
delimiter = "; "
csv = "\t"+delimiter
csv += delimiter.join(dsm_l.columns) + "\n"

for line in res_mtx:
    csv_line = delimiter.join(map(str, line))

    csv_line += "\n"
    csv += csv_line

with open("cpm.csv", "w") as file:
    file.write(csv)

print(csv)
