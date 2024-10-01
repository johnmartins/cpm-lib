from typing import Optional


class DSM:
    """
    Design Structure Matrix Class contains possible interactions between sub-systems.
    Typically, when performing Change Propagation analysis, there are two DSMs:
    one DSM for the likelihood of propagation, and one DSM for the impact of propagation.
    """

    def __init__(self, matrix: list[list[Optional[float]]], columns: list[str], instigator='column'):
        """
        Construct a DSM using a matrix and column-header
        :param matrix: List matrix containing floats or empty cells
        :param columns: Matrix header
        :param instigator: Can either be **column** or **row**. Determines directionality of interactions in DSM.
        By default, propagation travels from column to row
        """
        self.matrix = matrix
        self.columns = columns
        self.node_network: dict[int, 'GraphNode'] = self.build_node_network(instigator)

    def __str__(self):
        return f'{self.columns}\n{self.matrix}'

    def build_node_network(self, instigator: str) -> dict[int, 'GraphNode']:
        """
        Construct a node network using the DSM.
        This enables path finding to be run on the system.\n
        **This is done on DSM class instantiation and should probably not be done manually**
        :return:
        """
        network_dict = {}
        for index, col in enumerate(self.columns):
            network_dict[index] = GraphNode(index, col)

        for i, row in enumerate(self.matrix):
            for j, col in enumerate(row):
                # Ignore diagonal
                if i == j:
                    continue
                # Ignore empty cells
                if col == "" or col is None:
                    continue

                numerical_value = 0.0

                try:
                    numerical_value = float(col)
                except ValueError:
                    raise ValueError('Unexpected DSM cell value. Could not be parsed as a float. Control DSM input.')

                # Add interaction to node network
                if instigator == 'column':
                    network_dict[j].add_neighbour(network_dict[i], numerical_value)  # Assumes cell only contains a float.
                elif instigator == 'row':
                    network_dict[i].add_neighbour(network_dict[j], numerical_value)
                else:
                    raise TypeError('Instigator needs to either be "column" or "row".')

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
            from_this = self.node.neighbours[next_index]
            # Likelihood of that node being propagated to:
            to_next = self.next[next_index].get_probability()
            prob = prob * (1 - from_this * to_next)

        return 1 - prob

    def get_risk(self):

        if len(self.next) == 0:

            if self.parent is None:
                # These nodes are not connected.
                return 0

            # If the impact is null, then return 0.
            if self.node.index not in self.parent.impact_node.neighbours:
                raise ValueError('Unexpected empty DSM cell. The final impact cell was null. Check if DSMs are valid.')

            # Final connection is the only one where we care about impact
            return self.parent.impact_node.neighbours[self.node.index]

        prob = 1

        for next_index in self.next:
            # Likelihood of propagating to the next node
            from_this = self.node.neighbours[next_index]
            # Likelihood of that node propagating
            from_next = self.next[next_index].get_risk()
            # Impact of propagating to this node from next

            prob = prob * (1 - from_this * from_next)

        return 1 - prob


class ChangePropagationTree:
    """
    Used to calculate how the start node affects the end node
    """
    def __init__(self, start_index: int, target_index: int, dsm_impact: DSM, dsm_likelihood: DSM):
        """
        Calculate the risk and probability of a change propagating from one sub-system to another.
        :param start_index: Column index for start of propagation
        :param target_index: Column index for propagation target
        :param dsm_impact: Impact DSM
        :param dsm_likelihood: Likelihood DSM
        """
        self.dsm_impact: DSM = dsm_impact
        self.dsm_likelihood: DSM = dsm_likelihood
        self.start_index: int = start_index
        self.target_index: int = target_index
        self.start_leaf: Optional[ChangePropagationLeaf] = None

    def propagate_back(self, end_leaf: ChangePropagationLeaf):
        current_leaf = end_leaf

        while current_leaf:
            if current_leaf.parent:
                current_leaf.parent.next[current_leaf.node.index] = current_leaf

            current_leaf = current_leaf.parent

    def propagate(self, search_depth: int = 4) -> 'ChangePropagationTree':
        """
        Propagate change. This will determine the paths of possible propagation within the system.
        Use `get_risk()` and `get_probability()` to extract the corresponding values.
        :param search_depth:
        :return:
        """
        network = self.dsm_likelihood.node_network

        self.start_leaf = ChangePropagationLeaf(network[self.start_index], self.dsm_impact.node_network[self.start_index])
        search_stack = [self.start_leaf]
        visited_nodes = set()
        end_leafs: list[ChangePropagationLeaf] = []

        while len(search_stack) > 0:
            current_leaf = search_stack.pop(0)

            if current_leaf.node.index == self.target_index:
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

        return self

    def get_risk(self) -> float:
        """
        Get risk of propagation
        :return:
        """
        risk = self.start_leaf.get_risk()
        return risk

    def get_probability(self) -> float:
        """
        Get probability/likelihood of propagation
        :return:
        """
        prob = self.start_leaf.get_probability()
        return prob
