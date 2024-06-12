from typing import Any, Optional


class DSM:

    def __init__(self, matrix: Any, columns: list[str]):
        self.matrix = matrix
        self.columns = columns
        self.node_network: dict[int, 'GraphNode'] = self.build_node_network()

    def __str__(self):
        return f'{self.columns}\n{self.matrix}'

    def build_node_network(self) -> dict[int, 'GraphNode']:
        network_dict = {}
        for index, col in enumerate(self.columns):
            network_dict[index] = GraphNode(index, col)

        for i, row in enumerate(self.matrix):
            for j, col in enumerate(row):
                # Ignore diagonal
                if i == j:
                    continue
                # Ignore empty cells
                if not col:
                    continue
                # Add interaction to node network
                network_dict[i].add_neighbour(network_dict[j], col)

        return network_dict


class GraphNode:

    def __init__(self, index, name):
        self.index: int = index
        self.neighbours: dict[int, float] = {}  # Maps graph node index to cost
        self.name: str = name

    def __str__(self):
        return f"{self.index}[{self.neighbours.keys()}"

    def add_neighbour(self, neighbour, cost):
        self.neighbours[neighbour.index] = cost

    def get_path_weight(self, index):
        if index not in self.neighbours:
            return None
        else:
            return self.neighbours[index]


class ChangePropagationLeaf:
    def __init__(self, node: GraphNode, parent: 'ChangePropagationLeaf' = None):
        self.node: GraphNode = node
        self.parent: Optional['ChangePropagationLeaf'] = parent


class ChangePropagationTree:
    """
    Used to calculate how the start node affects the end node
    """
    def __init__(self, start_index: int, target_index: int, dsm_impact: DSM, dsm_likelihood: DSM):
        self.dsm_impact: DSM = dsm_impact
        self.dsm_likelihood: DSM = dsm_likelihood
        self.start_index: int = start_index
        self.target_index: int = target_index

    def propagate (self, levels: int = 1) -> float:
        network = self.dsm_impact.node_network

        print(f"Searching for paths from {network[self.start_index].name} to {network[self.target_index].name}")

        start_leaf = ChangePropagationLeaf(network[self.start_index])
        search_stack = [start_leaf]
        visited_nodes = set()
        end_leafs: list[ChangePropagationLeaf] = []

        while len(search_stack) > 0:
            current_leaf = search_stack.pop(0)

            if current_leaf.node.index != self.target_index:
                visited_nodes.add(current_leaf.node.index)

            print(f'Visiting {current_leaf.node.name}, which has {len(current_leaf.node.neighbours)} neighbors.')

            if current_leaf.node.index == self.target_index:
                print("Found target")
                end_leafs.append(current_leaf)
                continue

            for neighbour in current_leaf.node.neighbours:
                cpf = ChangePropagationLeaf(network[neighbour], current_leaf)

                if cpf.node.index not in visited_nodes:
                    search_stack.append(cpf)

        print(f"Found {len(end_leafs)} solutions")
        print(end_leafs)

        for index, end_leaf in enumerate(end_leafs):

            leaf = end_leaf

            while leaf:
                print(f"{index}: {leaf.node.name}")
                leaf = leaf.parent

        return 0.3







