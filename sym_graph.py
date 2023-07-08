import json
from random import sample


class Vertex:
    # --------------------- TAL'S CODE START---------------------#
    def __init__(self, baddr, instructions: str, path_len: int, path_num: int, key, constraint: list = []):
        self.baddr = baddr
        self.instructions = instructions
        self.constraint = constraint
        self.paths_constraints = []
        self.path_len = path_len  # added this vertex param to indicate path length to the vertex
        self.path_num = path_num  # added this vertex param to indicate baddr is from deifferent path
        self.id = key

    # --------------------- TAL'S CODE END---------------------#

    # we define uniqueness by address only
    def __eq__(self, other):
        assert (isinstance(other, Vertex))
        return self.baddr == other.baddr

    def __str__(self):
        if self.id == "loopSeerDum":
            return f'{{ "block_addr": {self.baddr}, "path_num": {self.path_num}, "instructions": "{self.instructions}",' \
                   f'"id": {self.id}, "constraints": {self.constraint} }}'
        return f'{{ "block_addr": {self.baddr}, "path_num": {self.path_num}, "instructions": "{self.instructions}",' \
               f'"id": "{self.id}", "constraints": {self.constraint} }}'


class Edge:
    def __init__(self, source: str, dest: str):
        self.source = source
        self.dest = dest

    def __eq__(self, other):
        assert (isinstance(other, Edge))
        return (self.source == other.source and self.dest == other.dest)

    def __str__(self):
        if self.dest == "loopSeerDum":
            return f'{{ "src": \"{self.source}\", "dst": {self.dest} }}'
        return f'{{ "src": \"{self.source}\", "dst": \"{self.dest}\" }}'


class SymGraph:  # TODO: sanity check, when graph is done, vertices.keys() length is same as edges.keys()
    def __init__(self, root: Vertex, func_name: str = "unknown_function", path_constraints_len_limit: int = 5000,
                 path_len_limit: int = 100):
        self.root = root
        self.path_constraints_len_limit = path_constraints_len_limit
        self.path_len_limit = path_len_limit
        self.vertices = {}
        self.edges = {}
        self.addVertex(root)
        self.func_name = func_name

    # --------------------- TAL'S CODE START---------------------#
    def addVertex(self, vertex: Vertex):
        vertex.constraint = list(filter(None, vertex.constraint))

        # We do not want to save excessively long constraints or long paths
        if vertex.path_len > self.path_len_limit:
            return False

        sum_c = 0
        for c in vertex.constraint:
            sum_c = sum_c + len(c)
        if sum_c > self.path_constraints_len_limit:
            return False
        len_and_constraint = [vertex.path_len, vertex.constraint]

        if vertex.id in self.vertices:
            self.vertices[vertex.id].constraint.append(len_and_constraint)
        else:
            self.vertices[vertex.id] = vertex
            self.vertices[vertex.id].constraint = [len_and_constraint]
            self.vertices[vertex.id].id = vertex.id

        if (vertex.id not in self.edges.keys()):
            self.edges[vertex.id] = []
        return True
    # --------------------- TAL'S CODE END---------------------#

    def addEdge(self, edge: Edge):
        # if not (edge.source in self.vertices.keys() and edge.source in self.edges.keys()) \
        #         or not (edge.dest in self.vertices.keys() and edge.dest in self.edges.keys()):
        #     # This exists only for debugging purposes
        #     print(f"edge.source={edge.source}")
        #     print(f"edge.dest={edge.dest}")
        #     print(f"vertices={self.vertices.keys()}")
        #     print(f"edges={self.edges.keys()}")

        if edge.source not in self.vertices.keys():
            print("<------------------->")
            print(f"edge.source= {edge.source}, not in self.vertices.keys() = {self.vertices.keys()}")

        if edge.source not in self.edges.keys():
            print("<------------------->")
            print(f"edge.source = {edge.source}, not in self.edges.keys() = {self.edges.keys()}")

        if edge.dest not in self.vertices.keys():
            print("<------------------->")
            print(f"edge.dest = {edge.dest}, not in self.vertices.keys() = {self.vertices.keys()}")

        if edge.dest not in self.edges.keys():
            print("<------------------->")
            print(f"edge.dest= {edge.dest}, not in self.edges.keys() = {self.edges.keys()}")

        assert (edge.source in self.vertices.keys() and edge.source in self.edges.keys())
        assert (edge.dest in self.vertices.keys() and edge.dest in self.edges.keys())

        if (edge not in self.edges[edge.source]):
            self.edges[edge.source].append(edge)

    # TODO: redo the printing!
    def __str__(self):
        res = f'{{ "func_name": "{self.func_name}",'
        res += f'"GNN_DATA": {{ '
        res += f'"nodes": [ '
        res += ', '.join([str(v) for v in list(self.vertices.values())])

        res += f' ], "edges": [ '
        all_edges = [item for sublist in self.edges.values() for item in sublist]
        res += ', '.join([str(e) for e in all_edges])

        res += f' ] }} }}'
        return res


