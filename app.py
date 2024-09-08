import sys
import os
import pandas as pd
import numpy as np
import flask
import dash_player
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, callback

path = os.path.dirname(os.path.realpath(__file__))
dir_file = os.listdir(path + "/video")


df = pd.read_csv("data/timeseries.csv")


# https://dash.plotly.com/dash-player
app = Dash(__name__)
app.title = "Crover data visualiser tool"
app.layout = html.Div([
      html.Div(html.H2("Crover video plot visualiser")),
      dash_player.DashPlayer(
            id="player",
            url="/video/test1.mp4",
            controls=True,
            width="50%",
            height="50%"
      ),
      dcc.Dropdown(id="dropdown",options=["geography", "New York"],value='New York'),
      dcc.Slider(0, id="video_start_slider" ,marks=None),                            
      html.Div([dcc.Graph(id="graph")])
    
    ])


@app.callback(Output(component_id="video_start_slider", component_property="max"),
              Input(component_id="player", component_property="duration")
              )
def update_video_start_point(value):
    return value

@app.callback(Output(component_id="graph", component_property="figure"),
              Input(component_id="video_start_slider", component_property="value"),
              Input(component_id="player", component_property="currentTime")
              )
def update_line_chart(duration, current_time):
    fig = px.line()

    if duration is not None:
        # x_axis = [value for value in np.arange(0., duration, 1.0)]
        fig = px.line(df,x = "Date", y=["B", "D"] , hover_data=[df.index], markers=True)
        fig.add_vline(x=duration, line_width=3, line_dash="dash", line_color="green")
        fig.add_vline(x=current_time, line_width=3, line_dash="dash", line_color="red")

    return fig

# For loading static director to acess
server = app.server

@server.route("/video/<path:path>")
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, "video"), path)

@server.route("/data/<path:path>")
def serve_static_data(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, "data"), path)

if __name__ == "__main__":
    app.run(debug=True)
