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
    
    def normalize_using_max(self, column):
        max_val = column.max()
        normalized_column = column / max_val
        return normalized_column

    def update(self, selected_player, similar_players_df, local_normalization):
        """ 
        @similar_players_df List(str): dataframe from get_similar_players in table.py
        """
        # Create the plot layout
        #Local Normalization / Global Normalization
        # if selected_player:
        #     selected_player_df = main_df.drop(columns=['team', 'position', 'birth_year'])
        #     selected_player_df = selected_player_df.loc[selected_player]
        #     if local_normalization:
        #         normalized_df = selected_player_df.apply(normalize_using_max)
        #     else:
        #         normalized_df = normalized_main_df.loc[selected_player]
        # elif not similar_player_df.empty:
        if local_normalization:
            normalized_df = similar_players_df.apply(self.normalize_using_max).drop(columns=['position'])
        else:
            normalized_df = normalized_main_df.loc[similar_players_df.index]
        
        # if selected_player: print('a')
        # if not similar_players_df.empty: print('b')
        # if local_normalization: print('c')

        fig = go.Figure()
        fig.add_trace(go.Heatmap(
            name="",
            customdata=similar_players_df,
            z=normalized_df,
            x=normalized_df.columns,
            y=normalized_df.index,
            hovertemplate='Player: %{y}<br>%{x}: %{customdata:.2f}',
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
                title_font=dict(size=17, color='#9D9D9D')
            ),
            xaxis_title="Attributes",
            yaxis_title="Players"
            )
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        
        return fig