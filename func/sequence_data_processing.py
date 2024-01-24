def generate_graph_and_training_data(frequent_sequences):
    items = set()
    for _, sequence in frequent_sequences:
        items.update(sequence)
    items = list(items)

    # 初始化 graph_data
    graph_data = {item: [0] * len(items) for item in items}
    item_index = {item: index for index, item in enumerate(items)}

    # 分析序列中的位置关系来填充 graph_data
    for _, sequence in frequent_sequences:
        for i in range(len(sequence) - 1):
            graph_data[sequence[i]][item_index[sequence[i + 1]]] = 1

    training_data = {item: [] for item in items}

    for _, sequence in frequent_sequences:
        column = [1 if item in sequence else 0 for item in items]
        for item in items:
            training_data[item].append(column[items.index(item)])

    return graph_data, training_data


def main():
    frequent_sequences = [
        (4, ['牛奶']),
        (2, ['牛奶', '面包']),
        (2, ['牛奶', '饼干']),
        (4, ['面包']),
        (2, ['面包', '饼干']),
        (3, ['饼干'])
    ]

    graph_data, training_data = generate_graph_and_training_data(frequent_sequences)
    print("Graph Data:")
    print(graph_data)
    print("\nTraining Data:")
    print(training_data)


if __name__ == "__main__":
    main()
