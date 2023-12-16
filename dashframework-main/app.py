from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.field import *
from jbi100_app.config import *
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
from PIL import Image
    
if __name__ == '__main__':
    # Create data
    df = team_data

    # Instantiate custom views
    field = Field("field")
    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="one-half column",
                children=make_menu_layout()
            ),

            # Right column
            html.Div(
                id="right-column",
                className="one-half column",
            ),
        ],
    )

    #Define interactions
    @app.callback(
        Output(field.html_id, "figure"), 
        [
        #Input("select-team", "value")
        #Input(field.html_id, 'selectedData')
    ])
    def update_field():
        return field.build_background_fig()

    # @app.callback(
    #     Output(scatterplot2.html_id, "figure"), [
    #     Input("select-color-scatter-2", "value"),
    #     Input(scatterplot1.html_id, 'selectedData')
    # ])
    # def update_scatter_2(selected_team, selected_data):
    #     return scatterplot2.update(selected_team, selected_data)


    app.run_server(debug=False, dev_tools_ui=False)