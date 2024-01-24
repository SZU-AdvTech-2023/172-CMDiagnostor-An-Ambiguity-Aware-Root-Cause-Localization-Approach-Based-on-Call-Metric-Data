# filename: print_unique_events.py

def print_unique_events(records):
    """
    Prints all unique events from a list of records.

    :param records: A list of dictionaries, where each dictionary contains an 'event' field.
    """
    unique_events = set()
    for record in records:
        if 'event' in record:
            unique_events.add(record['event'])

    for event in unique_events:
        print(event)


if __name__ == "__main__":
    # 示例用法
    modified_records = [{'event': 'event1'}, {'event': 'event2'}, {'event': 'event1'}]
    print_unique_events(modified_records)
