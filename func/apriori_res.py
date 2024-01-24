import datetime
import json
import os

import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from datetime import datetime, timedelta
import ijson
import chardet

from func.check_training_data import is_binary_training_data
from func.clean_illegal_characters import clean_illegal_characters
from func.convert_to_training_data import convert_df_to_training_data
from func.deduplicate_events import deduplicate_event_arrays
from func.erro_events import remove_erro_events
from func.filter_rules_by_event_sequence import filter_rules
from func.print_unique_events import print_unique_events

EVENT_MAP_TABLES = {
    # "网口接管失败告警": "网口接管失败告警",
    # "iface_takeover_fail": "接管网口失败",
    # "vm_net_conn": "虚拟机网络不通",
    # "vm_paused_io_error": "虚拟机异常挂起",
    # "vm_abnormal_shutdown": "虚拟机异常关机重启",
    # "vnetdev_net_conn": "虚拟网络设备与外部网络不通",
    # "vnetdev_fault": "虚拟网络设备无响应",
    # "vnetdev_internal": "虚拟网络设备内部告警",
    # "vrouter_run": "路由器运行失败告警",
    # "vr_ha": "虚拟路由器告警",
    # "iface_fault": "网口故障告警",
    # "stp_enable": "交换机STP启用告警",
    # "iface_error": "网口异常告警",
    # "host_offline": "主机离线告警",
    # "host_iface_abnormal_traffic": "服务器网卡流量异常",
    # "nic_transceiver": "网卡光模块异常告警",
    # "nic_removed": "物理网卡被移除",
    # "host_iface_config": "主机网口与对端设备网口配置不匹配",
    # "controller_offline": "控制节点离线告警",
    # "vnet_status": "虚拟网络服务状态异常告警",
    # "host_mgmt_service_status_abnormal": "主机管理服务状态异常",
    # "cfg_failure": "网络配置下发失败",
    # "iface_update_fdb_fail": "更新网卡FDB失败",
    # "host_logical_iface_abnormal": "逻辑口状态异常",
    # "host_iface_in_bandwidth_overload": "网口入口带宽利用率过高",
    # "host_iface_out_bandwidth_overload": "网口出口带宽利用率过高",
    # "虚拟网络性能异常": "虚拟网络性能异常",
    # "逻辑口状态异常": "逻辑口状态异常",
    # "网口异常告警": "iface_error",
    # "物理网卡被移除": "nic_removed",
    # "网卡光模块异常告警": "nic_transceiver",
    # "网口出带宽利用率过高": "网口出带宽利用率过高",
    # "网口入带宽利用率过高": "网口入带宽利用率过高",
    # "主机网口与对端设备网口配置不匹配": "host_iface_config",
    # "虚拟机业务中断": "虚拟机业务中断",
    # "主机离线告警": "host_offline",
    # "虚拟机网络不通": "vm_net_conn",
    # "虚拟机异常关机重启": "vm_abnormal_shutdown",
    # "主机网关不通告警": "host_gateway_unreachable",
    # "虚拟机无响应": "vm_fault",
    # "虚拟网络设备无响应": "vnetdev_fault",
    "虚拟网口丢包告警": "vm_iface_lost_rate",
    "虚拟机单网口连接session数告警": "session_num",
    "虚拟网络设备CPU使用告警": "vnetdev_cpu",
    "虚拟网络设备ALG使用过高": "vnet_alg_high",
    "数据通信口(vxlan)告警": "host_vxlan",
    "数据通信口(vxlan)提醒": "host_vxlan_hyperframe",
    "管理通信口发包超限告警": "mgmt_qos_rate_out",
    "存储私网异常": "vs_private_nic",
    "网卡驱动兼容告警": "nic_driver_firmware",
    "网口损坏告警": "host_netcard",
    "主机网口降速告警": "auto_negotiation_rate",
    "主机网关不通告警": "host_gateway_unreachable",
    "网口掉线告警": "iface_down",
    "主机网口丢包告警": "host_iface_lost_rate",
    "主机网卡工作异常": "host_nic",
    "主机聚合口告警": "host_bond",
    "网口错包告警": "err_packet",
    "数据面抓包口存在异常流量": "pcapif_traffic_abnormal",
    "数据面转发性能不足": "dp_high_performance_bottleneck",
    "主机网口主备状态异常告警": "host_iface_switch_abnormal_alarms",
    "跨主机网口高时延异常告警": "CrossHost_iface_high_latency_abnormal_alarms",
    "跨主机网口时延抖动异常告警": "CrossHost_iface_high_jitter_abnormal_alarms",
    "跨主机网口中断异常告警": "CrossHost_iface_abnormal_interruption_abnormal_alarms",
    "虚拟机业务卡慢": "虚拟机业务卡慢",
    "虚拟网口丢包告警": "vm_iface_lost_rate",
    "数据面转发性能不足": "数据面转发性能不足",
    "数据面会话使用率过高": "数据面会话使用率过高",
    "虚拟机单网口连接session数告警": "session_num",
    "数据面抓包口存在异常流量": "pcapif_traffic_abnormal",
    "虚拟设备性能不足": "虚拟设备性能不足",
    "虚拟网络设备CPU使用告警": "vnetdev_cpu",
    "虚拟机非最佳性能配置": "虚拟机非最佳性能配置",
    "网口错包告警": "err_packet",
    "主机聚合口告警": "host_bond",
    "网卡寄存器状态异常": "网卡寄存器状态异常",
    "网口损坏告警": "host_netcard",
    "主机网卡工作异常": "host_nic",
    "主机网卡流量异常": "主机网卡流量异常",
    "主机CPU告警": "host_cpu",
    "主机vxlan状态异常": "主机vxlan状态异常",
    "网口掉线告警": "iface_down",
    "网卡驱动兼容告警": "nic_driver_firmware",
    "主机网口丢包告警": "host_iface_lost_rate",
    "主机网口降速告警": "auto_negotiation_rate",
    "管理通信口发包超限告警": "mgmt_qos_rate_out",
    "虚拟网络设备ALG使用过高": "虚拟网络设备ALG使用过高",
    "数据通信口(vxlan)告警": "host_vxlan",
    "数据通信口(vxlan)提醒": "host_vxlan_hyperframe",
    "数据通信IP冲突": "vxlan_ip_conflict",
    "存储私网异常": "vs_private_nic",
    "拨测告警": "dial_testing",
    "主机网口主备状态异常告警": "主机网口主备状态异常告警",
    "跨主机网口高时延异常告警": "CrossHost_iface_high_latency_abnormal_alarms",
    "网卡光模块状态异常告警": "网卡光模块状态异常告警",
    "网口带宽利用率过高": "网口带宽利用率过高",
    "跨主机网口中断异常告警": "跨主机网口中断异常告警",
    "跨主机网口时延抖动异常告警": "CrossHost_iface_high_jitter_abnormal_alarms"
}


