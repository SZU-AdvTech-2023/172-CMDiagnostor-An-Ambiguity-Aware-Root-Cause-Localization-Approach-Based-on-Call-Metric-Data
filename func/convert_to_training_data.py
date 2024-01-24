# convert_to_training_data.py
import pandas as pd
import random
from datetime import datetime, timedelta


def convert_df_to_training_data(df_grouped):
    all_events = set()
    for events in df_grouped['event']:
        all_events.update(events)

    # 初始化 training_data 字典
    training_data = {event: [0] * len(df_grouped) for event in all_events}

    # 使用行号更新 training_data 中的告警记录
    for row_num, (_, row) in enumerate(df_grouped.iterrows()):
        for event in row['event']:
            if event in training_data:
                training_data[event][row_num] = 1

    return training_data

def generate_random_datetime(start, end):
    """
    Generates a random datetime between 'start' and 'end'.
    """
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

# 示例使用，可以根据需要注释掉或删除
if __name__ == "__main__":
    # df_grouped_example = pd.DataFrame({
    #     'realtime': ['2021-01-01', '2021-01-02', '2021-01-03'],
    #     'event': [['HA失败', 'cpu告警'], ['cpu告警'], ['HA失败']]
    # })
    # training_data_result = convert_df_to_training_data(df_grouped_example)
    # print(training_data_result)

    # 生成一个更大的示例 DataFrame
    num_rows = 100  # 示例数据行数
    start_datetime = datetime(2021, 1, 1)
    end_datetime = datetime(2021, 12, 31)

    df_grouped_example = pd.DataFrame({
        'realtime': [generate_random_datetime(start_datetime, end_datetime).strftime("%Y-%m-%d %H:%M:%S") for _ in range(num_rows)],
        'event': [random.sample(['HA失败', 'cpu告警', '网络延迟', '内存不足', '磁盘故障'], random.randint(1, 3)) for _ in range(num_rows)]
    })

    training_data_result = convert_df_to_training_data(df_grouped_example)
    print(training_data_result)
