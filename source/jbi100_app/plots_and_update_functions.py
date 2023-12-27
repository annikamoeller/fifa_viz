from dash import dcc, html
from .config import *
from PIL import Image
import plotly.express as px

def build_background_fig():
    field_image = Image.open('jbi100_app/assets/soccer_field_3.jpg')
    field_width, field_height = field_image.size
    ar = field_width / field_height
    fig = px.imshow(field_image)
    return fig

# Testing commit/push