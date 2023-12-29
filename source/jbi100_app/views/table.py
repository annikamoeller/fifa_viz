from dash import dcc, html
import plotly.graph_objects as go
from ..config import *
import plotly.express as px
from dash import dash_table

class Table(html.Div):
    def __init__(self, name, df, selected_stat):
        """
        @name (str): used for the html_id
        @feature_x (str): x-axis value that matches df column
        @feature_y (str): y-axis value that matches df column
        @df (df): main dataframe to be used
        """
        self.html_id = name.lower().replace(" ", "-")
        df = df.reset_index()
        df = df[['player', selected_stat, 'team']]
        self.clickPlayer = None

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=
                dash_table.DataTable(
                                id=self.html_id,
                                columns=[{'name': col, 'id': col} for col in df.columns],
                                data=df.to_dict('records'),
                                style_table={'height': '300px', 'overflowY': 'scroll'},
                                style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
                                style_cell={'minWidth': 100, 'width': 100, 'maxWidth': 100, 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                                style_data={'color': 'black'}
                                ),
            style={'margin': 'auto', 'width': '100%', 'padding': 10}
        )
    
    def update(self, selected_stat, team_filter=None, position_filter=None):
        """
        @team (str): the team for the scatter plot
        @returns ->>> figure class with new plot
        """
        df = main_df
        df = df.reset_index()
        if team_filter and position_filter:
            df = df[df['team']==team_filter]
            df = df[df['position']==position_filter]
        if team_filter and not position_filter:
            df = df[df['team']==team_filter]
        if position_filter and not team_filter:
            df = df[df['position']==position_filter]
        df = df[['player', selected_stat, 'team']]

        columns=[{'name': col, 'id': col} for col in df.columns] 
        data=df.to_dict('records'),
        return data, columns

    #Not needed or used for now
    def get_click_player(self):
        return self.clickPlayer
    
    #Not needed or used for now
    def set_click_player(self, clickedPlayer):
        self.clickPlayer = clickedPlayer