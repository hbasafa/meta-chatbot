from src.python.utils.common import get_difference, get_key

GROUND = None
GROUND_LAYER_NAME = None
LAYER_NAME = "layer_name"


class Tree(object):

    def __init__(self, root, **kwargs):
        self.root = root
        self.edges = {(root, GROUND): {LAYER_NAME: kwargs[LAYER_NAME]}}
        self.levels = []

    def add_children(self, children, parent):
        for child in children:
            self.add_node(child, parent)

    def add_layer(self, children, parents=list()):
        if len(parents) == 0:
            parents = self.get_leaves()
        for child in children:
            self.add_node_to_parents(child, parents)

    def add_layer_with_name(self, children, layer_name, parents=list()):
        if len(parents) == 0:
            parents = self.get_leaves()

        self.levels.append(layer_name)

        for child in children:
            self.add_node_to_parents(child, parents, **{LAYER_NAME: layer_name})

    def add_node(self, node, parent, **kwargs):
        e = node, parent
        self.edges.update({e: kwargs})

    def add_node_to_parents(self, node, parents, **kwargs):
        for p in parents:
            self.add_node(node, p, **kwargs)

    def get_leaves(self):
        dicks, asses = zip(*self.get_edges())
        leaves = get_difference(dicks, asses)
        return leaves

    def get_edges(self):
        edges = list(self.edges.keys())
        return edges

    def get_edges_with_attributes(self):
        return self.edges

    def get_levels(self):
        return self.levels

    def print_all(self):
        print(self.get_edges_with_attributes())

    def print(self):
        print(self.get_edges())

    def __str__(self):
        #TODO
        return self.get_edges().__str__()

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        if isinstance(item, str):
            edges = [e for e, v in self.get_edges_with_attributes().items() if v[LAYER_NAME] == item]
            nodes = [s for s, t in edges]
            return nodes
        else:
            raise KeyError


class Node(object):

    def __init__(self, node_id, name):
        self.node_id = node_id
        self.name = name



