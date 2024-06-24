from cpm.parse import parse_csv


def test_parse_dsm_header():
    dsm = parse_csv('./tests/test-assets/dsm-simple-symmetrical.csv')

    assert dsm.columns[0] == 'A'
    assert dsm.columns[1] == 'B'
    assert dsm.columns[2] == 'C'
    assert dsm.columns[3] == 'D'
    assert len(dsm.columns) == 4


def test_parse_dsm_matrix():
    dsm = parse_csv('./tests/test-assets/dsm-simple-symmetrical.csv')

    should_be = [[None, 0.1, 0.2, 0.3],
                 [0.1, None, 0.4, 0.5],
                 [0.2, 0.4, None, 0.6],
                 [0.3, 0.5, 0.6, None]]

    for i, row in enumerate(should_be):
        for j, col in enumerate(row):
            assert should_be[i][j] == dsm.matrix[i][j]


def test_parse_dsm_network():
    dsm = parse_csv('./tests/test-assets/dsm-network-test.csv')
    assert dsm.node_network[3].name == 'D'
    d_neighbours = list(dsm.node_network[3].neighbours.keys())
    assert len(d_neighbours) == 1   # Should only have one connection
    assert d_neighbours[0] == 0     # Has neighbour with A
    a_neighbours = list(dsm.node_network[0].neighbours.keys())
    assert len(a_neighbours) == 1   # Should only have one
    assert a_neighbours[0] == 2     # A should be neighbour with C
    c_neighbours = list(dsm.node_network[2].neighbours.keys())
    assert len(c_neighbours) == 1
    assert c_neighbours[0] == 1
    b_neighbours = list(dsm.node_network[1].neighbours.keys())
    assert len(b_neighbours) == 1
    assert b_neighbours[0] == 3


def test_parse_dsm_network_instigator_row():
    dsm = parse_csv('./tests/test-assets/dsm-network-test.csv', instigator='row')
    assert dsm.node_network[3].name == 'D'
    d_neighbours = list(dsm.node_network[3].neighbours.keys())
    assert len(d_neighbours) == 1   # Should only have one connection
    assert d_neighbours[0] == 1     # Has neighbour with B
    b_neighbours = list(dsm.node_network[1].neighbours.keys())
    assert len(b_neighbours) == 1   # Should only have one
    assert b_neighbours[0] == 2     # B should be neighbour with C
    c_neighbours = list(dsm.node_network[2].neighbours.keys())
    assert len(c_neighbours) == 1
    assert c_neighbours[0] == 0
    a_neighbours = list(dsm.node_network[0].neighbours.keys())
    assert len(a_neighbours) == 1
    assert a_neighbours[0] == 3


def test_parse_file_object():
    path = './tests/test-assets/dsm-network-test.csv'
    with open(path) as file:
        dsm = parse_csv(file)

        for col in ['A', 'B', 'C', 'D']:
            assert col in dsm.columns
