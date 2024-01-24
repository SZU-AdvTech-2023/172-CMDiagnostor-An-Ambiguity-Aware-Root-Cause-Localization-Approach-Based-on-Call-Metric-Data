import pandas as pd

def deduplicate_event_arrays(df_grouped):
    """
    Deduplicates the elements in the 'event' column of the provided DataFrame.

    :param df_grouped: A pandas DataFrame with a column named 'event' containing arrays of strings.
    :return: DataFrame with deduplicated event arrays.
    """
    df_grouped['event'] = df_grouped['event'].apply(lambda x: list(set(x)))
    return df_grouped

# 示例使用，可以根据需要注释掉或删除
# if __name__ == "__main__":
#     data = {
#         'real_time': ['2021-01-01', '2021-01-02'],
#         'event': [['a', 'b', 'a', 'c'], ['b', 'c', 'c', 'd']]
#     }
#     df_grouped = pd.DataFrame(data)
#     deduplicated_df = deduplicate_event_arrays(df_grouped)
#     print(deduplicated_df)
