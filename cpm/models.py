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

    def get_path_weight(self, index):
        if index not in self.neighbours:
            return None
        else:
            return self.neighbours[index]


class ChangePropagationLeaf:
    def __init__(self, node: GraphNode, parent: 'ChangePropagationLeaf' = None):
        self.node: GraphNode = node
        self.parent: Optional['ChangePropagationLeaf'] = parent
        self.level: int = self.set_level()
        self.next = []

    def set_level(self):
        level = 0
        node = self.parent

        while node:
            level += 1
            node = node.parent

        return level


class ChangePropagationPath:

    def __init__(self, dsm_impact: DSM):
        self.leaf_array: list[ChangePropagationLeaf] = []
        self.probability: float = 1
        self.dsm_impact = dsm_impact
        self.impact = -1

    def set_next(self, leaf: ChangePropagationLeaf):
        self.leaf_array.insert(0, leaf)

        if leaf.parent:
            self.probability *= leaf.node.neighbours[leaf.parent.node.index]

            # If this is the first connection (which is the end of the path) then store the impact.
            # We only care about the impact of the final path.
            if len(self.leaf_array) == 1:
                self.impact = self.dsm_impact.node_network[leaf.node.index].get_path_weight(leaf.parent.node.index)

            print(f'Path weight: {self.probability}')

    def __str__(self) -> str:
        obj_str = ""
        for index, leaf in enumerate(self.leaf_array):
            obj_str += leaf.node.name
            if index < len(self.leaf_array) - 1:
                obj_str += " --> "

        return obj_str


class ChangePropagationTree:
    """
    Used to calculate how the start node affects the end node
    """
    def __init__(self, start_index: int, target_index: int, dsm_impact: DSM, dsm_likelihood: DSM):
        self.dsm_impact: DSM = dsm_impact
        self.dsm_likelihood: DSM = dsm_likelihood
        self.start_index: int = start_index
        self.target_index: int = target_index

    def propagate(self, search_depth: int = 4) -> float:
        network = self.dsm_impact.node_network

        print(f"Searching for paths from {network[self.start_index].name} to {network[self.target_index].name}")

        start_leaf = ChangePropagationLeaf(network[self.start_index])
        search_stack = [start_leaf]
        visited_nodes = set()
        end_leafs: list[ChangePropagationLeaf] = []

        while len(search_stack) > 0:
            current_leaf = search_stack.pop(0)

            print(f'Visiting {current_leaf.node.name}, which has {len(current_leaf.node.neighbours)} neighbors.')

            if current_leaf.node.index == self.target_index:
                print("Found target")
                end_leafs.append(current_leaf)
                continue

            for neighbour in current_leaf.node.neighbours:
                # At this stage we COULD check if the neighbour is already part of the path to avoid circular references
                # But it is not obvious that this would save computational expense. We can try it if the algorithm
                # performs poorly.

                cpf = ChangePropagationLeaf(network[neighbour], current_leaf)

                if cpf.node.index not in visited_nodes and cpf.level <= search_depth:
                    search_stack.append(cpf)

        print(f"Found {len(end_leafs)} solutions")

        paths = self.construct_paths(end_leafs)

        return self.calculate_risk(paths)


    def construct_paths(self, end_leafs: list[ChangePropagationLeaf]) -> list[ChangePropagationPath]:

        risk_array = []
        paths_array = []

        for index, end_leaf in enumerate(end_leafs):
            leaf = end_leaf

            path_str_array = []
            current_path = ChangePropagationPath(self.dsm_impact)

            while leaf:
                path_str_array.append(f"[{index}] {leaf.node.name}")

                current_path.set_next(leaf)

                if not leaf.parent:
                    break

                leaf = leaf.parent

            risk = 1 - current_path.impact * current_path.probability
            risk_array.append(risk)
            paths_array.append(current_path)

            print(current_path)

        multiplied_risk = 1
        for risk in risk_array:
            multiplied_risk *= risk

        return paths_array

    def calculate_risk(self, paths: list[ChangePropagationPath], algorithm: str = 'cambridge') -> float:

        if algorithm == 'cambridge':
            return self.cambridge_risk_algorithm(paths)
        else:
            raise ValueError('Unknown algorithm: ' + algorithm)

    def cambridge_risk_algorithm(self, paths):
        pass

    def cambridge_risk_algorithm_test(self, paths) -> float:

        high_level_or_gates: dict[str, list[ChangePropagationPath]] = {}
        gate_probabilities: dict[str, float] = {}

        for path in paths:
            gate_key = str(path.leaf_array[0].node.index) + "-" + str(path.leaf_array[1].node.index)

            if gate_key not in high_level_or_gates:
                high_level_or_gates[gate_key] = []

            high_level_or_gates[gate_key].append(path)

        for gate_key in high_level_or_gates:
            gate_probability = 1

            for path in high_level_or_gates[gate_key]:
                gate_probability *= 1 - path.probability

            gate_probability = 1 - gate_probability
            gate_probabilities[gate_key] = gate_probability

        risk = 1
        for gate_key in gate_probabilities:
            impact = 0.5
            risk *= 1 - gate_probabilities[gate_key]

        return 1 - risk












