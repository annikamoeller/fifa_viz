from dash import dcc, html
from ..config import teams_list
from PIL import Image
import plotly.express as px

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

def generate_field():
    return html.Div(
        id="field",
        children=dcc.Graph(figure=build_background_fig()))

def build_background_fig():
    field_image = Image.open('jbi100_app/assets/soccer_field_3.jpg')
    field_width, field_height = field_image.size
    ar = field_width / field_height
    fig = px.imshow(field_image)
    #fig.update_xaxes(range=[0,field_width], showgrid=False, showticklabels=False)
    #fig.update_yaxes(range=[0,field_height], showgrid=False, showticklabels=False)
    #fig.update_layout(width=1000, height=1000/ar, xaxis_title=None, yaxis_title=None, dragmode=False) # Fix aspect ratio
    # fig.update_traces(hovertemplate = None, hoverinfo = "skip")
    # fig.update_traces(marker=dict(size=16,
    #                             line=dict(width=2,
    #                                         color='Gold'),
    #                             color='Orange'),
    #                 selector=dict(mode='markers'),
    #                 hovertemplate=None,
    #                 hoverinfo="skip")
    return fig
    
def make_menu_layout():
    return [generate_description_card(), generate_control_card(), generate_field()]
