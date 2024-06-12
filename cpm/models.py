from typing import Any


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
            network_dict[index] = GraphNode(index)

        for i, row in enumerate(self.matrix):
            for j, col in enumerate(row):
                # Ignore diagonal
                if i == j:
                    continue
                # Ignore empty cells
                if not col:
                    continue
                # Add interaction to node network
                network_dict[i].add_neighbour(network_dict[j])

        for g in network_dict:
            print(network_dict[g])

        return network_dict


class GraphNode:

    def __init__(self, index):
        self.index: int = index
        self.neighbours: dict[int, 'GraphNode'] = {} # Should map index to cost, no?

    def __str__(self):
        return f"{self.index}[{self.neighbours.keys()}"

    def add_neighbour(self, neighbour):
        self.neighbours[neighbour.index] = neighbour


class ChangePropagationTree:
    """
    Used to calculate how the start node affects the end node
    """
    def __init__(self, start_node, target_node):
        self.start_node:
        self.target_node




