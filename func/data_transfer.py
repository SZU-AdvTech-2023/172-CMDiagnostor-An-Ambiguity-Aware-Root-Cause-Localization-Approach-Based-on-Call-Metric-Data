import pandas as pd
import ast

from func.check_for_cycle_in_graph import check_for_cycle
from func.cycle_modify import cycle_modify



def dfs_remove_cycle(graph, node, visited, rec_stack, path):
    """
    Helper function for depth-first search that also removes a cycle if found.

    :param graph: The graph represented as adjacency list.
    :param node: The current node being visited.
    :param visited: Set of already visited nodes.
    :param rec_stack: Stack to keep track of the nodes in the current path.
    :param path: List to record the path of nodes.
    :return: True if a cycle is found and removed, False otherwise.
    """
    visited.add(node)
    rec_stack.add(node)
    path.append(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            if dfs_remove_cycle(graph, neighbor, visited, rec_stack, path):
                return True
        elif neighbor in rec_stack:
            # Found a cycle, remove an edge to break the cycle
            cycle_start_index = path.index(neighbor)
            cycle = path[cycle_start_index:]
            # Remove the edge from the last node in the cycle to its first node
            graph[cycle[-1]].remove(cycle[0])
            return True

    path.pop()  # Remove the current node from the path as we backtrack
    rec_stack.remove(node)
    return False


def remove_cycle_if_exists(graph_data):
    """
    Detects if there is a cycle in the graph and removes it.

    :param graph_data: Graph data as a dictionary where keys are nodes and values are lists of neighbors.
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
            if dfs_remove_cycle(graph, node, visited, rec_stack, []):
                print(f"Cycle removed from the graph involving node {node}.")
                break

    return graph


def data_transfer(rules):
    data = {'source': [], 'target': []}
    # 遍历关联规则，转换成因果关系
    for index, row in rules.iterrows():
        for antecedent in row['antecedents']:
            for consequent in row['consequents']:
                data['source'].append(antecedent)
                data['target'].append(consequent)

    # data_df = pd.DataFrame(data)
    # 使用循环遍历source和target，并打印它们
    for source, target in zip(data['source'], data['target']):
        print(f"Source: {source}, Target: {target}")

    # 创建一个新的字典来存储转换后的数据
    graph_data = {}

    # 获取所有独立的节点
    nodes = sorted(set(data['source'] + data['target']))

    # 初始化每个节点的连接状态为全0
    for node in nodes:
        graph_data[node] = [0] * len(nodes)

    # 设置有连接的节点状态为1
    for s, t in zip(data['source'], data['target']):
        source_index = nodes.index(s)
        target_index = nodes.index(t)
        graph_data[s][target_index] = 1

    # TODO: 检查环并删除环
    # modified_graph = remove_cycle_if_exists(graph_data)
    # cycle = check_for_cycle(modified_graph)
    # if cycle:
    #     print("The graph contains a cycle:", cycle)
    # else:
    #     print("The graph does not contain a cycle.")
    # 创建包含confidence的边数据
    edges_with_confidence = [(ant, cons, row['confidence']) for index, row in rules.iterrows() for ant in
                             row['antecedents'] for cons in row['consequents']]
    graph_data = cycle_modify(graph_data, edges_with_confidence)
    # 创建 graph_df
    graph_df = pd.DataFrame(graph_data)

    return graph_df
