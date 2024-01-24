import pandas as pd

def clean_illegal_characters(df):
    """
    清理 DataFrame 中的非法字符。
    """
    clean_df = df.copy()
    for col in clean_df.columns:
        if clean_df[col].dtype == object:
            clean_df[col] = clean_df[col].apply(lambda x: ''.join([i if ord(i) < 128 else ' ' for i in str(x)]))
    return clean_df


