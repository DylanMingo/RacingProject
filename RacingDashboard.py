import os
import pandas as pd
import glob
from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objs as go

# Initialize the Dash app
app = Dash(__name__)
server = app.server

# Initialize lists to hold data for each lap
time_data = []
speed_data = []
rpm_data = []
gear_data = []
accel_data = []
clutch_data = []
steering_data = []
laps = []

# Read each CSV file using the correct pattern for your file naming convention
file_pattern = "PE*_Lap*.csv"
files = glob.glob(file_pattern)

if files:
    for idx, file in enumerate(files):
        df = pd.read_csv(file)

        # Filter the data to include only points where speed > 0.5 mph
        df = df[df['Vehicle Speed (mph)'] > 0.5]

        # Adjust the time data to start from zero for each lap
        df['Time (sec)'] = df['Time (sec)'] - df['Time (sec)'].iloc[0]

        # Replace gear position 15 with None to create gaps in the plot
        df['Gear Current (Gear)'] = df['Gear Current (Gear)'].apply(lambda x: None if x == 15 else x)

        # Extract event number and lap number from the filename
        event_num = file.split('_')[0][2:]  # Extract the number after 'PE'
        lap_num = file.split('_')[1][3:].split('.')[0]  # Extract the number after 'Lap'

        # Use the event and lap numbers for naming
        time_data.append(df['Time (sec)'])
        speed_data.append(df['Vehicle Speed (mph)'])
        rpm_data.append(df['Engine RPM (RPM)'])
        gear_data.append(df['Gear Current (Gear)'])
        accel_data.append(df['Accel. Pedal Pos. (%)'])
        clutch_data.append(df['Clutch Pedal Pos. (%)'])
        steering_data.append(df['(TC) Steering Wheel Angle (degrees)'])
        laps.append(f'Event {event_num} - Lap {lap_num}')
else:
    print("No files found matching the pattern 'PE*_Lap*.csv'.")

# Define the layout for dark background
layout = go.Layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False),
    title=dict(x=0.5, xanchor='center')
)

# Create individual figures
speed_fig = go.Figure(layout=layout)
for i in range(len(time_data)):
    speed_fig.add_trace(go.Scatter(x=time_data[i], y=speed_data[i], mode='lines', name=laps[i]))
speed_fig.update_layout(title='Speed over Time', xaxis_title='Time (s)', yaxis_title='Speed (mph)')

rpm_fig = go.Figure(layout=layout)
for i in range(len(time_data)):
    rpm_fig.add_trace(go.Scatter(x=time_data[i], y=rpm_data[i], mode='lines', name=laps[i]))
rpm_fig.update_layout(title='Engine RPM over Time', xaxis_title='Time (s)', yaxis_title='Engine RPM')

gear_fig = go.Figure(layout=layout)
for i in range(len(time_data)):
    gear_fig.add_trace(go.Scatter(x=time_data[i], y=gear_data[i], mode='lines', name=laps[i]))
gear_fig.update_layout(title='Gear over Time', xaxis_title='Time (s)', yaxis_title='Gear')

accel_fig = go.Figure(layout=layout)
for i in range(len(time_data)):
    accel_fig.add_trace(go.Scatter(x=time_data[i], y=accel_data[i], mode='lines', name=laps[i]))
accel_fig.update_layout(title='Accelerator Pedal Position over Time', xaxis_title='Time (s)',
                        yaxis_title='Accelerator Pedal Position (%)')

clutch_fig = go.Figure(layout=layout)
for i in range(len(time_data)):
    clutch_fig.add_trace(go.Scatter(x=time_data[i], y=clutch_data[i], mode='lines', name=laps[i]))
clutch_fig.update_layout(title='Clutch Pedal Position over Time', xaxis_title='Time (s)',
                         yaxis_title='Clutch Pedal Position (%)')

steering_fig = go.Figure(layout=layout)
for i in range(len(time_data)):
    steering_fig.add_trace(go.Scatter(x=time_data[i], y=steering_data[i], mode='lines', name=laps[i]))
