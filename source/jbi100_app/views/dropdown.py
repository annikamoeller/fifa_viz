from dash import dcc, html

class Dropdown(html.Div):
 
    def __init__(self, name, dropDownValues, startingValue, label=None, df=None):
        """
        Create a dropdown
        @name (str): name of the plot, used for html_id
        @dropDownValues (array[str]): an array of values to be displayed on the dropdown 
        @startingValue (str): the starting value for the dropdown
        @label (str): the title above the dropdown, leave empty for none
        """
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
            ], style={'margin': 'auto', 'width': '17%', 'color': 'black'} #Style of the dropdown
        )