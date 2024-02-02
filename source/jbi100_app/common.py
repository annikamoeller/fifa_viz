import numpy as np
import os 
from IPython.display import Image
from jbi100_app.config import *
from sklearn.metrics.pairwise import cosine_similarity

""" This file is to store functions used in several places """

def filter_df(df, team_filter, position_filter):
    if team_filter and position_filter:
        df = df[df['team'].isin(team_filter)]
        df = df[df['position'].isin(position_filter)]
    if team_filter and not position_filter:
        df = df[df['team'].isin(team_filter)]
    if position_filter and not team_filter:
        df = df[df['position'].isin(position_filter)]
    return df

def rank_df(df, selected_stat):
    #df['rank'] = df[selected_stat].rank(method = 'dense', ascending=False)
    selected_stat_90s = f"{selected_stat} per 90s"
    try:
        df = df[['player', selected_stat, selected_stat_90s, 'team', 'position']]
    except:
        print("not 90s")
        df = df[['player', selected_stat, 'team', 'position']]
    df = df.sort_values(by=selected_stat, ascending=False)
    return df

def normalize_df(column):
    """Takes column from pandas dataframe, returns the normalized column 
    so that the values lie in [0, 1]."""
    max_val = column.max()
    normalized_column = column / max_val
    return normalized_column

def median_imputation_of_nan(col):
    col_median = np.median(col.dropna())
    return col.fillna(col_median) 

