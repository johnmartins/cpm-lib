from cpm.models import ChangePropagationTree
from cpm.parse import parse_csv
from cpm.utils import calculate_risk_matrix


def test_risk_calculation_1():
    dsm_p = parse_csv('./tests/test-assets/dsm-cpx-probs.csv')
    dsm_i = parse_csv('./tests/test-assets/dsm-cpx-imps.csv')

    # 4 path length complex DSM
    depth = 4
    res_mtx: list[list[float]] = []

    for i, _ in enumerate(dsm_p.columns):
        res_mtx.append([])
        for j, _ in enumerate(dsm_p.columns):
            cpt = ChangePropagationTree(start_index=j, target_index=i, dsm_impact=dsm_i, dsm_likelihood=dsm_p)
            cpt.propagate(search_depth=depth)
            r = cpt.get_risk()
            res_mtx[i].append(r)

    dsm_r = parse_csv('./tests/test-assets/dsm-cpx-answers-risks.csv')

    for i, _ in enumerate(dsm_r.columns):
        for j, _ in enumerate(dsm_r.columns):
            if dsm_r.matrix[i][j] is None:
                continue
            assert abs(res_mtx[i][j] - dsm_r.matrix[i][j]) < 0.001


def test_matrix_risk_calculation_1():
    dsm_p = parse_csv('./tests/test-assets/dsm-cpx-probs.csv')
    dsm_i = parse_csv('./tests/test-assets/dsm-cpx-imps.csv')
    dsm_answers = parse_csv('./tests/test-assets/dsm-cpx-answers-risks.csv')

    depth = 4

    dsm_risk = calculate_risk_matrix(dsm_i, dsm_p, search_depth=depth)

    assert dsm_risk is not None
    assert len(dsm_risk) > 0

    for i, _ in enumerate(dsm_risk):
        for j, _ in enumerate(dsm_risk):
            if i == j:
                continue

            if dsm_answers.matrix[i][j] in [None, 0] and dsm_risk[i][j] in [None, 0]:
                continue
            assert abs(dsm_answers.matrix[i][j] - dsm_risk[i][j]) < 0.001


def test_matrix_risk_calculation_2():
    dsm_p = parse_csv('./tests/test-assets/dsm-bm-8-probs.csv')
    dsm_i = parse_csv('./tests/test-assets/dsm-bm-8-imps.csv')
    dsm_r = parse_csv('./tests/test-assets/dsm-bm-8-risks.csv')

    depth = 4

    res_mtx = calculate_risk_matrix(dsm_i, dsm_p, search_depth=depth)

    for i, _ in enumerate(dsm_p.columns):
        for j, _ in enumerate(dsm_r.columns):
            a = res_mtx[i][j]
            b = dsm_r.matrix[i][j]

            # Ignore diagonal
            if i == j:
                continue

            assert (abs(a - b) < 0.001)


def test_transpose():
    dsm_p = parse_csv('./tests/test-assets/dsm-bm-8-probs.csv')
    dsm_i = parse_csv('./tests/test-assets/dsm-bm-8-imps.csv')
    dsm_p_t = parse_csv('./tests/test-assets/dsm-bm-8-probs-transpose.csv', instigator='row')
    dsm_i_t = parse_csv('./tests/test-assets/dsm-bm-8-imps-transpose.csv', instigator='row')

    depth = 4

    res_mtx = calculate_risk_matrix(dsm_i, dsm_p, search_depth=depth)
    res_mtx_t = calculate_risk_matrix(dsm_i_t, dsm_p_t, search_depth=depth)

    for i, _ in enumerate(dsm_p.columns):
        for j, _ in enumerate(dsm_p_t.columns):
            a = res_mtx[i][j]
            b = res_mtx_t[j][i]

            # Ignore diagonal
            if i == j:
                continue

            assert (abs(a - b) < 0.001)


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
