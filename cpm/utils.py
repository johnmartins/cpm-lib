from typing import Union
from cpm.models import ChangePropagationTree, DSM


def calculate_risk_matrix(dsm_impact: DSM, dsm_likelihood: DSM, search_depth=4) \
        -> list[list[Union[float, str]]]:
    """
    Run Change Propagation algorithm on entire DSM, and generate a risk matrix.
    :param dsm_impact:
    :param dsm_likelihood:
    :param search_depth:
    :return:
    """

    cpm: list[list[Union[float, str]]] = []

    for l_index, lcol in enumerate(dsm_likelihood.columns):
        cpm.append([])

        for i_index, icol in enumerate(dsm_impact.columns):
            cpt = ChangePropagationTree(i_index, l_index,
                                        dsm_impact=dsm_impact,
                                        dsm_likelihood=dsm_likelihood)
            cpt.propagate(search_depth=search_depth)
            cpm[l_index].append(cpt.get_risk())

    return cpm
