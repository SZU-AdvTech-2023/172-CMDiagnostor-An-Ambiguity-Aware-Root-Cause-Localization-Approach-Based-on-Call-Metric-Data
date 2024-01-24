import pandas as pd

# from data_test import data_output
from pyrca.analyzers.bayesian import BayesianNetworkConfig, BayesianNetwork


def bayesian_root_cause_analysis(graph_df, train_df, alarm):
    # 3. 配置和初始化模型
    config = BayesianNetworkConfig(graph=graph_df)
    model = BayesianNetwork(config)

    # 4. 使用时间序列数据训练模型
    model.train(train_df)

    # 5. 使用模型查找根因
    anomalous_metrics = [alarm]
    # anomalous_metrics = ['Metric_B']
    results = model.find_root_causes(anomalous_metrics)

    # 6. 打印结果
    print(results.to_dict())

    print("end")

    return results
