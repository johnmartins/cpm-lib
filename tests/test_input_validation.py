import pytest
from cpm.models import ChangePropagationTree, DSM
from cpm.parse import parse_csv
from cpm.utils import calculate_risk_matrix


def test_throws_if_dsm_instigator_mismatch_1():
    dsm_p = parse_csv('./tests/test-assets/dsm-cpx-probs.csv', instigator="row")
    dsm_i = parse_csv('./tests/test-assets/dsm-cpx-imps.csv')

    with pytest.raises(ValueError):
        calculate_risk_matrix(dsm_i, dsm_p, search_depth=4)


def test_throws_if_dsm_instigator_mismatch_2():
    dsm_p = parse_csv('./tests/test-assets/dsm-cpx-probs.csv', instigator="row")
    dsm_i = parse_csv('./tests/test-assets/dsm-cpx-imps.csv')

    with pytest.raises(ValueError):
        ChangePropagationTree(0, 4, dsm_i, dsm_p)


def test_throws_if_dsm_incomplete():
    mtx = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
        [0.7, 0.8, 0.9],
    ]
    cols = ["a", "b", "c", "d"]
    with pytest.raises(ValueError):
        dsm = DSM(mtx, cols)


def test_throws_if_dsm_size_mismatch():
    cols_p = ["a", "b", "c"]
    mtx_p = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
        [0.7, 0.8, 0.9],
    ]
    cols_i = ["a", "b", "c", "d"]
    mtx_i = [
        [0.1, 0.2, 0.3, 0.4],
        [0.4, 0.5, 0.6, 0.7],
        [0.7, 0.8, 0.9, 0.10],
        [0.11, 0.12, 0.13, 0.14]
    ]

    dsm_p = DSM(mtx_p, cols_p)
    dsm_i = DSM(mtx_i, cols_i)

    with pytest.raises(ValueError):
        # If DSMs are of different size, then input validation should prevent execution.
        ChangePropagationTree(0, 2, dsm_i, dsm_p)
