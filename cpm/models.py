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
                network_dict[i].add_neighbour(network_dict[j], float(col))  # Assumes cell only contains a float.

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


class ChangePropagationLeaf:
    def __init__(self, node: GraphNode, impact_node: GraphNode, parent: 'ChangePropagationLeaf' = None):
        self.node: GraphNode = node
        self.impact_node: GraphNode = impact_node
        self.parent: Optional['ChangePropagationLeaf'] = parent
        self.level: int = self.set_level()
        self.next: dict[int, 'ChangePropagationLeaf'] = {}  # index -> leaf

    def set_level(self):
        level = 0
        node = self.parent

        while node:
            level += 1
            node = node.parent

        return level

    def get_probability(self):

        if len(self.next) == 0:
            return 1

        prob = 1

        for next_index in self.next:
            # Likelihood of propagating to this node
            to_this = self.next[next_index].node.neighbours[self.node.index]
            # Likelihood of that node being propagated to:
            to_next = self.next[next_index].get_probability()
            prob = prob * (1 - to_this * to_next)

        return 1 - prob

    def get_risk(self):

        if len(self.next) == 0:
            return self.impact_node.neighbours[self.parent.node.index]

        prob = 1

        for next_index in self.next:
            # Likelihood of propagating to this node
            to_this = self.next[next_index].node.neighbours[self.node.index]
            # Likelihood of that node being propagated to:
            to_next = self.next[next_index].get_risk()
            # Impact of propagating to this node from next

            prob = prob * (1 - to_this * to_next)

        print(self.node.name)

        return 1 - prob


class ChangePropagationTree:
    """
    Used to calculate how the start node affects the end node
    """
    def __init__(self, start_index: int, target_index: int, dsm_impact: DSM, dsm_likelihood: DSM):
        self.dsm_impact: DSM = dsm_impact
        self.dsm_likelihood: DSM = dsm_likelihood
        self.start_index: int = start_index
        self.target_index: int = target_index
        self.start_leaf: ChangePropagationLeaf = None

    def propagate_back(self, end_leaf: ChangePropagationLeaf):
        current_leaf = end_leaf

        while current_leaf:
            if current_leaf.parent:
                current_leaf.parent.next[current_leaf.node.index] = current_leaf

            current_leaf = current_leaf.parent

    def propagate(self, search_depth: int = 4) -> float:
        network = self.dsm_likelihood.node_network

        print(f"Searching for paths from {network[self.start_index].name} to {network[self.target_index].name}")

        self.start_leaf = ChangePropagationLeaf(network[self.start_index], self.dsm_impact.node_network[self.start_index])
        search_stack = [self.start_leaf]
        visited_nodes = set()
        end_leafs: list[ChangePropagationLeaf] = []

        while len(search_stack) > 0:
            current_leaf = search_stack.pop(0)

            print(f'Visiting {current_leaf.node.name}, which has {len(current_leaf.node.neighbours)} neighbors.')

            if current_leaf.node.index == self.target_index:
                print("Found target")
                end_leafs.append(current_leaf)

                # Propagate back and register path
                self.propagate_back(current_leaf)

                continue

            for neighbour in current_leaf.node.neighbours:

                # Trace back and ensure that we do not create circular paths
                leaf_back_trace = current_leaf
                already_visited = False
                while leaf_back_trace.parent:
                    if neighbour == leaf_back_trace.parent.node.index:
                        already_visited = True
                        break
                    leaf_back_trace = leaf_back_trace.parent
                if already_visited:
                    continue

                cpf = ChangePropagationLeaf(network[neighbour], self.dsm_impact.node_network[neighbour], current_leaf)

                if cpf.node.index not in visited_nodes and cpf.level <= search_depth:
                    search_stack.append(cpf)

        print(f"Found {len(end_leafs)} solutions")

        return self.construct_paths()

    def construct_paths(self):
        risk = self.start_leaf.get_risk()
        prob = self.start_leaf.get_probability()
        print(f'probability: {prob}\t\trisk: {risk}')
        return risk

