import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    
    # TASK 1: Dropdown list for Launch Site selection
    html.Div([
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
            ],
            value='ALL',  # default value
            placeholder="Select a Launch Site",
            style={'width': '50%', 'padding': '3px', 'font-size': '20px'}
        )
    ]),
    html.Br(),
    
    # TASK 2: Pie chart for Launch success/failure count
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    html.P("Payload range (Kg):"),
    # TASK 3: Payload slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={i: str(i) for i in range(int(min_payload), int(max_payload) + 1, 5000)},
        value=[min_payload, max_payload]
    ),
    
    # TASK 4: Scatter chart for correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2 Callback function
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    
    success_counts = filtered_df['class'].value_counts()
    fig = px.pie(
        values=success_counts,
        names=['Failed', 'Successful'],
        title=f"Launch Success for {selected_site}" if selected_site != 'ALL' else "Launch Success for All Sites"
    )
    return fig

# TASK 4 Callback function
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(
        spacex_df['Payload Mass (kg)'] >= low) & 
        (spacex_df['Payload Mass (kg)'] <= high)
    ]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    fig = px.scatter(
        filtered_df, 
        x='Payload Mass (kg)', 
        y='class', 
        color='Launch Site',
        title=f"Payload Mass vs Launch Success for {selected_site}" if selected_site != 'ALL' else "Payload Mass vs Launch Success for All Sites",
        labels={'class': 'Success (1 = Success, 0 = Failure)'}
    )
    return fig

if __name__ == "__main__":
    app.run()
