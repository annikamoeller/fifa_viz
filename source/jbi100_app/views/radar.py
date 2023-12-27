import pandas as pd
from ..config import *
from dash import dcc, html
import plotly.graph_objs as go

class Radar(html.Div):
    def __init__(self, name, player1, player2, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.player1 = player1
        self.player2 = player2


        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=
                dcc.Graph(id=self.html_id),
            style={'margin': 'auto', 'width': '70%','text-align': 'center', 'padding': 20}
        )
    
    def update(self, clickedPlayer=None, hoveredPlayer=None, selected_stat=None):
        """ @clickedPlayer (str) = The clicked player name
            @hoveredPlayer (str) = The hovered player name"""
        
        if selected_stat == 'Goalkeeper': df = goalkeeping_radar_df
        if selected_stat == 'Defender': df = defense_radar_df
        if selected_stat == 'Midfilder': df = midfielder_radar_df
        if selected_stat == 'Striker': df = striker_radar_df

        if clickedPlayer is None and hoveredPlayer is None: return self.clear(df)

        categories = list(df.columns)

        fig = go.Figure()

        if clickedPlayer:
            player_values = df.loc[clickedPlayer].values

            fig.add_trace(go.Scatterpolar(
                r=player_values,
                theta=categories,
                fill='toself',
                name=clickedPlayer
            ))

        if hoveredPlayer:
            player_values = df.loc[hoveredPlayer].values
            fig.add_trace(go.Scatterpolar(
                r=player_values,
                theta=categories,
                fill='toself',
                name=hoveredPlayer
            ))

        fig = self.set_fig_style(fig)

        return fig
    
    def clear(self, df):
        print(df)
        categories = list(df.columns)
        empty_values = []

        for value in categories:
            empty_values.append(0)

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
        fig.update_layout(plot_bgcolor='white',
            paper_bgcolor='#26232C',
            modebar_color = '#136d6d',
            title_font_color='white',
            legend_font_color='white',
            legend_title_font_color='white',
            showlegend=True,
            polar=dict(
                radialaxis=dict(
                visible=True,
                range=[0, 5],
                color="white",
                )))
        
        fig.update_polars(bgcolor="#9D9D9D", angularaxis=dict(color="#9D9D9D"))
        
        return fig