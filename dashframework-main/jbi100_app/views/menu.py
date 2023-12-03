from dash import dcc, html
from ..config import teams_list


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

    :return: A Div containing controls for graphs.
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


def make_menu_layout():
    return [generate_description_card(), generate_control_card()]
