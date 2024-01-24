def dfs(graph, node, visited, rec_stack):
    """
    Helper function for depth-first search that also finds the edges forming a cycle.

    :param graph: The graph represented as adjacency list.
    :param node: The current node being visited.
    :param visited: Set of already visited nodes.
    :param rec_stack: Stack to keep track of the nodes in the current path.
    :return: A list of edges representing a cycle if found, otherwise None.
    """
    visited.add(node)
    rec_stack.add(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            result = dfs(graph, neighbor, visited, rec_stack)
            if result is not None:
                return result + [(node, neighbor)]
        elif neighbor in rec_stack:
            # Found a cycle, return the edge
            return [(node, neighbor)]

    rec_stack.remove(node)
    return None


def check_for_cycle(graph_data):
    """
    Detects if there is a cycle in the graph and returns the edges forming the cycle.

    :param graph_data: Graph data as a dictionary where keys are nodes and values are lists of neighbors.
    :return: A list of edges representing a cycle if found, otherwise None.
    """
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
            cycle = dfs(graph, node, visited, rec_stack)
            if cycle:
                return cycle
    return None


def remove_edge(graph_data, edge_to_remove):
    """
    Removes an edge from the graph.

    :param graph_data: Graph data as a dictionary.
    :param edge_to_remove: The edge to be removed, represented as a tuple (source, target).
    """
    source, target = edge_to_remove
    target_index = list(graph_data.keys()).index(target)
    graph_data[source][target_index] = 0


# TODO:删除的环的选择

# 用户输入选择删除哪条边
# def cycle_modify(graph_data):
#     while True:
#         cycle_edges = check_for_cycle(graph_data)
#         if not cycle_edges:
#             print("No cycle found. Graph is now acyclic.")
#             break
#
#         print("Found a cycle:")
#         for i, edge in enumerate(cycle_edges):
#             print(f"{i}: {edge}")
#
#         try:
#             choice = int(input("Enter the number of the edge you want to remove: "))
#             if 0 <= choice < len(cycle_edges):
#                 edge_to_remove = cycle_edges[choice]
#                 remove_edge(graph_data, edge_to_remove)
#                 print("Edge removed:", edge_to_remove)
#             else:
#                 print("Invalid choice. No edge removed.")
#         except ValueError:
#             print("Invalid input. Please enter a number.")
#
#     return graph_data

# 删除具有最小confidence的边
def cycle_modify(graph_data, edges_with_confidence):
    """
    Detects and removes the edge with the lowest confidence in any cycle found in the graph_data until no cycle is found.

    :param graph_data: Graph data as a dictionary.
    :param edges_with_confidence: List of edges with their confidence.
    :return: Modified graph_data with cycles removed.
    """
    i = 0
    while True:
        cycle_edges = check_for_cycle(graph_data)
        if not cycle_edges:
            print("No cycle found. Graph is now acyclic.")
            break

        # 查找并删除具有最小confidence的边
        edge_to_remove = min(cycle_edges, key=lambda edge: next(
            (conf for src, tgt, conf in edges_with_confidence if src == edge[0] and tgt == edge[1]), float('inf')))
        remove_edge(graph_data, edge_to_remove)
        i += 1
        print(f"Cycle found. Removing edge: {edge_to_remove}")

    print("Total number of edges removed:", i)
    return graph_data

# 删除具有最小confidence的边并且打印置信度
# def cycle_modify(graph_data, edges_with_confidence):
#     """
#     Detects and removes the edge with the lowest confidence in any cycle found in the graph_data until no cycle is found,
#     and prints the confidence of the removed and remaining edges in the cycle.
#
#     :param graph_data: Graph data as a dictionary.
#     :param edges_with_confidence: List of edges with their confidence.
#     :return: Modified graph_data with cycles removed.
#     """
#     i = 0
#     while True:
#         cycle_edges = check_for_cycle(graph_data)
#         if not cycle_edges:
#             print("No cycle found. Graph is now acyclic.")
#             break
#
#         # 查找并删除具有最小confidence的边
#         edge_to_remove, min_confidence = min(
#             ((edge, conf) for edge in cycle_edges for src, tgt, conf in edges_with_confidence if src == edge[0] and tgt == edge[1]),
#             key=lambda x: x[1],
#             default=(None, float('inf'))
#         )
#         if edge_to_remove:
#             remove_edge(graph_data, edge_to_remove)
#             i += 1
#             print(f"Cycle found. Removing edge: {edge_to_remove} with confidence {min_confidence}")
#             # 打印未被删除边的置信度
#             for edge in cycle_edges:
#                 if edge != edge_to_remove:
#                     remaining_confidence = next((conf for src, tgt, conf in edges_with_confidence if src == edge[0] and tgt == edge[1]), None)
#                     print(f"Remaining edge: {edge} with confidence {remaining_confidence}")
#
#     print("Total number of edges removed:", i)
#     return graph_data


# if __name__ == "__main__":
#     graph_data = {
#         'A': [0, 1, 0, 0],
#         'B': [1, 0, 0, 0],
#         'C': [0, 0, 0, 1],
#         'D': [0, 0, 1, 0],
#
#     }
#     cycle_modify(graph_data)
