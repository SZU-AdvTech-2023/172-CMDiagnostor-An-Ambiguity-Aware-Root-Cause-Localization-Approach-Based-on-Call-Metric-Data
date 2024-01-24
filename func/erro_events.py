# filter_events.py
import re

def remove_erro_events(unique_records):
    """
    Removes and prints events from the given records if they contain alphanumeric characters and hyphens simultaneously.
    Returns the modified list without these specific events.

    :param unique_records: A list of dictionaries with an 'event' field.
    :return: Modified list of records with specific events removed.
    """
    # 正则表达式匹配包含数字、英文字符和短横线的字符串
    pattern = re.compile(r'^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*-)[a-zA-Z0-9-]+$')

    # 新列表用于存储不满足条件的记录
    remaining_records = []

    # 遍历数组并检查每个字典的 event 字段
    for record in unique_records:
        event = record.get("event", "")
        if not pattern.match(event):
            remaining_records.append(record)

    return remaining_records

# # 示例使用，可以根据需要注释掉或删除
# if __name__ == "__main__":
#     unique_records = [
#         {"event": "e388dd68-2854-4885-a734-4010744131cb"},
#         {"event": "事件456"},
#         {"event": "event789"},
#         {"event": "123-测试"},
#         {"event": "test-event"},
#     ]
#     modified_records = remove_erro_events(unique_records)
#     print("Remaining records:", modified_records)
