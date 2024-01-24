from prefixspan import PrefixSpan

def mine_sequential_patterns(dataset, min_support):
    """
    使用前缀跨度算法挖掘序列模式。

    参数:
    dataset: 一个列表的列表，表示序列数据。
    min_support: 一个整数，表示最小支持度。

    返回:
    一个列表，其中每个元素都是一个频繁序列及其支持度。
    """
    ps = PrefixSpan(dataset)
    frequent_sequences = ps.frequent(min_support)
    # 打印结果
    for sequence in frequent_sequences:
        print(sequence)
    return frequent_sequences

def main():
    # 示例数据集
    dataset = [['牛奶', '面包'],
               ['牛奶', '饼干'],
               ['面包', '饼干', '牛奶'],
               ['牛奶', '面包', '饼干'],
               ['面包', '苹果']]

    # 最小支持度设为2
    min_support = 2

    # 调用函数进行顺序模式挖掘
    frequent_sequences = mine_sequential_patterns(dataset, min_support)

    # 打印结果
    for sequence in frequent_sequences:
        print(sequence)

if __name__ == "__main__":
    main()
