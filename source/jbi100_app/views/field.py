from dash import dcc, html
import plotly.graph_objects as go
import pitchly
from pitchly.pitch import Pitch
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

class Field(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")
        self.field = self.build_background_fig()
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="field",
            children=[
                html.Div(
                    id="field",
                    children=dcc.Graph(figure=self.field))]
                )

    def build_background_fig(self):
        field_image = Image.open('jbi100_app/assets/soccer_field_3.jpg')
        field_width, field_height = field_image.size
        ar = field_width / field_height
        fig = px.imshow(field_image)
        fig.update_xaxes(range=[0,field_width], showgrid=False, showticklabels=False)
        fig.update_yaxes(range=[0,field_height], showgrid=False, showticklabels=False)
        fig.update_layout(width=1000, height=1000/ar, xaxis_title=None, yaxis_title=None, dragmode=False) # Fix aspect ratio
        # fig.update_traces(hovertemplate = None, hoverinfo = "skip")
        fig.update_traces(marker=dict(size=16,
                                    line=dict(width=2,
                                                color='Gold'),
                                    color='Orange'),
                        selector=dict(mode='markers'),
                        hovertemplate=None,
                        hoverinfo="skip")
        return fig
    
    def update_field_players(self, team):
        if team:
            self.field.update_xaxes
