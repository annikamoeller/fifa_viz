from dash import dcc, html
import plotly.graph_objects as go
from ..config import *
import plotly.express as px
from dash import dash_table
from ..common import *
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
            print(selected_stat)
            self.selected_stat_90s = f"{selected_stat}/game"
            print(self.selected_stat_90s)
            try:
                df = df[['player', self.selected_stat, self.selected_stat_90s, 'team', 'position']]
            except:
                print("not 90s")
                df = df[['player', self.selected_stat, 'team', 'position']]

            #df['rank'] = df[selected_stat].rank(method = 'dense', ascending=False)
            df = df[['player', 'team', self.selected_stat, self.selected_stat_90s, 'position']]
            df = df.sort_values(by=selected_stat, ascending=False)

            # Main table
            super().__init__(
                className="graph_card",
                children=
                    dash_table.DataTable(
                                    id=self.html_id,
                                    columns=[{'name': col, 'id': col} for col in df.columns],
                                    page_current=0,
                                    page_size=20,
                                    data=df.to_dict('records'),
                                    sort_action = 'native',
                                    fixed_rows = {'headers': True},
                                    style_table={'height': '450px', 'color': '#ebebeb'},
                                    style_header={'backgroundColor': 'darkgrey', 'fontWeight': 'bold', 'fontSize': '14px', 'font-family': 'Arial'},
                                    style_cell = {'backgroundColor': '#ebebeb', 'border-color': '1px blue', 'font-family': 'Arial'},
                                    #style_cell={'minWidth': 100, 'width': 100, 'maxWidth': 100, 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                                    style_data={'color': '#26232C'},
                                    style_cell_conditional=[
                                    {'if': {'column_id': 'player'}, 'width': '30%'},
                                    {'if': {'column_id': self.selected_stat}, 'width': '20%'},
                                    {'if': {'column_id': 'team'}, 'width': '15%'},
                                    {'if': {'column_id': 'position'}, 'width': '12.5%'}, 
                                    {'if': {'column_id': self.selected_stat_90s}, 'width': '12.5%'}]
                                    ),
                style={'margin': 'auto', 'width': '100%', 'padding': 10}
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
            df = main_gk_df
        else: df = table_df
            
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
        if on: df = radar_gk_df
        else: df = radar_df

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

        # similar_player_data = similar_player_df.to_dict('records')
        # columns=[{'name': col, 'id': col} for col in similar_player_df.columns]

        # return similar_player_data, columns
        
    def set_clicked_cell(self, clicked_cell):
        self.clicked_cell = clicked_cell

    def get_clicked_cell(self):
        return self.clicked_cell