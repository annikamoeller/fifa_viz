from dash import dcc, html
from ..config import *
from .scatterplot import *
from dash.dependencies import Input, Output


scatter_plot = Scatterplot("shot_distance", 'birth_year', 'average_shot_distance', player_stats)

"""
Sub menu class of the left handside of the web page
"""
def generate_description_card():
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

def generate_control_card():
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

def generate_scatter():
    """

    :return: A div with a scatter plot
    """

    return scatter_plot

    

def make_menu_layout():
    """
    Defines the elements that the submenu has and are returned to the main menu
    """
    return [generate_description_card(), generate_control_card(), generate_scatter()]
