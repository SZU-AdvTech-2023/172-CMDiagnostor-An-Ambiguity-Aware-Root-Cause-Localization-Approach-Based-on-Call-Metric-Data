import json

import pandas as pd

from func.bayesian_root_cause_analysis import bayesian_root_cause_analysis
from func.cycle_modify import cycle_modify
# from func.data_transfer import data_transfer
from func.result_to_print import get_root_cause_info

import ast

def convert_string_to_frozenset(frozenset_str):
    # Remove the "frozenset" part of the string
    content = frozenset_str.strip("frozenset()")
    # Convert the string to a literal tuple using ast.literal_eval
    content_tuple = ast.literal_eval(content)
    # Convert the tuple to a frozenset
    return frozenset(content_tuple)

def read_rules_from_excel(min_support, min_confidence):
    """
    从指定的 Excel 文件中读取 '关联规则' 工作表。

    :param min_support: 最小支持度
    :param min_confidence: 最小置信度
    :return: 从 Excel 文件读取的 '关联规则' DataFrame
    """
    # 根据 min_support 和 min_confidence 值构建文件名
    output_file = f'output_support_{min_support}_confidence_{min_confidence}.xlsx'

    try:
        # 读取 '关联规则' 工作表
        rules = pd.read_excel(output_file, sheet_name='关联规则')
        return rules
        # rules_df = pd.read_excel(output_file, sheet_name='关联规则')
        # rules_df['antecedents'] = rules_df['antecedents'].apply(lambda x: frozenset(x.split(', ')))
        # rules_df['consequents'] = rules_df['consequents'].apply(lambda x: frozenset(x.split(', ')))
        # return rules_df
    except FileNotFoundError:
        print(f"文件 {output_file} 未找到。")
        return None
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None


def load_training_data_from_json(file_name):
    with open(file_name, 'r') as file:
        training_data = json.load(file)
    return training_data


def data_transfer(rules):
    data = {'source': [], 'target': []}
    for index, row in rules.iterrows():
        antecedents = convert_string_to_frozenset(row['antecedents'])
        consequents = convert_string_to_frozenset(row['consequents'])

        for antecedent in antecedents:
            for consequent in consequents:
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

if __name__ == "__main__":
    # 示例 min_support 和 min_confidence 值
    min_supports = [0.02, 0.03, 0.04]
    # min_support = 0.02  # 示例值
    # min_confidence = 0.3  # 示例值
    min_confidences = [0.2, 0.3, 0.4]

    output_array = ""
    for min_support in min_supports:
        for min_confidence in min_confidences:
            # 读取规则
            rules = read_rules_from_excel(min_support, min_confidence)

            # 如果读取成功
            if rules is not None:
                print("rules读取成功")

            file_name = 'training_data.json'
            training_data = load_training_data_from_json(file_name)

            # 如果读取成功
            if training_data is not None:
                print("training_data读取成功")

            # 数据转换
            graph_df = data_transfer(rules)
            train_df = pd.DataFrame(training_data)

            alarms = ['主机配置内存告警', '虚拟机内存告警', '网口掉线告警', '存储掉线告警', '虚拟机异常关机重启',
                      'KubernetesPodNotHealthy']
            for alarm in alarms:
                a = f"Alarm: {alarm}\n"
                output_array += a
                # 贝叶斯算法
                results = bayesian_root_cause_analysis(graph_df, train_df, alarm)
                # 提取并打印根因链
                s = f"Trying min_support = {min_support}, min_confidence = {min_confidence}\n"
                results_dict = results.to_dict()  # 如果 RCAResults 有 to_dict 方法
                info = get_root_cause_info(results_dict)
                new_output_str = s + info
                output_array += new_output_str

    print(output_array)
