import os
import pandas as pd
import glob
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

# Initialize the Dash app
app = Dash(__name__)
server= app.server

# Initialize lists to hold data for each lap
time_data = []
speed_data = []
rpm_data = []
gear_data = []
accel_data = []
clutch_data = []
steering_data = []
laps = []

# Read each CSV file (assuming they are named 'testlap1.csv', 'testlap2.csv', etc.)
file_pattern = "testlap*.csv"
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

        time_data.append(df['Time (sec)'])
        speed_data.append(df['Vehicle Speed (mph)'])
        rpm_data.append(df['Engine RPM (RPM)'])
        gear_data.append(df['Gear Current (Gear)'])
        accel_data.append(df['Accel. Pedal Pos. (%)'])
        clutch_data.append(df['Clutch Pedal Pos. (%)'])
        steering_data.append(df['(TC) Steering Wheel Angle (degrees)'])
        laps.append(f'Lap {idx + 1}')
else:
    print("No files found matching the pattern 'testlap*.csv'.")

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
    speed_fig.add_trace(go.Scatter(x=time_data[i], y=speed_data[i], mode='lines', name=f'Lap {i + 1}'))
speed_fig.update_layout(title='Speed over Time', xaxis_title='Time (s)', yaxis_title='Speed (mph)')

rpm_fig = go.Figure(layout=layout)
for i in range(len(time_data)):
    rpm_fig.add_trace(go.Scatter(x=time_data[i], y=rpm_data[i], mode='lines', name=f'Lap {i + 1}'))
rpm_fig.update_layout(title='Engine RPM over Time', xaxis_title='Time (s)', yaxis_title='Engine RPM')

gear_fig = go.Figure(layout=layout)
for i in range(len(time_data)):
    gear_fig.add_trace(go.Scatter(x=time_data[i], y=gear_data[i], mode='lines', name=f'Lap {i + 1}'))
gear_fig.update_layout(title='Gear over Time', xaxis_title='Time (s)', yaxis_title='Gear')

accel_fig = go.Figure(layout=layout)
for i in range(len(time_data)):
    accel_fig.add_trace(go.Scatter(x=time_data[i], y=accel_data[i], mode='lines', name=f'Lap {i + 1}'))
accel_fig.update_layout(title='Accelerator Pedal Position over Time', xaxis_title='Time (s)',
                        yaxis_title='Accelerator Pedal Position (%)')

clutch_fig = go.Figure(layout=layout)
for i in range(len(time_data)):
    clutch_fig.add_trace(go.Scatter(x=time_data[i], y=clutch_data[i], mode='lines', name=f'Lap {i + 1}'))
clutch_fig.update_layout(title='Clutch Pedal Position over Time', xaxis_title='Time (s)',
                         yaxis_title='Clutch Pedal Position (%)')

steering_fig = go.Figure(layout=layout)
for i in range(len(time_data)):
    steering_fig.add_trace(go.Scatter(x=time_data[i], y=steering_data[i], mode='lines', name=f'Lap {i + 1}'))
steering_fig.update_layout(title='Steering Wheel Angle over Time', xaxis_title='Time (s)',
                           yaxis_title='Steering Wheel Angle (degrees)')

# Create figure for combined data
combined_fig = go.Figure(layout=layout)

# Define the layout of the app
app.layout = html.Div([
    html.H1('Car Racing Data Dashboard', style={'color': 'white', 'textAlign': 'center'}),
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
], style={'backgroundColor': 'black', 'color': 'white'})


# Define the callback to update the combined graph
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

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host="0.0.0.0", port=port)
