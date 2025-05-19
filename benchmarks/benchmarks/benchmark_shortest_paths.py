"""Benchmarks for shortest path algorithms"""

import networkx as nx
from benchmarks.utils import BenchmarkGraph, generate_weighted_graph


class AlgorithmBenchmarks:
    timeout = 120
    _graphs = [
        BenchmarkGraph.from_func(f, *args)
        for nodes in [10, 100, 1000]
        for f, args in [
            (nx.erdos_renyi_graph, (nodes, 1 / nodes)),
            (nx.erdos_renyi_graph, (nodes, 0.1)),
            (nx.erdos_renyi_graph, (nodes, 0.5)),
            (nx.erdos_renyi_graph, (nodes, 0.9)),
            (nx.random_labeled_tree, (nodes,)),
            (nx.path_graph, (nodes,))
        ]
    ] + [
        BenchmarkGraph.from_func(generate_weighted_graph, 20, f, *args)
        for nodes in [10, 100, 1000]
        for f, args in [
            (nx.erdos_renyi_graph, (nodes, 1 / nodes)),
            (nx.erdos_renyi_graph, (nodes, 0.1)),
            (nx.erdos_renyi_graph, (nodes, 0.5)),
            (nx.erdos_renyi_graph, (nodes, 0.9)),
            (nx.random_labeled_tree, (nodes,)),
            (nx.path_graph, (nodes,))
        ]
    ]
    params = [x.name for x in _graphs]

    param_names = ["graph"]

    def setup(self, graph):
        self.graphs_dict = dict(zip(self.params, self._graphs))

    def time_single_source_dijkstra(self, graph):
        # timing this should also give us information about
        # underlying shortest path methods
        G = self.graphs_dict[graph]
        for source in G:
            for target in G:
                _ = nx.single_source_dijkstra(G, source, target)
