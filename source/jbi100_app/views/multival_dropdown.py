from dash import dcc, html
from jbi100_app.config import *

class MultiValDropdown(html.Div):
    def __init__(self, name, dropDownValues, startingValue, label=None, df=None):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.dropDownValues = dropDownValues

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.Label(label),
                dcc.Dropdown(
                    id=self.html_id,
                    options=dropDownValues,
                    value=startingValue,
                    multi=True
                )
            ], style={'margin': 'auto', 'width': '17%', 'color': 'black'}
        )

    def update(self, selected_stat):
        if selected_stat == 'Goalkeeper': df = goalkeeping_radar_df
        if selected_stat == 'Defender': df = defense_radar_df
        if selected_stat == 'Midfilder': df = midfielder_radar_df
        if selected_stat == 'Striker': df = striker_radar_df
        return df.columns.tolist()