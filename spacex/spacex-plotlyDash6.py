import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

space_df=pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')
#print(space_df.columns)
app=dash.Dash(__name__)

app.layout=html.Div(children=[
    html.H1('Space X Launch Records Dashboard', 
    style={'textAlign': 'center', 'color': '#503D36', 'font-size': 26}),
    #Add Drop-down to select Input Launch Site
    html.Div([
        html.H3(
        'Select Launch Site:',
        style={'height':'35px', 'font-size': 30}
        ),
        dcc.Dropdown(
           options=[{'label': 'All Sites', 'value': 'All Sites'}] +
            [{'label': site, 'value': site} for site in space_df['Launch Site'].unique()],
            value='All Sites', 
            id='launchsite',
        )
    ]),

    dcc.Graph(id='pie-plot'),
    
   #Add range slider to select payload 
   
    html.Div([
        html.H3(
            'Select Payload Range',
            style={'height':'35px', 'font-size': 30}
        ),
        dcc.RangeSlider
        (
            id='payloadslider',
            min=space_df['Payload Mass (kg)'].min(),
           max=space_df['Payload Mass (kg)'].max(),
            step=500,
            value=[space_df['Payload Mass (kg)'].min(),space_df['Payload Mass (kg)'].max()],
            marks={i: int(i) for i in range (int(space_df['Payload Mass (kg)'].min()),int(space_df['Payload Mass (kg)'].max())+1)},
        )
]),

dcc.Graph(id='scatter-plot')   
])


#Add a call back function
    
# add pie chart to update to based on selected site dropdown
@app.callback(
    Output(component_id='pie-plot',component_property='figure',),
    Input(component_id='launchsite',component_property='value')
)
def update_pie(selected_site):
    if selected_site=='All Sites':
        site_success_counts = space_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(site_success_counts, values='class', names='Launch Site', 
                     title='Total Success Launches By Site')
    else:
        site_df = space_df[space_df['Launch Site'] == selected_site]
        fig = px.pie(site_df, names='class', title=f'Total Success Launches for {selected_site}')
    return fig



#Add callback to give scatter chart on the payload
@app.callback(
    Output(component_id='scatter-plot', component_property='figure'),
    [
        Input(component_id='payloadslider', component_property='value'),
        Input(component_id='launchsite', component_property='value')
    ]
)

def update_scatter(payload,selected_site):
    low,high=payload
    payload_df=space_df[(space_df['Payload Mass (kg)']>=low)&(space_df['Payload Mass (kg)']<=high)]
    if selected_site != 'All Sites':
        sele_site_df=payload_df[payload_df['Launch Site']==selected_site]
    else:
        sele_site_df=payload_df
    fig=px.scatter(
    sele_site_df,
    x='Payload Mass (kg)',y='class',
    title=f'Payload vs. Outcome for {selected_site} (Payload Range: {low}-{high})',
    color='class'
   )
    return fig

if __name__=='__main__':
    app.run_server()
