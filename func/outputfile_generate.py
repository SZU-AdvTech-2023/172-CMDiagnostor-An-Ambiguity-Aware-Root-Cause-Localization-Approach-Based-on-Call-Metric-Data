import datetime
import json
import os

import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

from func.apriori_res import read_file_streaming, EVENT_MAP_TABLES, array_to_dataframe
from func.check_training_data import is_binary_training_data
from func.convert_to_training_data import convert_df_to_training_data
from func.data_transfer import data_transfer
from func.deduplicate_events import deduplicate_event_arrays
from func.erro_events import remove_erro_events
from func.filter_rules_by_event_sequence import filter_rules
from datetime import datetime, timedelta


def generate_sample_dataframe(min_support, min_confidence):
    """
    根据 min_support 和 min_confidence 值生成示例 DataFrame。
    这里仅为演示，实际应用中应根据这些值生成或处理数据。
    """
    # 生成一些示例数据
    data = {
        'Item': np.random.choice(['A', 'B', 'C', 'D'], size=10),
        'Quantity': np.random.randint(1, 10, size=10),
        'Support': np.full(10, min_support),
        'Confidence': np.full(10, min_confidence)
    }
    return pd.DataFrame(data)


def main():
    min_support_values = [0.1, 0.2, 0.3]  # 示例值
    min_confidence_values = [0.5, 0.6, 0.7]  # 示例值

    for min_support in min_support_values:
        for min_confidence in min_confidence_values:
            # 生成示例 DataFrame
            df = generate_sample_dataframe(min_support, min_confidence)

            # 设置输出文件名
            output_file = f'output_support_{min_support}_confidence_{min_confidence}.xlsx'

            # 创建一个 Excel 写入器
            writer = pd.ExcelWriter(output_file)

            # 将DataFrame写入Excel文件
            df.to_excel(writer, index=False)

            # 保存Excel文件
            writer._save()

            # 输出成功提示
            print(f"min_support={min_support}, min_confidence={min_confidence} 的结果已写入 {output_file} 文件中")


def save_training_data_as_json(training_data, file_name):
    with open(file_name, 'w') as file:
        json.dump(training_data, file)


