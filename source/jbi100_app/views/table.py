from dash import dcc, html
import plotly.graph_objects as go
from ..config import *
import plotly.express as px
from dash import dash_table
from ..common import *

from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Table(html.Div):
    def __init__(self, name, df, selected_stat):
        """
        @name (str): used for the html_id
        @df (df): main dataframe to be used
        @selected_stat (str): stat that the df is sorted by
        """

        self.html_id = name.lower().replace(" ", "-")
        self.clicked_cell = None

        if df is not None:
            df = df.reset_index()
            self.selected_stat = selected_stat
            df = df[['player', self.selected_stat, 'team', 'position']]
            df['rank'] = df[selected_stat].rank(method = 'dense', ascending=False)
            df = df[['rank', 'player', 'team', selected_stat, 'position']]
            df = df.sort_values(by=selected_stat, ascending=False)

            # Main table
            super().__init__(
                className="graph_card",
                children=
                    dash_table.DataTable(
                                    id=self.html_id,
                                    columns=[{'name': col, 'id': col} for col in df.columns],
                                    data=df.to_dict('records'),
                                    fixed_rows = {'headers': True},
                                    style_table={'height': '450px', 'overflowY': 'scroll', 'color': '#ebebeb'},
                                    style_header={'backgroundColor': 'darkgrey', 'fontWeight': 'bold', 'fontSize': '14px', 'font-family': 'Arial'},
                                    style_cell = {'backgroundColor': '#ebebeb', 'border-color': '1px blue', 'font-family': 'Arial'},
                                    #style_cell={'minWidth': 100, 'width': 100, 'maxWidth': 100, 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                                    style_data={'color': '#26232C'},
                                    style_cell_conditional=[
                                    {'if': {'column_id': 'player'}, 'width': '40%'},
                                    {'if': {'column_id': self.selected_stat}, 'width': '30%'},
                                    {'if': {'column_id': 'team'}, 'width': '30%'},
            ]
                                    ),
                style={'margin': 'auto', 'width': '100%', 'padding': 10}
            )

        else:
            # Just an empty table for now.
            super().__init__(
                className="graph_card",
                children=[
                    dash_table.DataTable(
                                    id=self.html_id,
                                    columns=[],
                                    style_table={'overflowY': 'scroll'},
                                    style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
                                    #style_cell={'minWidth': 100, 'width': 100, 'maxWidth': 100, 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                                    style_data={'color': 'black'}
                                    )],
                style={'margin': 'auto', 'width': '80%', 'padding': 10}
            )
    
    def update(self, selected_stat, on, team_filter=None, position_filter=None):
        """
        @selected_stat (str): statistic to display selected by user
        @team_filter (str): team(s) to filter by
        @position_filter (str): position(s) to filter by
        @returns ->>> updated data and columns for table
        """
        if on: 
            position_filter = ['GK']
            df = gk_df
        else: df = main_df
            
        df = df.reset_index()
        df = filter_df(df, team_filter, position_filter)
        df = rank_df(df, selected_stat)

        columns=[{'name': col, 'id': col} for col in df.columns]
        data=df.to_dict('records')
        
        return data, columns

    def get_5_similar_players_df(self):
        return self.similar_players_df

    def get_similar_players(self, on, player, num_similar_players=5):
        """
        @player (str): the player for which we want similar players
        @num_similar_players (str): the number of players that we want returned
        @returns ->>> similar player data and columns for table
        """
        if on: df = gk_df
        else: df = main_df

        cleanup_pos = {"position": {"GK": 1, "DF": 2, "MF": 3, "FW": 4}}
        df = df.replace(cleanup_pos)
        df = df.drop(columns='team')
        if not on:
            df = df.drop(columns='birth_year')

        player = df.loc[player].values
        player = player.reshape(1, -1)
        df = df.dropna()
 
        result = cosine_similarity(player, df)

        result = np.array(result)
        result = result.round(8)
        x = np.argsort(result[0])[::-1][1:num_similar_players+1]
        similar_player_df = df.iloc[x]
        self.similar_players_df = similar_player_df
        similar_player_df = similar_player_df.reset_index()

        similar_player_data = similar_player_df.to_dict('records')
        columns=[{'name': col, 'id': col} for col in similar_player_df.columns]

        return similar_player_data, columns
    
    def set_clicked_cell(self, clicked_cell):
        self.clicked_cell = clicked_cell

    def get_clicked_cell(self):
        return self.clicked_cell