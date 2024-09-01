import sys
import os
import pandas as pd
import flask
import dash_player
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, callback

path = os.path.dirname(os.path.realpath(__file__))
dir_file = os.listdir(path + "/video")
print(dir_file)
print("here")
# https://dash.plotly.com/dash-player
app = Dash(__name__)
app.title = "Crover data visualiser tool"
app.layout = html.Div(
    [
        html.Div(html.H2("Crover data visualiser tool")),
        html.Div(
            [
                # html.Div(
                #     children=[
                #         html.Video(
                #             id="player",
                #             src="/video/Bezubaan_Phir_Se__ABCD_2__Varun_Dhawan_-_Shraddha_Kapoor__Sachin_-_Jigar.mp4",
                #             controls=True,
                #         ),
                #         dcc.Checklist(
                #             id="bool-props-radio",
                #             options=[
                #                 {"label": val.capitalize(), "value": val}
                #                 for val in [
                #                     "playing",
                #                     "loop",
                #                     "controls",
                #                     "muted",
                #                 ]
                #             ],
                #             value=["controls"],
                #             inline=True,
                #             style={"margin": "20px 0px"},
                #         ),
                #     ]
                # ),
                # dash_player.DashPlayer()
                html.Div(
                    style={"width": "50%", "padding": "0px"},
                    children=[
                        dash_player.DashPlayer(
                            id="player",
                            url="/video/test1.mp4",
                            controls=True,
                            width="100%",
                            height="100%",
                        ),
                        # dcc.Checklist(
                        #     id="bool-props-radio",
                        #     options=[
                        #         {"label": val.capitalize(), "value": val}
                        #         for val in [
                        #             "playing",
                        #             "loop",
                        #             "controls",
                        #             "muted",
                        #         ]
                        #     ],
                        #     value=["controls"],
                        #     inline=True,
                        #     style={"margin": "20px 0px"},
                        # ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="seekto-number-input",
                                    type="number",
                                    placeholder="seekTo value",
                                    style={"width": "calc(100% - 115px)"},
                                ),
                                html.Button(
                                    "seekTo",
                                    id="seekto-number-btn",
                                    style={"width": "105px"},
                                ),
                            ],
                            style={"margin": "20px 0px"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    id="current-time-div",
                                    style={"margin": "10px 0px"},
                                ),
                                html.Div(
                                    id="seconds-loaded-div",
                                    style={"margin": "10px 0px"},
                                ),
                                html.Div(
                                    id="duration-div",
                                    style={"margin": "10px 0px"},
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "column",
                            },
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%", "padding": "10px"},
                    children=[
                        html.P("Volume:", style={"marginTop": "30px"}),
                        dcc.Slider(
                            id="volume-slider",
                            min=0,
                            max=1,
                            step=0.05,
                            value=0.5,
                            updatemode="drag",
                            marks={0: "0%", 0.5: "50%", 1: "100%"},
                        ),
                        html.P("Playback Rate:", style={"marginTop": "25px"}),
                        dcc.Slider(
                            id="playback-rate-slider",
                            min=0,
                            max=2,
                            step=None,
                            updatemode="drag",
                            marks={i: str(i) + "x" for i in [0, 0.5, 1, 1.5, 2]},
                            value=1,
                        ),
                        html.P(
                            "Update Interval for Current Time:",
                            style={"marginTop": "30px"},
                        ),
                        dcc.Slider(
                            id="intervalCurrentTime-slider",
                            min=0,
                            max=1000,
                            step=None,
                            updatemode="drag",
                            marks={i: str(i) for i in [0, 250, 500, 750, 1000]},
                            value=250,
                        ),
                        html.P(
                            "Update Interval for Seconds Loaded:",
                            style={"marginTop": "30px"},
                        ),
                        dcc.Slider(
                            id="intervalSecondsLoaded-slider",
                            min=0,
                            max=1000,
                            step=None,
                            updatemode="drag",
                            marks={i: str(i) for i in [0, 250, 500, 750, 1000]},
                            value=500,
                        ),
                        html.P(
                            "Update Interval for Duration:",
                            style={"marginTop": "30px"},
                        ),
                        dcc.Slider(
                            id="intervalDuration-slider",
                            min=0,
                            max=1000,
                            step=None,
                            updatemode="drag",
                            marks={i: str(i) for i in [0, 250, 500, 750, 1000]},
                            value=500,
                        ),
                    ],
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "space-between",
            },
        ),
    ]
)


@callback(
    Output("player", "playing"),
    Output("player", "loop"),
    Output("player", "controls"),
    Output("player", "muted"),
    Input("bool-props-radio", "value"),
)
def update_bool_props(values):
    playing = "playing" in values
    loop = "loop" in values
    controls = "controls" in values
    muted = "muted" in values
    print(playing)
    print(loop)
    return playing, loop, controls, muted


@callback(
    Output("player", "seekTo"),
    Input("seekto-number-btn", "n_clicks"),
    State("seekto-number-input", "value"),
)
def set_prop_seekTo(n_clicks, seekto):
    return seekto


@callback(
    Output("current-time-div", "children"),
    Input("player", "currentTime"),
)
def display_currentTime(currentTime):
    return f"Current Time: {currentTime}"


@callback(
    Output("seconds-loaded-div", "children"),
    Input("player", "secondsLoaded"),
)
def display_secondsLoaded(secondsLoaded):
    return f"Second Loaded: {secondsLoaded}"


@callback(
    Output("duration-div", "children"),
    Input("player", "duration"),
)
def display_duration(duration):
    return f"Duration: {duration}"


@callback(
    Output("player", "volume"),
    Input("volume-slider", "value"),
)
def set_volume(value):
    return value


@callback(
    Output("player", "playbackRate"),
    Input("playback-rate-slider", "value"),
)
def set_playbackRate(value):
    return value


@callback(
    Output("player", "intervalCurrentTime"),
    Input("intervalCurrentTime-slider", "value"),
)
def set_intervalCurrentTime(value):
    return value


@callback(
    Output("player", "intervalSecondsLoaded"),
    Input("intervalSecondsLoaded-slider", "value"),
)
def set_intervalSecondsLoaded(value):
    return value


@callback(
    Output("player", "intervalDuration"),
    Input("intervalDuration-slider", "value"),
)
def set_intervalDuration(value):
    return value


server = app.server


@server.route("/video/<path:path>")
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, "video"), path)


print(os.path.join(os.getcwd(), "video"))

if __name__ == "__main__":
    app.run(debug=False)
