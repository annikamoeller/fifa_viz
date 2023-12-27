from dash import dcc, html

class Dropdown(html.Div):
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
                )
            ], style={'margin': 'auto', 'width': '17%', 'color': 'black'}
        )