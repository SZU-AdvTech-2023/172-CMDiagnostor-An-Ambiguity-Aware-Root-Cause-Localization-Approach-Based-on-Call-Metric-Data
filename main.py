import pandas as pd

from func.apriori_res import apriori_res
from func.bayesian_root_cause_analysis import bayesian_root_cause_analysis
from func.data_transfer import data_transfer
from func.print_root_cause_chains import print_root_cause_chains
from func.result_to_print import get_root_cause_info

if __name__ == '__main__':
    # 1、 先用apriori算法对数据进行关联规则挖掘
    # 2、 再用贝叶斯算法构图
    # 3、 最后根据生成的告警树来寻找根因

    output_array = ""   # 输出结果

    # 关联规则挖掘算法，rules：关联规则的结果
    min_supports = 0.03
    min_confidences = 0.3
    rules, training_data = apriori_res(min_supports, min_confidences)

    # 数据转换
    graph_df = data_transfer(rules)
    train_df = pd.DataFrame(training_data)

    # alarm设置为你要查询的告警名
    alarm = "主机配置内存告警"

    a = f"Alarm: {alarm}\n"
    output_array += a   # 输出告警名称
    # 贝叶斯算法
    results = bayesian_root_cause_analysis(graph_df, train_df, alarm)
    # 提取并打印根因链
    s = f"Trying min_support = 0.02, min_confidence = 0.2\n"
    results_dict = results.to_dict()  # 如果 RCAResults 有 to_dict 方法
    info = get_root_cause_info(results_dict)
    new_output_str = s + info
    output_array += new_output_str
    print(output_array)