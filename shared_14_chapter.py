"""
graph and graph related stuff
"""

class Vertex(object):
    __slots__ = '_element'

    def __init__(self, element=None, *args, **kwargs):
        if element is not None:
            self._element = element

    def element(self):
        return self._element

class Edge(object):
    __slots__ = '_origin', '_destination', '_element'

    def __init__(self, origin, destination, element=None, *args, **kwargs):
        self._origin = origin
        self._destination = destination

        if element is not None:
            self._element = element

    def endpoints(self):
        return (self._origin, self._destination)

    def opposite(self, v):
        if v not in (self._origin, self._destination):
            raise Exception('Vertex is not an endpoint of this edge.')
        return self._destination if v == self._origin else self._origin

class Graph(object):

    def __init__(self, directed=False, *args, **kwargs):
        self._outgoing = {}
        self._incoming = self._outgoing if not directed else {}

    def is_directed(self):
        return self._outgoing is not self._incoming

    def insert_vertex(self, element=None):
        v = Vertex(element)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}
        return v

    def insert_edge(self, u, v, element=None):
        e = Edge(u, v, element)
        self._incoming[v][u] = e
        self._outgoing[u][v] = e
        return e

    def incident_edges(self, v, outgoing=True):
        adj = self._outgoing if outgoing else self._incoming
        for e in adj[v].values():
            yield e

    def vertex_count(self):
        return len(self._outgoing)

    def vertices(self):
        return set(self._outgoing.keys())

    def edge_count(self):
        s = sum([len(self._outgoing[v]) for v in self._outgoing])
        return s if self.is_directed() else s // 2

    def edges(self):
        edges = set()
        for v in self._outgoing:
            edges.update(self._outgoing[v].values())
        return edges

    def get_edge(self, u, v):
        return self._outgoing[u].get(v)

    def incident_edges(self, v, outgoing=True):
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def degree(self, v, outgoing=True):
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

if __name__ == "__main__":
    # make a triangle shaped undirected cyclic graph
    g = Graph()
    v1 = g.insert_vertex()
    v2 = g.insert_vertex()
    v3 = g.insert_vertex()

    e1 = g.insert_edge(v1, v2)
    e2 = g.insert_edge(v2, v3)
    e3 = g.insert_edge(v3, v1)

    assert g.edge_count() == 3
    assert g.vertex_count() == 3
    assert not g.is_directed()
    assert g.vertices() == {v1, v2, v3}
    assert g.edges() == {e1, e2, e3}
    assert list(g.incident_edges(v1)) == [e1, e3]
    assert g.degree(v1) == 2
    assert g.get_edge(v3, v1) == e3