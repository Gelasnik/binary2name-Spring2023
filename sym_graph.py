import json
from random import sample


class MetaData:
    def __init__(self, root_id: int = 0, num_paths: int = 0, paths_len=None, num_vertices: int = 0,
                 num_edges: int = 0,
                 num_constraints: int = 0,
                 num_empty_vertices: int = 0):
        if paths_len is None:
            paths_len = []
        self.root_id = root_id
        self.num_paths = num_paths
        self.paths_len = paths_len
        self.num_vertices = num_vertices
        self.num_edges = num_edges
        self.num_constraints = num_constraints
        self.num_empty_vertices = num_empty_vertices

    def __str__(self):
        return f'{{ "root_id": {self.root_id}, ' \
               f'"num_paths": {self.num_paths}, ' \
               f'"paths_len": {self.paths_len}, ' \
               f'"num_vertices": {self.num_vertices}, ' \
               f'"num_edges": {self.num_edges}, ' \
               f'"num_constraints": {self.num_constraints}, ' \
               f'"num_empty_vertices": {self.num_empty_vertices} }}'


class Vertex:
    # --------------------- TAL'S CODE START---------------------#
    def __init__(self, baddr, instructions: str, path_len: int, paths: list, key, constraints=None):
        """
        :param baddr: block address
        :param instructions: block instructions
        :param path_len: length of the path from root to this vertex
        :param paths: array of paths that pass through this vertex
        :param constraints: block constraints
        """
        if constraints is None:
            constraints = []
        self.baddr = baddr
        self.instructions = instructions
        self.constraints = constraints
        self.path_len = path_len
        self.paths = paths
        self.id = key

    # --------------------- TAL'S CODE END---------------------#

    # we define uniqueness by address only
    def __eq__(self, other):
        assert (isinstance(other, Vertex))
        return self.baddr == other.baddr

    def __str__(self):
        if self.id == "loopSeerDum":
            return f'{{ "block_addr": {self.baddr}, "path_num": {self.paths}, "instructions": "{self.instructions}",' \
                   f'"id": {self.id}, "constraints": {self.constraints} }}'
        return f'{{ "block_addr": {self.baddr}, "path_num": {self.paths}, "instructions": "{self.instructions}",' \
               f'"id": "{self.id}", "constraints": {self.constraints} }}'


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
                 path_len_limit: int = 100, num_paths: int = -1):
        self.root = root
        self.path_constraints_len_limit = path_constraints_len_limit
        self.path_len_limit = path_len_limit
        self.vertices: dict[int, Vertex] = {}
        self.edges: dict[int, list:[Edge]] = {}
        self.id_to_addr = {}
        self.meta_data = MetaData(root_id=root.id, num_paths=num_paths)
        self.addVertex(root)
        self.func_name = func_name

    # --------------------- TAL'S CODE START---------------------#
    def getChildrenIds(self, vertex: Vertex):
        edges_from_vertex = self.edges[vertex.id]
        children = [edge.dest for edge in edges_from_vertex]
        return children

    def getVertex(self, id: int):
        return self.vertices[id]

    def addVertex(self, vertex: Vertex):
        vertex.constraints = list(filter(None, vertex.constraints))
        # We do not want to save excessively long constraints or long paths
        if vertex.path_len > self.path_len_limit:
            return

        sum_c = 0
        for c in vertex.constraints:
            sum_c = sum_c + len(c)
        if sum_c > self.path_constraints_len_limit:
            return

        current_path = 0
        if vertex.paths:
            current_path = vertex.paths[-1]

        path_len_and_constraint = [current_path, vertex.path_len, vertex.constraints]
        self.meta_data.num_constraints += len(vertex.constraints)
        if vertex.id in self.vertices:
            self.vertices[vertex.id].constraints.append(path_len_and_constraint)
            self.vertices[vertex.id].paths.extend(vertex.paths)
        else:
            self.vertices[vertex.id] = vertex
            self.vertices[vertex.id].constraints = [path_len_and_constraint]
            self.id_to_addr[vertex.id] = vertex.baddr
            self.meta_data.num_vertices += 1

        if vertex.id not in self.edges.keys():
            self.edges[vertex.id] = []

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

        if edge not in self.edges[edge.source]:
            self.meta_data.num_edges += 1
            self.edges[edge.source].append(edge)

    # TODO: redo the printing!
    def __str__(self):
        self.finalize_metadata()
        res = f'{{ "func_name": "{self.func_name}",'
        res += f'"GNN_DATA": {{ '

        res += f'"meta_data": [ '
        res += str(self.meta_data)

        res += f' ], "nodes": [ '
        res += ', '.join([str(v) for v in list(self.vertices.values())])

        res += f' ], "edges": [ '
        all_edges = [item for sublist in self.edges.values() for item in sublist]
        res += ', '.join([str(e) for e in all_edges])

        res += f' ] }} }}'
        return res

    def finalize_metadata(self):
        self.meta_data.num_empty_vertices = 0
        for vertex in self.vertices.values():
            if not vertex.constraints[-1][-1]:
                self.meta_data.num_empty_vertices += 1

    def add_path_len(self, path_num: int, path_len: int):
        self.meta_data.paths_len.append([path_num, path_len])
