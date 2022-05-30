from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

# """
# # Welcome to Streamlit!

# Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

# If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
# forums](https://discuss.streamlit.io).

# In the meantime, below is an example of what you can do with just a few lines of code:
# """


# with st.echo(code_location='below'):
#     total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
#     num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

#     Point = namedtuple('Point', 'x y')
#     data = []

#     points_per_turn = total_points / num_turns

#     for curr_point_num in range(total_points):
#         curr_turn, i = divmod(curr_point_num, points_per_turn)
#         angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#         radius = curr_point_num / total_points
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         data.append(Point(x, y))

#     st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#         .mark_circle(color='#0068c9', opacity=0.5)
#         .encode(x='x:Q', y='y:Q'))
"""
# Player Analysis Dashboard
This is a test to see if streamlit can deploy a plotly dash app.
"""
    
    
# Pandas, Plotly, and NumPy modules
import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Google Sheets Modules
import gspread
from df2gspread import  df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

# Misc. Modules
import json
import sys

SHIFT_NUMBER = int(input('Enter Pin: '))
PLAYER_ID = int(input('Enter Player ID: '))

# Shift Encryption
def encrypt(str, shift):
    encryptedString = ''
    for char in str:
        encryptedString += chr(ord(char) + shift)
    return encryptedString

# Shift Decryption
def decrypt(str, shift):
    decryptedString = ''
    for char in str:
        decryptedString += chr(ord(char) - shift)
    return decryptedString

# Encrypts the JSON file
def encryptJson(filename, shift):
    file = open(f"assets/{filename}", 'r+')
    data = json.load(file)
    for key in data:
        data[key] = encrypt(data[key], shift)
    file.seek(0)
    file.write(json.dumps(data))
    file.truncate()
    
# Decrypts the JSON file
def decryptJson(filename, shift):
    file = open(f"assets/{filename}", 'r+')
    data = json.load(file)
    for key in data:
        data[key] = decrypt(data[key], shift)
    file.seek(0)
    file.write(json.dumps(data))
    file.truncate()

# Decrypt the creds.json file at the before the data pull
decryptJson('creds.json', SHIFT_NUMBER)
    
# Spreadsheet Connection
try:
    print('Starting Data Pull...')
    WORKSHEET_ID = '1-kUlYLeDEQyzw2PYnLn6quq7kFYJbduI_Zrk_bQ7_9A'
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    path = 'assets/creds.json'
    google_key_file = path
    credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
    gc = gspread.authorize(credentials)
    
    # Opening the workbook
    workbook = gc.open_by_key(WORKSHEET_ID)

    # Opening separate worksheets
    AnalysisDashboard = workbook.worksheet('AnalysisDashboard')
    PlayerOllie = workbook.worksheet('PlayerOllie')
    TeamOllie = workbook.worksheet('TeamOllie')
    RosterOverview = workbook.worksheet('RosterOverview')
    
    print('Data Pull SUCCESS')
except Exception as e:
    print('Data Pull FAILED')
    
    
# Encrypt the creds.json file once finished with the data pull
encryptJson('creds.json', SHIFT_NUMBER)

# Set the Player ID
try:
    AnalysisDashboard.update('E4', PLAYER_ID)
except:
    pass

# Setup Graphs and Charts
# Fix Spreadsheet Range List Format
radar_stats = AnalysisDashboard.get('AR2:AR6')
for i in range(len(radar_stats)):
    radar_stats[i] = float(radar_stats[i].pop(0))
# Radar Chart
fig_radar = go.Figure()
fig_radar.add_traces(go.Scatterpolar(
    r=radar_stats,
    theta=AnalysisDashboard.get('AQ2:AQ6'),
    fill='toself',
    name='Player Data'
))
fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 10]
        )
    ),
    showlegend=False
)
# Line Charts
key_passes_stats = AnalysisDashboard.get('AA3:AA14')
key_passes_stats_x = AnalysisDashboard.get('W3:W14')
for i in range(len(key_passes_stats)):
    key_passes_stats[i] = float(key_passes_stats[i].pop(0))
    key_passes_stats_x[i] = key_passes_stats_x[i].pop(0)
fig_line = go.Figure()
print(key_passes_stats)
print(key_passes_stats_x)
fig_line.add_trace(go.Scatter(
    x=key_passes_stats_x,
    y=key_passes_stats,
    line=dict(color='firebrick', width=4)
))

# Layout of Dash Plotly Dashboard
def dash_layout():
    return html.Div(className='body', children=[
                html.Div(className='title', children=[
                    html.H1(className='headers', children=[
                        AnalysisDashboard.acell('A6').value
                    ]),
                    html.H2(className='headers', children=[
                        'Player Report'
                    ])
                ]),
                html.Div(className='stats', children=[
                    html.Div(className='offense', children=[
                        html.H2(className='headers', children=[
                            'Offense'
                        ]),
                        html.Div(className='offense-stats', children=[
                            html.Ul(className='stats-list', children=[
                                html.Li('Goals: '),
                                html.Li('Shots: '),
                                html.Li('Shots on Goal: '),
                                html.Li('Assists & Key Passes: '),
                                html.Li('Success Rate with Ball: '),
                                html.Li('Turnovers: ')
                            ]),
                            html.Ul(className='stats-numbers', children=[
                                html.Li(AnalysisDashboard.acell('C8').value),
                                html.Li(AnalysisDashboard.acell('C9').value),
                                html.Li(AnalysisDashboard.acell('C10').value),
                                html.Li(AnalysisDashboard.acell('C11').value),
                                html.Li(AnalysisDashboard.acell('C12').value),
                                html.Li(AnalysisDashboard.acell('C13').value)
                            ])
                        ])
                    ]),
                    html.Div(className='defense', children=[
                        html.H2(className='headers', children=[
                            'Defense'
                        ]),
                        html.Div(className='defense-stats', children=[
                            html.Ul(className='stats-list', children=[
                                html.Li('Fouls: '),
                                html.Li('Recoveries: '),
                                html.Li('Yellow Cards: '),
                                html.Li('Red Cards: ')
                            ]),
                            html.Ul(className='stats-numbers', children=[
                                html.Li(AnalysisDashboard.acell('E8').value),
                                html.Li(AnalysisDashboard.acell('E9').value),
                                html.Li(AnalysisDashboard.acell('E10').value),
                                html.Li(AnalysisDashboard.acell('E11').value)
                            ])
                        ])
                    ]),
                    html.Div(className='work', children=[
                        html.H2(className='headers', children=[
                            'Work'
                        ]),
                        html.Div(className='work-stats',children=[
                            html.Ul(className='stats-list', children=[
                                html.Li('Participation %: '),
                                html.Li('Passes Completed: '),
                                html.Li('Two Mile (seconds): ')
                            ]),
                            html.Ul(className='stats-numbers', children=[
                                html.Li(AnalysisDashboard.acell('G8').value),
                                html.Li(AnalysisDashboard.acell('G9').value),
                                html.Li(AnalysisDashboard.acell('G10').value)
                            ])
                        ])
                    ])
                ]),
                html.Div(className='chart-container', children=[
                    html.Div(className='radar-chart', children=[
                        dcc.Graph(className='chart', figure=fig_radar)
                    ]),
                    html.Div(className='line-chart', children=[
                        dcc.Graph(className='chart', figure=fig_line)
                    ])
                ])
            ])

app = dash.Dash(__name__)

app.layout = dash_layout()

if __name__ == '__main__':
    app.run_server(debug=False)
