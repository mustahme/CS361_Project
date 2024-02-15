import dash
from dash import html, dcc, Input, Output, callback_context
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# Sample data for Glenn Canyon (placeholder, replace with actual data loading)
glenn_dam_data = {
    'Time': [
        '2/09/23 12:00', '2/10/23 12:00', '2/11/23 12:00', '2/12/23 12:00',
        '2/13/23 12:00', '2/14/23 12:00', '2/15/23 12:00','2/16/23 12:00'
    ],
    'Volume (acre-ft)': [300229, 301759, 299299, 298029, 299912, 302500, 303391, 304083],
    'Dam Name': ['Glenn Canyon'] * 8
}

current_water_level = glenn_dam_data.get('Volume (acre-ft)')[len(glenn_dam_data.get('Time'))-1]
df = pd.DataFrame(glenn_dam_data)


# Assuming you have a function that gets the current water level and weather
def get_current_conditions():
    # Placeholder function to simulate getting current data
    return {
        'current_water_level': '304,083 acre-ft',
        'current_water_state': 'Healthy',
        'weather': 'Sunny, 75°F'
    }

def generate_water_level_info(current_water_level):
    # Convert current_water_level to a number if it's a string
    try:
        water_level_value = current_water_level
    except ValueError:
        water_level_value = 0  # Default value in case of conversion failure

    # Determine the color and state based on the threshold
    if water_level_value > 300000:  # Example threshold
        color = 'ForestGreen'
        water_state = 'Exceptional Health'
    elif water_level_value > 250000:  # Example threshold
        color = 'Green'
        water_state = 'Healthy'
    elif water_level_value > 200000:  # Example threshold
        color = 'GreenYellow'
        water_state = 'Normal'
    elif water_level_value > 200000:  # Example threshold
        color = 'orange'
        water_state = 'Drought'
    else:
        color = 'red'
        water_state = 'Servere Drought'

    # Generate the components with styling and content
    water_level_component = html.P(f'Current Water Volume: {current_water_level}'+' acre-feet', style={'color': color, 'text-align': 'center'})
    water_state_component = html.P(f'Current Water State: {water_state}', style={'text-align': 'center'})

    return [water_level_component, water_state_component]

# Define the homepage layout
home_page_layout = html.Div([
    html.H1('Dam Monitoring Dashboard', style={'padding': '5px', 'text-align': 'center'}),
    html.Div(id='navigation',style={'color': '#000000', 'padding': '5px', 'text-align': 'center'}, children = [
        dcc.Link('Go to Water Level Graph', href='/water-level-graph', style={
            'align':'center',
            'padding': '10px 15px',
            'background-color': '#007BFF',
            'color': 'white',
            'border-radius': '5px',
            'text-decoration': 'none',
            'display': 'inline-block',
            'margin':'5px'
        }),
        dcc.Link('FAQ / How to', href='/faq', style={
            'padding': '10px 15px',
            'background-color': '#007BFF',
            'color': 'white',
            'border-radius': '5px',
            'text-decoration': 'none',
            'display': 'inline-block',
            'margin': '10px 0'
        }),
    ]),
    html.Div(generate_water_level_info(current_water_level)),
    html.Div(id='current-conditions', style={'color': '#000000', 'padding': '5px', 'text-align': 'center'}, children=[
        html.P('Current weather: ' + get_current_conditions()['weather'])
    ]),

])

# Define the layout for the water level graph page
graph_page_layout = html.Div([
    html.H1('Water Level Graph', style={'padding': '5px', 'text-align': 'center'}),
    html.Div(id='navigation',style={'color': '#000000', 'padding': '5px', 'text-align': 'center'}, children = [
    dcc.Link('Return Home', href='/', style={
        'padding': '10px 15px',
        'background-color': '#007BFF',
        'color': 'white',
        'border-radius': '5px',
        'text-decoration': 'none',
        'display': 'inline-block',
        'margin':'5px'
    }),     dcc.Link('FAQ / How to', href='/faq', style={
        'padding': '10px 15px',
        'background-color': '#007BFF',
        'color': 'white',
        'border-radius': '5px',
        'text-decoration': 'none',
        'display': 'inline-block',
        'margin': '10px 0'
    }),]),
    dcc.Checklist(
        id='toggle-projections',
        options=[
            {'label': 'Show Conservative Projection', 'value': 'CP'},
            {'label': 'Show Aggressive Projection', 'value': 'AP'}
        ],
        value=[]  # Default is hiding both projections
    ),
    html.Button("Download Data", id="btn_download"),
    dcc.Download(id="download-dataframe-csv"),
    dcc.Graph(id='water-level-graph')
])

