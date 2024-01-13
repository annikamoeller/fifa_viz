import pandas as pd
from ..config import *
from dash import dcc, html
import plotly.graph_objs as go

class Radar(html.Div):
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
            style={'margin': 'auto', 'width': '70%', 'text-align': 'center', 'padding': 20}
        )
    
    def update(self, on, clickedPlayer=None, hoveredPlayer=None):
        """ 
        @clickedPlayer (str) = The clicked player name
        @hoveredPlayer (str) = The hovered player name
        """
        if on: df = gk_df
        else: df = self.df

        #If nothing is clicked or hovered create an empty radar
        if clickedPlayer is None and hoveredPlayer is None: return self.clear(df)

        categories = list(df.columns)

        fig = go.Figure()

        if clickedPlayer:
            player_values = df.loc[clickedPlayer].values

            fig.add_trace(go.Scatterpolar(
                r=player_values, #array of values for each label
                theta=categories, #array of labels
                fill='toself',
                name=clickedPlayer
            ))

        if hoveredPlayer:
            player_values = df.loc[hoveredPlayer].values
            fig.add_trace(go.Scatterpolar(
                r=player_values, #array of values for each label
                theta=categories, #array of labels
                fill='toself',
                name=hoveredPlayer
            ))

        #Set the color scheme for the plot
        fig = self.set_fig_style(fig)

        return fig
    
    def clear(self, df):
        """
        Instantiates a radar with empty values
        @df (pandas dataframe): trimmed dataframe (gkdf, defndf, midfdf, strdf) used to get the categories for the radar
        """
        categories = list(df.columns)

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=[0 for value in categories],
            theta=categories,
            fill='toself',
            name=''
        ))

        fig = self.set_fig_style(fig)

        return fig
    
    def set_fig_style(self, fig):
        """
        Updates a figures style
        @fig (figure): a graph figure to be updated
        """

        #add legend range for the radar axis and background colors
        fig.update_layout(plot_bgcolor='white',
            paper_bgcolor='#26232C',
            modebar_color = '#136d6d',
            showlegend=True,
            polar=dict(
                radialaxis=dict(
                visible=True,
                range=[0, 5],
                color="white",
                )))
        
        #update the radar colors
        fig.update_polars(bgcolor="#9D9D9D", angularaxis=dict(color="#9D9D9D"))
        
        return fig