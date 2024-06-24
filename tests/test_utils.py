
from cpm.parse import parse_csv
from cpm.utils import calculate_risk_matrix


def test_matrix_risk_calculation():
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

            print(f'{dsm_answers.matrix[i][j]} {dsm_risk[i][j]}')
            if dsm_answers.matrix[i][j] in [None, 0] and dsm_risk[i][j] in [None, 0]:
                continue
            assert abs(dsm_answers.matrix[i][j] - dsm_risk[i][j]) < 0.001
