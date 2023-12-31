from dash import dcc, html
import plotly.graph_objects as go
from ..config import *
import plotly.express as px
from dash import dash_table
from ..common import *

class Table(html.Div):
    def __init__(self, name, df, selected_stat):
        """
        @name (str): used for the html_id
        @df (df): main dataframe to be used
        @selected_stat (str): the statistic to be displayed
        """
        self.html_id = name.lower().replace(" ", "-")
        df = df.reset_index()
        self.selected_stat = selected_stat
        df = rank_df(df, selected_stat)

        self.clickPlayer = None

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=
                dash_table.DataTable(
                                id=self.html_id,
                                columns=[{'name': col, 'id': col} for col in df.columns],
                                data=df.to_dict('records'),
                                style_table={'height': '500px', 'overflowY': 'scroll'},
                                style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
                                #style_cell={'minWidth': 100, 'width': 100, 'maxWidth': 100, 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                                style_data={'color': 'black'},
                                style_cell_conditional=[
                                {'if': {'column_id': 'player'}, 'width': '50%'},
                                {'if': {'column_id': self.selected_stat}, 'width': '20%'},
                                {'if': {'column_id': 'team'}, 'width': '30%'},
                                ]
                                ),
            style={'margin': 'auto', 'width': '100%', 'padding': 10}
            )
    
    def update(self, selected_stat, team_filter=None, position_filter=None):
        """
        @selected_stat (str): statistic to display selected by user
        @team_filter (str): team(s) to filter by
        @position_filter (str): position(s) to filter by
        @returns ->>> updated data and columns for table
        """
        df = main_df
        df = df.reset_index()
        df = filter_df(df, team_filter, position_filter)
        df = rank_df(df, selected_stat)

        columns=[{'name': col, 'id': col} for col in df.columns]
        data=df.to_dict('records')
        
        print(columns)
        return data, columns

    #Not needed or used for now
    def get_click_player(self):
        return self.clickPlayer
    
    #Not needed or used for now
    def set_click_player(self, clickedPlayer):
        self.clickPlayer = clickedPlayer