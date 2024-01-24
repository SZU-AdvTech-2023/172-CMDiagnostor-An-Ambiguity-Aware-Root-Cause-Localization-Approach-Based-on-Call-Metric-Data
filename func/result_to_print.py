import pandas as pd

from func.bayesian_root_cause_analysis import bayesian_root_cause_analysis
from func.sequence_data_processing import generate_graph_and_training_data
from func.sequential_pattern_mining import mine_sequential_patterns


def get_root_cause_info(results):
    output = ""
    root_causes = set()

    output += "Root Cause Chains:\n"
    for paths in results['root_cause_paths'].values():
        for probability, chain in paths:
            reversed_chain = [(node.split('_')[-1], prob) for node, prob in chain[::-1]]
            output += " -> ".join([f"{node} ({prob})" for node, prob in reversed_chain[:-1]]) + f" (可能性：{probability})\n"
            root_causes.add(reversed_chain[0])

    output += "\nRoot Causes:\n"
    for cause, prob in root_causes:
        output += f"{cause} ({prob})\n"

    return output


if __name__ == "__main__":
    dataset = [['牛奶', '面包'],
               ['牛奶', '饼干'],
               ['面包', '饼干', '牛奶'],
               ['牛奶', '面包', '饼干'],
               ['面包', '苹果']]
    # 最小支持度设为2
    min_support = 2

    # 调用函数进行顺序模式挖掘
    frequent_sequences = mine_sequential_patterns(dataset, min_support)
    graph_data, training_data = generate_graph_and_training_data(frequent_sequences)
    # 数据转换
    graph_df = pd.DataFrame(graph_data)
    train_df = pd.DataFrame(training_data)
    alarm = '饼干'
    results = bayesian_root_cause_analysis(graph_df, train_df, alarm)
    results_dict = results.to_dict()  # 如果 RCAResults 有 to_dict 方法
    info = get_root_cause_info(results_dict)
    print(info)
