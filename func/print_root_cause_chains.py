# print_root_cause_chains.py

def print_root_cause_chains(results):
    output_str = ""
    if isinstance(results, dict):
        root_cause_nodes = results.get('root_cause_nodes', [])
        root_cause_paths = results.get('root_cause_paths', {})
    else:
        root_cause_nodes = results.root_cause_nodes
        root_cause_paths = results.root_cause_paths

    # 打印根因节点及其概率
    for root_cause, probability in root_cause_nodes:
        output_str += f"Root Cause: {root_cause} (Probability: {probability})\n"

    # 打印根因链路及其概率
    for root_cause, paths in root_cause_paths.items():
        for path_prob, path in paths:
            cause_chain = " -> ".join([node for node, _ in path])
            output_str += f"Root Cause Chain: {cause_chain} (Probability: {path_prob})\n"

    return output_str



# 用于测试的示例数据
if __name__ == "__main__":
    results = {'root_cause_nodes':
                   [('ROOT_KubernetesPodNotHealthy', 0.612597165989032)], 'root_cause_paths': {
        'ROOT_KubernetesPodNotHealthy': [(0.7755830041958336, [('ROOT_KubernetesPodNotHealthy', 0.612597165989032),
                                                               ('KubernetesPodNotHealthy', 0.614895067335747),
                                                               ('主机离线告警', 1), ('HA失败', 0.8748397834585555)]), (
                                         0.7683552146233311, [('ROOT_KubernetesPodNotHealthy', 0.612597165989032),
                                                              ('KubernetesPodNotHealthy', 0.614895067335747),
                                                              ('主机离线告警', 1),
                                                              ('组件授权信息异常', 0.8459286251685455)]), (
                                         0.7592645168458496, [('ROOT_KubernetesPodNotHealthy', 0.612597165989032),
                                                              ('KubernetesPodNotHealthy', 0.614895067335747),
                                                              ('虚拟机异常关机重启', 0.6939905674459137),
                                                              ('主机离线告警', 1), ('HA失败', 0.8748397834585555)])]}}

    print(type(results))
    print(results)

    print_root_cause_chains(results)
