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
                dcc.Graph(id=self.html_id, figure=self.initial_heatmap(),
            style={'margin': 'auto', 'width': '100%', 'height': '600px', 'text-align': 'center', 'padding': 10})
        )
    
    def normalize_using_max(self, column):
        max_val = column.max()
        if max_val > 0: return column / max_val
        else: return column

    def update(self, goalkeeper_mode, player, similar_player_names, local_normalization):
        """ 
        @similar_players_df List(str): dataframe from get_similar_players in table.py
        """
        print(similar_player_names)
        if not goalkeeper_mode:
            if local_normalization:
                normalized_df = df_hm.loc[similar_player_names].apply(self.normalize_using_max)
            else:
                normalized_df = df_hm_norm.loc[similar_player_names]
            customdata_input = df_hm.loc[similar_player_names]
        else: 
            if local_normalization:
                normalized_df = df_gk_hm.loc[similar_player_names].apply(self.normalize_using_max)
            else:
                normalized_df = df_gk_hm_norm.loc[similar_player_names]
            customdata_input = df_gk_hm.loc[similar_player_names]

        show_y_ticks = len(normalized_df) <= 9 # if more player are selected than the y axis can fit, dont show names.

        fig = go.Figure()
        fig.add_trace(go.Heatmap(
            name="", # removes 'trace' label when hovering
            customdata=customdata_input,
            z=normalized_df,
            x=normalized_df.columns,
            y=normalized_df.index,
            hovertemplate='Player: %{y}<br>%{x}: %{customdata:.2f}',
            hoverongaps = False,
            colorscale='Viridis'))
        
        return self.update_heatmap_layout(fig, player, show_y_ticks)
    
    def initial_heatmap(self, goalkeeper_mode=False):
        """
        Creates a basic heatmap with the top 5 values from main_df
        @return (figure) created heatmap figure
        """
        if goalkeeper_mode:
            first_five_values_df = df_gk_hm_norm.head(5)
            customdata_input = df_gk_hm.head()
        else:
            first_five_values_df = df_hm_norm.head(5)
            customdata_input = df_hm.head()

        fig = go.Figure()

        fig.add_trace(go.Heatmap(
            name="", # removes 'trace' label when hovering
            z=first_five_values_df,
            x=first_five_values_df.columns,
            y=first_five_values_df.index,
            customdata=customdata_input,
            hovertemplate='Player: %{y}<br>%{x}: %{customdata:.2f}',
            colorscale='Viridis'))
        
        return self.update_heatmap_layout(fig, None, True)
    
    def update_heatmap_layout(self, fig, player, show_y_ticks):
        """
        Updates a figures style
        @fig (figure): a graph figure to be updated
        @return (figure): updated figure
        """
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
                showticklabels=show_y_ticks
            ),
            xaxis_title="Attributes",
            yaxis_title="Players"
            )
        if player:
            fig.update_layout(title = f"5 most similar players to {player}",
                              title_font_color = '#ebebeb', title_x = 0.3)
        else:
            fig.update_layout(title = f"No player selected",
                    title_font_color = '#ebebeb', title_x = 0.3)
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        return fig