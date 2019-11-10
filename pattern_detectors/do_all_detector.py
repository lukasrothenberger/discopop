from typing import List

import numpy as np
from graph_tool import Vertex, Graph
from graph_tool.util import find_vertex

from utils import find_subnodes, is_depending, correlation_coefficient

do_all_threshold = 0.9


class DoAllInfo(object):
    """Class, that contains do-all detection result
    """
    node: Vertex
    node_id: str
    coefficient: float
    start_line: str
    end_line: str

    def __init__(self, graph: Graph, node: Vertex, coefficient: float):
        """
        :param graph: CU graph
        :param node: node, where do-all was detected
        :param coefficient: correlation coefficient
        """
        self.node = node
        self.node_id = graph.vp.id[node]
        self.coefficient = coefficient
        self.start_line = graph.vp.startsAtLine[node]
        self.end_line = graph.vp.endsAtLine[node]

    def __str__(self):
        return f'Do-all at: {self.node_id}\n' \
               f'Coefficient: {self.coefficient}\n' \
               f'Start line: {self.start_line}\n' \
               f'End line: {self.end_line}'


def run_detection(graph: Graph) -> List[DoAllInfo]:
    """Search for do-all loop pattern

    :param graph: CU graph
    :return: List of detected pattern info
    """
    result = []
    for node in find_vertex(graph, graph.vp.type, 'loop'):
        val = __detect_do_all(graph, node)
        if val > do_all_threshold:
            graph.vp.doAll[node] = val
            if not graph.vp.reduction[node]:
                result.append(DoAllInfo(graph, node, graph.vp.doAll[node]))

    return result


def __detect_do_all(graph: Graph, root: Vertex):
    """Calculate do-all value for node

    :param graph: CU graph
    :param root: root node
    :return: do-all scalar value
    """
    graph_vector = []

    subnodes = find_subnodes(graph, root, 'child')

    for i in range(0, len(subnodes)):
        for j in range(i, len(subnodes)):
            if is_depending(graph, subnodes[i], subnodes[j], root):
                graph_vector.append(0)
            else:
                graph_vector.append(1)

    pattern_vector = [1 for _ in graph_vector]

    if np.linalg.norm(graph_vector) == 0:
        return 0

    return correlation_coefficient(graph_vector, pattern_vector)
