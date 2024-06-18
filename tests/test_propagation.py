from cpm.models import ChangePropagationTree
from cpm.parse import parse_csv


def test_risk_calculation():
    dsm_p = parse_csv('./tests/test-assets/dsm-cpx-probs.csv')
    dsm_i = parse_csv('./tests/test-assets/dsm-cpx-imps.csv')

    # 4 path length complex DSM
    depth = 4
    res_mtx: list[list[float]] = []

    for i, col in enumerate(dsm_p.columns):
        res_mtx.append([])
        for j, col in enumerate(dsm_p.columns):
            cpt = ChangePropagationTree(start_index=j, target_index=i, dsm_impact=dsm_i, dsm_likelihood=dsm_p)
            cpt.propagate(search_depth=depth)
            r = cpt.get_risk()
            res_mtx[i].append(r)

    dsm_r = parse_csv('./tests/test-assets/dsm-cpx-answers-risks.csv')

    for i, col in enumerate(dsm_r.columns):
        for j, col in enumerate(dsm_r.columns):
            if dsm_r.matrix[i][j] is None:
                continue
            assert abs(res_mtx[i][j] - dsm_r.matrix[i][j]) < 0.001


def test_probability_calculation():
    dsm_p = parse_csv('./tests/test-assets/dsm-cpx-probs.csv')
    dsm_i = parse_csv('./tests/test-assets/dsm-cpx-imps.csv')

    # 4 path length complex DSM
    depth = 4
    res_mtx: list[list[float]] = []

    for i, col in enumerate(dsm_p.columns):
        res_mtx.append([])
        for j, col in enumerate(dsm_p.columns):
            cpt = ChangePropagationTree(start_index=j, target_index=i, dsm_impact=dsm_i, dsm_likelihood=dsm_p)
            cpt.propagate(search_depth=depth)
            r = cpt.get_probability()
            res_mtx[i].append(r)

    dsm_r = parse_csv('./tests/test-assets/dsm-cpx-answers-probs.csv')

    for i, col in enumerate(dsm_r.columns):
        for j, col in enumerate(dsm_r.columns):
            if dsm_r.matrix[i][j] is None:
                continue
            assert abs(res_mtx[i][j] - dsm_r.matrix[i][j]) < 0.001
