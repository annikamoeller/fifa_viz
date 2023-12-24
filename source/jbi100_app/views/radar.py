import pandas as pd
from ..config import *
from dash import dcc, html
import plotly.graph_objs as go

class radar(html.Div):
    def __init__(self, name, player1, player2, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.player1 = player1
        self.player2 = player2

        categories = ['processing cost','mechanical properties','chemical stability',
                    'thermal stability']

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=[1, 5, 2, 2],
            theta=categories,
            fill='toself',
            name='Product A'
        ))
        fig.add_trace(go.Scatterpolar(
            r=[4, 3, 2.5, 1],
            theta=categories,
            fill='toself',
            name='Product B'
        ))

        fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5]
            )),
        showlegend=False
        )

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="radar",
            children=
                dcc.Graph(figure=fig, id=self.html_id),
        )
    
    def update(self, clickedPlayer=None, hoveredPlayer=None):
        """ @clickedPlayer (str) = The clicked player name
            @hoveredPlayer (str) = The hovered player name"""
        categories = ['processing cost','mechanical properties','chemical stability',
                    'thermal stability']

        fig = go.Figure()

        if clickedPlayer:
            fig.add_trace(go.Scatterpolar(
                r=[1, 5, 2, 2],
                theta=categories,
                fill='toself',
                name=clickedPlayer
            ))

        if hoveredPlayer:
            fig.add_trace(go.Scatterpolar(
                r=[4, 3, 2.5, 1],
                theta=categories,
                fill='toself',
                name=hoveredPlayer
            ))
        
        fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5]
            )),
        showlegend=True
        )
    
        return fig
    
    def clear(self):
        categories = ['processing cost','mechanical properties','chemical stability',
                    'thermal stability']

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=[1, 5, 2, 2],
            theta=categories,
            fill='toself',
            name='empty'
        ))

        fig.add_trace(go.Scatterpolar(
            r=[4, 3, 2.5, 1],
            theta=categories,
            fill='toself',
            name='empty'
        ))

        fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5]
            )),
        showlegend=True
        )
    
        return fig