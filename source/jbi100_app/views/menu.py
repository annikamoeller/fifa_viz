from dash import dcc, html
from ..config import *
from .scatterplot import *
from dash.dependencies import Input, Output
from .radar import *




"""
Sub menu class of the left handside of the web page
"""


class Menu():
    def __init__(self, plots):
        self.plots = plots
        pass

    def generate_description_card(self):
        """
        :return: A Div containing dashboard title & descriptions.
        """
        return [html.Div(
            id="description-card",
            children=[
                html.H5("Example dashboard"),
                html.Div(
                    id="intro",
                    children="Select a team.",
                ),
            ],
        )]

    def generate_dropdown(self):
        """
        :return: A div with a drop down for the teams
        """
        return [html.Div(
            id="control-card",
            children=[
                html.Label("Select a team"),
                dcc.Dropdown(
                    id="select-team",
                    options=[{"label": i, "value": i} for i in teams_list],
                    value=teams_list[0],
                )
            ], style={"textAlign": "float-left"}
        )]

    def generate_plots(self):
        """
        :return: A div with a scatter plot
        """
        plots = []
        for plot in self.plots:
            plots.append(plot)
        return plots

    def make_menu_layout(self):
        """
        Defines the elements that the submenu has and are returned to the main menu
        """
        elements = []
        elements += self.generate_description_card()
        elements += self.generate_dropdown()
        elements += self.generate_plots()
  
        return elements
