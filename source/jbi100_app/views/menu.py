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
        return html.Div(
            id="description-card",
            children=[
                html.H5("Example dashboard"),
                html.Div(
                    id="intro",
                    children="Select a team.",
                ),
            ],
        )

    def generate_control_card(self):
        """

        :return: A div with a drop down for the teams
        """
        return html.Div(
            id="control-card",
            children=[
                html.Label("Select a team"),
                dcc.Dropdown(
                    id="select-team",
                    options=[{"label": i, "value": i} for i in teams_list],
                    value=teams_list[0],
                )
            ], style={"textAlign": "float-left"}
        )

    def generate_scatter(self):
        """

        :return: A div with a scatter plot
        """
        for plot in self.plots:
            if plot.__class__.__name__ == 'Scatterplot':
                return plot

    def generate_radar(self):
        """

        :return: A div with a scatter plot
        """
        for plot in self.plots:
            if plot.__class__.__name__ == 'radar':
                return plot

    def make_menu_layout(self):
        """
        Defines the elements that the submenu has and are returned to the main menu
        """
        return [self.generate_description_card(), self.generate_control_card(), self.generate_scatter(), self.generate_radar()]
