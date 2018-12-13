# Taken from the concept of spanning tree and the concept of BFS
# Breadth First Search Algorithm.
# https://www.sciencedirect.com/topics/engineering/spanning-tree

# 1. Mark all nodes and unvisited and store them
# 2. Set distance to zero for our initial node and to infinity for other nodes
# 3. Select the unvisited node with the smallest distance, its current node now.
# 4. Find unvisited neighbors for curr node and calc distances through the curr node.
#    Compare new calc dist, to the assigned and save the smaller one.
# 5. Mark curr node as visited and remove it from unvisited set
# 6. Stop if the dest node has been visited or if smallest dist unvisited is infinity.
#    if not repeat 3-6.

from collections import deque, namedtuple
#import math

inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def create_edge(start, end, cost=1):
    return Edge(start, end, cost=1)


class GraphIt:

    def __init__(self, edges):
        incorrect_edges = [ i for i in edges if len (i) not in [2, 3]]
        if incorrect_edges:
            raise ValueError('Wrong Edges: {}'.format(incorrect_edges))

        self.edges = [create_edge(*edge) for edge in edges]


    @property
    def vertices(self):
        return set(sum(([edge.start, edge.end] for edge in self.edges), []
                       )
                   )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]

        return node_pairs

    def remove_edges(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start-n2, end=n1, cost=cost))

    @property
    def neighbors(self):
        neighbors = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbors[edge.start].add((edge.end, edge.cost))

        return neighbors

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Source Node does not exist...'
        distances = {vertex: inf for vertex in self.vertices}
        prev_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()
        while vertices:
            curr_vertex = min(
                vertices, key=lambda vertex: distances[vertex]
            )
            if distances[curr_vertex] == inf:
                break

            for neighbor, cost in self.neighbors[curr_vertex]:
                alt_route = distances[curr_vertex] + cost
                if alt_route < distances[neighbor]:
                    distances[neighbor] = alt_route
                    prev_vertices[neighbor] = curr_vertex

            vertices.remove(curr_vertex)

        path, curr_vertex = deque(), dest
        while prev_vertices[curr_vertex] is not None:
            path.appendleft(curr_vertex)
            curr_vertex = prev_vertices[curr_vertex]
        if path:
            path.appendleft(curr_vertex)
        return path


graph = GraphIt([
    ("a", "b", 2),  ("a", "c", 10),  ("a", "f", 3), ("b", "c", 6),
    ("b", "d", 7), ("c", "d", 3), ("c", "f", 5),  ("d", "e", 1),
    ("e", "f", 0)])

print(graph.dijkstra("a", "e"))
