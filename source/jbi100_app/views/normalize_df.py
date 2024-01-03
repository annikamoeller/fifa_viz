def normalize_df(column):
    """Takes column from pandas dataframe, returns the normalized column 
    so that the values lie in [0, 1]."""
    max_val = column.max()
    normalized_column = column / max_val
    return normalized_column
    