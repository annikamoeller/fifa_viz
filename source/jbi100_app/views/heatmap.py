import pandas as pd
from ..config import *
from dash import dcc, html
import plotly.graph_objs as go
import plotly.express as px

class Heatmap(html.Div):
    def __init__(self, name, df):
        """
        @name (str): used for the html_id
        @df (df): main dataframe to be used
        """
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=
                dcc.Graph(id=self.html_id),
            style={'margin': 'auto', 'width': '70%','text-align': 'center', 'padding': 20}
        )
    

    def update(self, player_names=None, selected_attribute=None, selected_stat=None):
        """ 
        @selected_player List(str): Names of selected players.
        @selected_attribute List(str): Attributes selected form dropdown.
        """

        if selected_stat == 'Goalkeeper': df = goalkeeping_radar_df
        if selected_stat == 'Defender': df = defense_radar_df
        if selected_stat == 'Midfilder': df = midfielder_radar_df
        if selected_stat == 'Striker': df = striker_radar_df
        # fig = go.Figure()
        # fig.add_trace(go.Heatmap(
        #     z=[[1, 20, 30],
        #        [20, 1, 60],
        #        [30, 60, 1]]))
        
        df_test = df.loc[player_names, selected_attribute]

        # fig = go.Figure()
        # fig.add_trace(go.Heatmap(
        #     z=df_test.values,
        #     x=df_test.columns.tolist(),
        #     y=df_test.index,
        #     colorscale='Viridis'))

        fig = go.Figure()
        fig.add_trace(go.Heatmap(
            z=df_test,
            x=df_test.columns.tolist(),
            y=df_test.index,
            colorscale='Viridis'))

        # #Set the color scheme for the plot
        # fig = self.set_fig_style(fig)

        return fig