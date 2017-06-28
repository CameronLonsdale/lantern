"""Test the search analysis module"""

import random

from lantern.analysis.search import hill_climb


def test_hill_climb():
    """Testing hillclimb to reach a sorted version of the node 'cba'"""
    def get_next_node(node):
        a, b = random.sample(range(len(node)), 2)
        node[a], node[b] = node[b], node[a]
        score = 0
        if node[0] == "a": score += 1
        if node[1] == "b": score += 1
        if node[2] == "c": score += 1

        return node, score, None

    final_node, best_score, _ = hill_climb(50, list("cba"), get_next_node)
    assert ''.join(final_node) == "abc"
