from prefixspan import PrefixSpan

def prefixspan_sequential_patterns(dataset, min_support):
    """
    使用PrefixSpan算法进行顺序模式挖掘。

    :param dataset: 一个序列列表，每个序列是项的列表。
    :param min_support: 最小支持度的绝对值。
    :return: 频繁序列模式的列表。
    """
    ps = PrefixSpan(dataset)
    patterns = ps.frequent(min_support)
    return patterns

def main():
    # 示例数据集
    dataset = [
        ['A', 'B', 'C'],
        ['B', 'C', 'D'],
        ['A', 'C', 'D'],
        ['A', 'B', 'C', 'D'],
        ['A', 'B', 'C']
    ]

    # 设置最小支持度
    min_support = 2  # 支持度的绝对值

    # 执行PrefixSpan算法
    patterns = prefixspan_sequential_patterns(dataset, min_support)

    # 打印结果
    print("Frequent Sequential Patterns:")
    for pattern in patterns:
        print(pattern)

if __name__ == "__main__":
    main()