steering_fig.update_layout(title='Steering Wheel Angle over Time', xaxis_title='Time (s)',
                           yaxis_title='Steering Wheel Angle (degrees)')

# Define the layout of the app with Tabs
app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Race Data Dashboard', children=[
            html.H1('Racing Data Dashboard', style={'color': 'white', 'textAlign': 'center'}),
            dcc.Graph(figure=speed_fig),
            dcc.Graph(figure=rpm_fig),
            dcc.Graph(figure=gear_fig),
            dcc.Graph(figure=accel_fig),
            dcc.Graph(figure=clutch_fig),
            dcc.Graph(figure=steering_fig),
            html.Div([
                html.Label('Select Lap:', style={'color': 'white'}),
                dcc.Dropdown(
                    id='lap-dropdown',
                    options=[{'label': lap, 'value': lap} for lap in laps],
                    value=[laps[0]] if laps else [],
                    multi=True,
                    style={'backgroundColor': '#333', 'color': 'white'}
                ),
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Select Metric:', style={'color': 'white'}),
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[
                        {'label': 'Speed', 'value': 'speed'},
                        {'label': 'Engine RPM', 'value': 'rpm'},
                        {'label': 'Gear', 'value': 'gear'},
                        {'label': 'Accelerator Pedal Position', 'value': 'accel'},
                        {'label': 'Clutch Pedal Position', 'value': 'clutch'},
                        {'label': 'Steering Wheel Angle', 'value': 'steering'},
                    ],
                    value=['speed'],
                    multi=True,
                    style={'backgroundColor': '#333', 'color': 'white'}
                ),
            ], style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='combined-graph')
        ]),
        dcc.Tab(label='About Me', children=[
            html.H2('About Me', style={'color': 'white'}),
            html.P('Write something about yourself here.', style={'color': 'white'})
        ]),
        dcc.Tab(label='Race Videos', children=[
            html.H2('Upload Videos', style={'color': 'white'}),
            dcc.Upload(
                id='upload-video',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ], style={
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'color': 'white'
                }),
                multiple=True
            ),
            html.Div(id='output-video-upload', style={'color': 'white'})
        ]),
        dcc.Tab(label='Race Results', children=[
            html.H2('Race Details', style={'color': 'white'}),
            # Placeholder for race details content
            html.P('Race times, positions, and other details will be displayed here.', style={'color': 'white'})
        ])
    ], style={'backgroundColor': 'black', 'color': 'white'})
])

# Callback for the combined graph
@app.callback(
    Output('combined-graph', 'figure'),
    [Input('lap-dropdown', 'value'), Input('metric-dropdown', 'value')]
)
def update_combined_graph(selected_laps, selected_metrics):
    combined_fig = go.Figure(layout=layout)

    metric_data = {
        'speed': speed_data,
        'rpm': rpm_data,
        'gear': gear_data,
        'accel': accel_data,
        'clutch': clutch_data,
        'steering': steering_data
    }

    metric_labels = {
        'speed': 'Speed (mph)',
        'rpm': 'Engine RPM',
        'gear': 'Gear',
        'accel': 'Accelerator Pedal Position (%)',
        'clutch': 'Clutch Pedal Position (%)',
        'steering': 'Steering Wheel Angle (degrees)'
    }

    for lap in selected_laps:
        lap_index = laps.index(lap)
        for metric in selected_metrics:
            y_data = metric_data[metric][lap_index]
            combined_fig.add_trace(
                go.Scatter(x=time_data[lap_index], y=y_data, mode='lines', name=f'{lap} - {metric_labels[metric]}'))

    combined_fig.update_layout(
        title=f'Selected Metrics over Time',
        xaxis_title='Time (s)',
        yaxis_title='Value'
    )

    return combined_fig

# Callback for video upload
@app.callback(
    Output('output-video-upload', 'children'),
    [Input('upload-video', 'contents')],
    [State('upload-video', 'filename'), State('upload-video', 'last_modified')]
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            html.Div([
                html.H5(filename),
                html.Video(src=content, controls=True, style={'width': '100%'})
            ]) for content, filename in zip(list_of_contents, list_of_names)
        ]
        return children

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host="0.0.0.0", port=port)

