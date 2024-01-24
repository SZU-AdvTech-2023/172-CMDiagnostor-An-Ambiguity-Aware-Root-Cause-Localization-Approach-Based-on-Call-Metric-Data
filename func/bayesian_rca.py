import pandas as pd

from func.bayesian_root_cause_analysis import bayesian_root_cause_analysis
from func.sequence_data_processing import generate_graph_and_training_data
from func.sequential_pattern_mining import mine_sequential_patterns
from pyrca.analyzers.bayesian import BayesianNetwork

def train_and_analyze_bayesian_network(causal_relations, time_series_data):
    # 构建因果图的 DataFrame
    graph_data = {'from': [relation[0] for relation in causal_relations],
                  'to': [relation[1] for relation in causal_relations]}
    graph_df = pd.DataFrame(graph_data)

    # 准备时间序列数据
    df = pd.DataFrame(time_series_data)

    # 训练贝叶斯网络模型
    model = BayesianNetwork(config=BayesianNetwork.config_class(graph=graph_df))
    model.train(df)
    model.save("model_folder")

    # 加载模型并进行根本原因分析
    model = BayesianNetwork.load("model_folder")
    # 假设检测到“面包”的异常购买行为
    results = model.find_root_causes(["面包"])
    return results.to_dict()




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
