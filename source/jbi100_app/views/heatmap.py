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
                dcc.Graph(id=self.html_id, figure=self.initial_heatmap()),
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
        # Next step is to create two routes, depending on wheter 1st/2nd input == None. [done]
        # i.e., the heatmap for 5 similiar players or the scatterplot selection. [done]
        # Next step is to make sure that the hover tempplate is correct for each of the 4 scenarios.

        if not selected_player: # If 5 similar players are given, and no selection is made in the scatter plot.
            if local_normalization:
                normalized_df = similar_players_df.apply(self.normalize_using_max).drop(columns=['position'])
            else:
                normalized_df = normalized_main_df.loc[similar_players_df.index]
            customdata_input = similar_players_df
        else: # If a player selection is made in the scatter plot.
            if local_normalization:
                normalized_df = normalized_main_df.loc[selected_player].apply(self.normalize_using_max)
            else:
                normalized_df = normalized_main_df.loc[selected_player]
            customdata_input = main_df.drop(columns=['team', 'position', 'birth_year']).loc[selected_player]

        if len(normalized_df) > 9: 
            y_axis = []
        else: 
            y_axis = normalized_df.index


        fig = go.Figure()
        fig.add_trace(go.Heatmap(
            name="",
            customdata=customdata_input,
            z=normalized_df,
            x=normalized_df.columns,
            y=y_axis,
            hovertemplate='Player: %{y}<br>%{x}: %{customdata:.2f}',
            colorscale='Viridis'))
        
        return self.update_heatmap_layout(fig)
    
    def initial_heatmap(self):
        """
        Creates a basic heatmap with the top 5 values from main_df
        @return (figure) created heatmap figure
        """
        first_five_values_df = normalized_main_df.head(5)

        fig = go.Figure()

        fig.add_trace(go.Heatmap(
            z=first_five_values_df,
            x=first_five_values_df.columns,
            y=first_five_values_df.index,
            colorscale='Viridis'))
        
        return self.update_heatmap_layout(fig)
    
    def update_heatmap_layout(self, fig):
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
                title_font=dict(size=17, color='#9D9D9D')
            ),
            xaxis_title="Attributes",
            yaxis_title="Players"
            )
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        return fig