import pandas as pd

# TODO:优化代码，时间太久了
def find_first_close_events(df, event1, event2, time_threshold):
    """
    在DataFrame中找到第一对时间接近的event1和event2，并判断它们的先后顺序。

    :param df: 包含 real_time 和 event 的 DataFrame。
    :param event1: 第一个事件类型。
    :param event2: 第二个事件类型。
    :param time_threshold: 两个事件被视为接近的时间阈值（秒）。
    :return: 如果找到一对事件，并且event2在event1之前，返回True；否则返回False。
    """
    df['real_time'] = pd.to_datetime(df['real_time'])
    event1_times = df[df['event'] == event1]['real_time']
    event2_times = df[df['event'] == event2]['real_time']

    for time1 in event1_times:
        for time2 in event2_times:
            if abs((time2 - time1).total_seconds()) <= time_threshold:
                return time2 < time1
    return False

def filter_rules(rules, df, time_threshold):
    """
    过滤掉在给定时间阈值内event2先于event1发生的规则。

    :param rules: 关联规则的DataFrame。
    :param df: 原始数据的DataFrame。
    :param time_threshold: 时间阈值（秒）。
    :return: 过滤后的规则。
    """
    to_delete = []
    for index, rule in rules.iterrows():
        antecedents = next(iter(rule['antecedents']))
        consequents = next(iter(rule['consequents']))
        if find_first_close_events(df, antecedents, consequents, time_threshold):
            to_delete.append(index)
    return rules.drop(rules.index[to_delete])



if __name__ == "__main__":
    # 示例数据
    data = {
        'real_time': ['2021-01-01 12:00:00', '2021-01-01 12:01:00', '2021-01-01 12:02:00', '2021-01-01 12:03:00'],
        'event': ['主机内存告警', 'KubernetesPodNotHealthy', '主机内存告警', 'KubernetesPodNotHealthy']
    }
    df = pd.DataFrame(data)
    df['real_time'] = pd.to_datetime(df['real_time'])

    # 示例关联规则
    rules_data = {
        'antecedents': [frozenset(['主机内存告警']), frozenset(['KubernetesPodNotHealthy'])],
        'consequents': [frozenset(['KubernetesPodNotHealthy']), frozenset(['主机内存告警'])],
        'support': [0.6, 0.5],
        'confidence': [0.8, 0.7]
    }
    rules = pd.DataFrame(rules_data)

    # 过滤规则
    time_threshold = 120  # 2分钟
    filtered_rules = filter_rules(rules, df, time_threshold)

    print("过滤后的关联规则：")
    print(filtered_rules)
