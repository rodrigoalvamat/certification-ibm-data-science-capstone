# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe

spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
server = app.server

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites',
                                                     'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40',
                                                     'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40',
                                                     'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A',
                                                     'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E',
                                                     'value': 'VAFB SLC-4E'},
                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={
                                                    2500: '2500', 5000: '5000', 7500: '7500'},
                                                value=[0, 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(dropdown):
    if dropdown == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site',
                     title='Total Success Launchs By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == dropdown]
        filtered_df = filtered_df['class'].value_counts(
        ).sort_index(ascending=True)
        figure = px.pie(filtered_df, values='class', names=['Failure', 'Success'],
                        title='Total Success Launchs for site {}'.format(dropdown))
        return figure


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id="payload-slider", component_property="value"),
              Input(component_id='site-dropdown', component_property='value')])
def get_scatter_plot(slider, dropdown):
    filtered_df = spacex_df
    if dropdown != 'ALL':
        filtered_df = spacex_df[spacex_df['Launch Site'] == dropdown]

    higher = filtered_df['Payload Mass (kg)'] >= slider[0]
    lower = filtered_df['Payload Mass (kg)'] <= slider[1]
    filtered_df = filtered_df[higher & lower]

    figure = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                        color="Booster Version Category",
                        title='Launch Outcome by Payload Mass for site: {}'.format(dropdown))
    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)