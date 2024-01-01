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
            style={'margin': 'auto', 'width': '90%','text-align': 'center', 'padding': 10}
        )
    
    def update(self, selected_player, similar_players_df):
        """ 
        @similar_players_df List(str): dataframe from get_similar_players in table.py
        """
        # Create the plot layout

        fig = go.Figure()
        fig.add_trace(go.Heatmap(
            z=similar_players_df,
            x=similar_players_df.columns,
            y=similar_players_df.index,
            colorscale='Viridis'))
        
        #Update the style and colors of the graph
        fig.update_layout(plot_bgcolor='#26232C',
            paper_bgcolor='#26232C',
            modebar_color = '#136d6d',
            title_font_color='white',
            legend_font_color='white',
            legend_title_font_color='white',
            xaxis = dict(
            color="#9D9D9D",
            tickfont_size=14,
            title_font=dict(size=20, color='#9D9D9D')),
            yaxis=dict(
                color="#9D9D9D",
                titlefont_size=16,
                tickfont_size=14,
                gridcolor='#9D9D9D',
                title_font=dict(size=17, color='#9D9D9D'),
            ))
        return fig