def read_file():
    # 检测JSON文件编码
    with open('../data/all_alarm_1.json', 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']

    # 使用正确的编码方式打开JSON文件
    with open('../data/all_alarm_1.json', 'r', encoding=encoding) as f:
        datas = json.load(f)
    return datas


def read_large_json_file(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as f:
        for line in f:
            try:
                data = json.loads(line)
                yield data  # 使用生成器逐行返回解析的数据
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")


def read_file_streaming(filename):
    datas = []
    # 使用正确的编码方式打开JSON文件进行流式读取
    with open(filename, 'rb') as f:
        # ijson会逐条解析JSON对象，而不是一次性加载整个文件
        objects = ijson.items(f, 'item')
        for obj in objects:
            datas.append(obj)
    return datas


def get_alarm_name():
    alarm_name = []
    for key, value in EVENT_MAP_TABLES.items():
        alarm_name.append(key)
        alarm_name.append(value)
    print(alarm_name)
    return alarm_name


def check_global_alarm(data, alarm_name):
    for key, value in data.items():
        if isinstance(value, dict):
            if check_global_alarm(value, alarm_name):
                return True
        elif isinstance(value, str) and value in alarm_name:
            return True
    return False


def array_to_dataframe(groups):
    # 打印groups
    for group in groups:
        events = []  # 存储组中所有数据点的event值
        for data_point in group:
            events.append(data_point['event'])
        event_str = ', '.join(events)  # 将所有event值连接成一个字符串
        # print(f"real_time: {group[0]['real_time']}, events: {event_str}")
        # print('-----------------------------------------------')  # 打印分隔线，区分不同组的数据

    # 创建空列表
    data = []

    # 遍历groups列表
    for group in groups:
        # 获取组中第一个数据点的'real_time'，添加到data列表中作为第一行数据
        real_time = group[0]['real_time']

        # 获取组中所有数据点的'event'，添加到data列表中作为第二行数据
        events = [data_point['event'] for data_point in group]
        data.append([real_time, events])

    # 将data列表转换为DataFrame
    df = pd.DataFrame(data, columns=['real_time', 'event'])
    return df


def apriori_res(min_support, min_confidence):
    print(os.getcwd())
    # 读取原始数据
    # 分别读取多个 JSON 文件， 包含历史的告警数据
    data1 = read_file_streaming('data/all_alarm_1.json')
    data2 = read_file_streaming('data/all_alarm_2.json')
    data3 = read_file_streaming('data/all_alarm_3.json')
    data4 = read_file_streaming('data/old_alarm2.json')
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

    # # 获取过滤的字段
    # alarm_name = get_alarm_name()
    # # print(alarm_name)
    #
    # # 过滤数据
    # new_datas = []
    # for data in datas:
    #     if check_global_alarm(data, alarm_name):
    #         new_datas.append(data)
    #
    # num_new_datas = len(new_datas)
    # print("新数据的数量：", num_new_datas)

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
    # time_threshold = 120  # 2分钟
    # rules = filter_rules(rules, df_time, time_threshold)

    # 设置文件路径
    output_file = 'output.xlsx'

    # 创建一个 Excel 写入器
    writer = pd.ExcelWriter(output_file)

    # 将频繁项集写入Excel表的一个工作表
    frequent_itemsets.to_excel(writer, sheet_name='频繁项集', index=False)

    # 将关联规则写入Excel表的另一个工作表
    # rules.to_excel(writer, sheet_name='关联规则', index=False)
    rules.to_excel(writer, sheet_name='关联规则', index=False)

    # 保存Excel文件
    writer._save()

    # 输出成功提示
    print("输出结果已写入output.xlsx文件中")

    # return rules, training_data
    return rules, training_data


if __name__ == '__main__':
    rules, training_data = apriori_res(0.02, 0.2)