def output_apriori_res(min_support, min_confidence):
    print(os.getcwd())
    # 读取原始数据
    # 分别读取多个 JSON 文件， 包含历史的告警数据
    data1 = read_file_streaming('../data/all_alarm_1.json')
    data2 = read_file_streaming('../data/all_alarm_2.json')
    data3 = read_file_streaming('../data/all_alarm_3.json')
    data4 = read_file_streaming('../data/old_alarm2.json')
    # 合并数据
    datas = data1 + data2 + data3 + data4
    # 获取JSON文件中的字段数量
    num_data = len(datas)
    print("原始数据的数量：", num_data)

    # 将告警事件的英文转换为中文
    for item in datas:
        # 如果告警数据有title字段，直接设置为告警名称
        if 'title' in item['attributes']:
            item['event'] = item['attributes'].get('title', '')

    # 将告警字段的event全部转成中文
    for item in datas:
        if item['event'] not in EVENT_MAP_TABLES.keys():
            for eve_cn, eve_en in EVENT_MAP_TABLES.items():
                if item['event'] == eve_en:
                    item['event'] = eve_cn

    # 拨测告警单独处理
    for item in datas:
        if item['resource_type'] == "dial_testing":
            item['event'] = "拨测告警"


    # 获取告警字段中我们需要的字段：last_receive_time、event、resource_type
    records = []
    for item in datas:
        timestamp = item.get('last_receive_time', '')
        dt_object = datetime.fromtimestamp(timestamp)
        date_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        if 'title' in item['attributes']:
            record = {
                'last_receive_time': item.get('last_receive_time', ''),
                'real_time': date_string,
                'title': item['attributes'].get('title', ''),
                'event': item['event'],
                'resource_type': item['resource_type']
            }
            records.append(record)
        else:
            record = {
                'last_receive_time': item.get('last_receive_time', ''),
                'real_time': date_string,
                'title': item['event'],
                'event': item['event'],
                'resource_type': item['resource_type']
            }
            records.append(record)

    # 对数据进行去重
    unique_records = list(set(tuple(sorted(record.items())) for record in records))
    unique_records = [dict(record) for record in unique_records]

    # 删掉不符合格式的event
    modified_records = remove_erro_events(unique_records)

    # 打印过滤完的所有event类型
    # print_unique_events(modified_records)

    # 将数据转换为DataFrame格式
    df = pd.DataFrame(modified_records)

    # 将last_receive_time字段转换为时间类型
    df['real_time'] = pd.to_datetime(df['real_time'])

    # 对'real_time'和'event'列进行去重
    df.drop_duplicates(subset=['real_time', 'event'], inplace=True)

    # 对'real_time'列进行升序排序
    df.sort_values(by='real_time', inplace=True)

    df = df[['real_time', 'event']]

    df_time = df
    # 创建空列表
    groups = []

    # 遍历排序后的数据
    for index, row in df.iterrows():
        if not groups:
            # 第一个数据点，创建新组
            groups.append([row])
        else:
            # 获取最后一个组的最后一个数据点的'real_time'
            last_real_time = groups[-1][-1]['real_time']
            current_real_time = row['real_time']
            time_diff = (current_real_time - last_real_time).total_seconds() / 60

            if time_diff <= 10:
                # 时间差不超过10分钟，添加到最后一个组
                groups[-1].append(row)
            else:
                # 时间差超过10分钟，创建新组
                groups.append([row])

    # 把分组后的groups转成df格式
    df_grouped = array_to_dataframe(groups)

    # 给分组后的event去重
    df_grouped = deduplicate_event_arrays(df_grouped)
    # 获取 event 列不为空的行
    mask = df_grouped['event'].apply(len) > 1

    # 根据条件筛选数据
    df_grouped = df_grouped.loc[mask]

    # 打印结果
    # print(df_grouped)

    # 根据df_grouped生成training_data
    training_data = convert_df_to_training_data(df_grouped)
    # 保存training_data
    save_training_data_as_json(training_data, 'training_data.json')
    # 检查training_data是否只有两个状态
    result = is_binary_training_data(training_data)
    transactions = df_grouped['event'].values.tolist()
    # print(transactions)

    # 设置numpy数组的打印选项
    np.set_printoptions(threshold=np.inf)

    # 将事务列表转换成二进制矩阵
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    # print(te_ary)
    # print(df.to_string())

    # 挖掘频繁项集
    # frequent_itemsets = apriori(df, min_support=0.03, use_colnames=True)
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)

    # 挖掘关联规则
    # rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.2)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

    # 过滤规则
    time_threshold = 120  # 2分钟
    rules = filter_rules(rules, df_time, time_threshold)

    # 设置输出文件名
    output_file = f'output_support_{min_support}_confidence_{min_confidence}.xlsx'

    # 创建一个 Excel 写入器
    writer = pd.ExcelWriter(output_file)

    # 将频繁项集写入Excel表的一个工作表
    frequent_itemsets.to_excel(writer, sheet_name='频繁项集', index=False)

    # 将关联规则写入Excel表的另一个工作表
    rules.to_excel(writer, sheet_name='关联规则', index=False)

    # 保存Excel文件
    writer._save()

    # 输出成功提示
    print(f"min_support={min_support}, min_confidence={min_confidence} 的结果已写入 {output_file} 文件中")

    # return rules, training_data
    return rules, training_data


if __name__ == "__main__":
    # 定义要尝试的支持度和置信度阈值范围
    min_supports = [0.02, 0.03, 0.04]
    # min_supports = [0.04, 0.05]
    min_confidences = [0.2, 0.3, 0.4]
    # min_confidences = [0.4, 0.5]

    for min_support in min_supports:
        for min_confidence in min_confidences:
            rules, training_data = output_apriori_res(min_support, min_confidence)