# FAQ/How to Use Page Layout
faq_page_layout = html.Div([
    html.H1('FAQ / How to', style={'text-align': 'center'}),
    html.Div([
        dcc.Link('Go back to Home', href='/', style={
            'padding': '10px 15px',
            'background-color': '#007BFF',
            'color': 'white',
            'border-radius': '5px',
            'text-decoration': 'none',
            'display': 'inline-block',
            'margin': '10px 0'
        }),
        dcc.Link('Go to Water Level Graph', href='/water-level-graph', style={
            'align': 'center',
            'padding': '10px 15px',
            'background-color': '#007BFF',
            'color': 'white',
            'border-radius': '5px',
            'text-decoration': 'none',
            'display': 'inline-block',
            'margin': '5px'
        }),
    ], style={'color': '#000000', 'padding': '5px', 'text-align': 'center'}),
    html.Div([
        html.H3('How do I reset page?'),
        html.P('Click home icon in top right corner'),
        html.H3('How can I check individual data points?'),
        html.P('Hover over data points to see details regarding each unit.'),
        html.H3('How often does data update?'),
        html.P('Data will be requested from our provider each time the page is refreshed.'),
        # Add more questions and answers as needed
    ],style={'text-align': 'center'}),

])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/water-level-graph':
        return graph_page_layout
    elif pathname == '/faq':
        return faq_page_layout  # Return the FAQ page layout when the URL matches
    else:
        return home_page_layout

# Callback to generate and download CSV file
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_download", "n_clicks"),
    prevent_initial_call=True
)
def download_data(n_clicks):
    return dcc.send_data_frame(df.to_csv, "my_data.csv")

# Callback for updating the graph with the projections
@app.callback(
    Output('water-level-graph', 'figure'),
    [Input('toggle-projections', 'value')],
    #prevent_initial_call=True
)
def update_graph(toggle_values):
    # Convert to DataFrame
    df = pd.DataFrame(glenn_dam_data)
    df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%y %H:%M')

    # Generate a plot with Plotly for the known data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Time'], y=df['Volume (acre-ft)'], mode='lines+markers', name='Actual Volume'))

    # Generate projected data for the next 8 days with two different models
    last_known_volume = df['Volume (acre-ft)'].iloc[-1]
    last_known_date = df['Time'].iloc[-1]
    projection_start_date = last_known_date + timedelta(days=0)

    # Conservative and aggressive projections
    conservative_projection = [last_known_volume + (i * i * 10) for i in range(8)]
    aggressive_projection = [last_known_volume + (i * 100 + i * i * i * i) for i in range(8)]

    # Add the conservative projected data to the plot
    fig.add_trace(go.Scatter(
        x=[projection_start_date + timedelta(days=i) for i in range(8)],
        y=conservative_projection,
        mode='lines+markers',
        name='Conservative Projection',
        line=dict(dash='dash'),
        visible='CP' in toggle_values  # Set visibility based on toggle
    ))

    # Add the aggressive projected data to the plot
    fig.add_trace(go.Scatter(
        x=[projection_start_date + timedelta(days=i) for i in range(8)],
        y=aggressive_projection,
        mode='lines+markers',
        name='Aggressive Projection',
        line=dict(dash='dash'),
        visible='AP' in toggle_values  # Set visibility based on toggle
    ))

    # Add annotation for the last known volume
    fig.add_annotation(
        x=last_known_date,
        y=last_known_volume,
        text=f"Last known volume: {last_known_volume} acre-ft",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )

    fig.update_layout(title='Water Level at Glenn Canyon')
    fig.data[1].visible = 'CP' in toggle_values  # Conservative projection visibility
    fig.data[2].visible = 'AP' in toggle_values  # Aggressive projection visibility

    return fig



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Tracking URL location
    html.Div(id='page-content')  # Content will be rendered in this div
])

if __name__ == '__main__':
    app.run_server(debug=True)

