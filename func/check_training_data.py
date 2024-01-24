def is_binary_training_data(training_data):
    """
    Checks if all values in the training_data dictionary are binary (only 0 or 1)
    and not all zeros or all ones. Prints non-binary entries.

    :param training_data: A dictionary with lists of integers as values.
    :return: True if all lists are binary and not all zeros/ones, False otherwise.
    """
    is_binary = True
    for key, values in training_data.items():
        if not all(val in [0, 1] for val in values):  # Check if all values are 0 or 1
            print(f"Non-binary values found in '{key}': {values}")
            is_binary = False
        elif all(val == 0 for val in values) or all(val == 1 for val in values):  # Check if all values are same
            print(f"Values in '{key}' are all the same: {values}")
            is_binary = False

    return is_binary


if __name__ == "__main__":
    # 示例使用
    training_data = {
        '拨测告警': [1, 1, 1, 1, 1, 0],
        '虚拟机业务卡慢': [1, 1, 1, 1, 1, 0],
        '主机网口主备状态异常告警': [1, 0, 0, 0, 0, 1],
        '网口掉线告警': [0, 1, 0, 0, 0, 1],
        '网口损坏告警': [1, 0, 0, 0, 1, 0],
        '跨主机告警': [0, 1, 1, 1, 0, 0],
        '网口错包告警': [0, 1, 0, 0, 1, 0],
        '网口寄存器状态异常': [0, 1, 0, 0, 0, 0],
        '主机网口丢包告警': [0, 0, 1, 0, 0, 0],
        '主机CPU告警': [0, 0, 1, 0, 0, 0],
        '主机vxlan状态异常': [0, 0, 0, 1, 0, 0],
        '数据通信IP冲突': [0, 0, 0, 1, 0, 0],
        '存储私网异常': [0, 0, 0, 0, 1, 0],
    }
    result = is_binary_training_data(training_data)
    print("Is binary training data:", result)
