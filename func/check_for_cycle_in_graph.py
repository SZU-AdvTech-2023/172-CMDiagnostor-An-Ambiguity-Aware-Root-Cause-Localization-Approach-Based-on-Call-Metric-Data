def dfs(graph, node, visited, rec_stack, path):
    """
    Helper function for depth-first search that also finds the complete cycle path.

    :param graph: The graph represented as adjacency list.
    :param node: The current node being visited.
    :param visited: Set of already visited nodes.
    :param rec_stack: Stack to keep track of the nodes in the current path.
    :param path: List to record the path of nodes.
    :return: A list representing a cycle if found, otherwise None.
    """
    visited.add(node)
    rec_stack.add(node)
    path.append(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            result = dfs(graph, neighbor, visited, rec_stack, path)
            if result is not None:
                return result
        elif neighbor in rec_stack:
            # Found a cycle, return the path
            cycle_start_index = path.index(neighbor)
            return path[cycle_start_index:] + [neighbor]

    path.pop()  # Remove the current node from the path as we backtrack
    rec_stack.remove(node)
    return None


def check_for_cycle(graph_data):
    """
    Detects if there is a cycle in the graph and returns the complete cycle path.

    :param graph_data: Graph data as a dictionary where keys are nodes and values are lists of neighbors.
    :return: A list representing a complete cycle if found, otherwise None.
    """
    # Convert graph_data to adjacency list
    graph = {node: [] for node in graph_data}
    for node, edges in graph_data.items():
        for neighbor_index, has_edge in enumerate(edges):
            if has_edge:
                neighbor = list(graph_data.keys())[neighbor_index]
                graph[node].append(neighbor)

    visited = set()
    rec_stack = set()

    for node in graph:
        if node not in visited:
            cycle = dfs(graph, node, visited, rec_stack, [])
            if cycle:
                return cycle
    return None


