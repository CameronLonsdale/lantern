"""Algorithms for searching and optimisation."""

import copy


def hill_climb(nsteps, start_node, get_next_node):
    """Modular hill climbing algorithm.

    Example:
        >>> def get_next_node(node):
        ...     a, b = random.sample(range(len(node)), 2)
        ...     node[a], node[b] = node[b], node[a]
        ...     plaintext = decrypt(node, ciphertext)
        ...     score = lantern.score(plaintext, *fitness_functions)
        ...     return node, score, Decryption(plaintext, ''.join(node), score)
        >>> final_node, best_score, outputs = hill_climb(10, "ABC", get_next_node)

    Args:
        nsteps (int): The number of neighbours to visit
        start_node: The starting node
        get_next_node (function): Function to return the next node
            the score of the current node and any optional output from the current node

    Returns:
        The highest node found, the score of this node and the outputs from the best nodes along the way
    """
    outputs = []
    best_score = -float('inf')

    for step in range(nsteps):
        next_node, score, output = get_next_node(copy.deepcopy(start_node))

        # Keep track of best score and the start node becomes finish node
        if score > best_score:
            start_node = copy.deepcopy(next_node)
            best_score = score
            outputs.append(output)

    return start_node, best_score, outputs
