import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


df=pd.read_csv('datasets/activities.csv')
fig = px.bar(df, x='gear_name', y='distance',template="plotly",
labels={
                     "distance": "Distance(m)",
                     "gear_name":"Gear name",
                 },
)
fig.layout.plot_bgcolor = 'rgb(255, 255, 255)'
fig.layout.paper_bgcolor = 'rgb(255, 255, 255, 0.5)'

df2=pd.read_csv('datasets/gear.csv')
gear_1_name=df2['Name'][0]
gear_1_distance=round(df2['Distance'][0]/1000,2)
gear_1_count=df[df.gear_name==gear_1_name].gear_name.count()
gear_1_average_speed=round(df[df.gear_name==gear_1_name].average_speed.mean(),2)
gear_1_max_speed=df[df.gear_name==gear_1_name].max_speed.max()

gear_2_name=df2['Name'][1]
gear_2_distance=round(df2['Distance'][1]/1000,2)
gear_2_count=df[df.gear_name==gear_2_name].gear_name.count()
gear_2_average_speed=round(df[df.gear_name==gear_2_name].average_speed.mean(),2)
gear_2_max_speed=df[df.gear_name==gear_2_name].max_speed.max()

layout=html.Div([   
    html.Nav(
        children=[
            html.A("",className="logo",href='/home'),
            html.Div(['RUNALYZE'], className="app-title"),
            html.A('Performance Metrics',
            className="button1", href='/apps/performancemetrics'),
            html.A('Recent Activities',href='/apps/recentactivities',className="button2",),
            html.A('Gear Comparison',
            className="button3",style={'background-color': 'rgb(255, 255, 255, 0.5)'}),
        ],
    className="NavBar",
    ),
    html.Div(className="Top"),
    html.Div([
        html.Div([
            html.Div('Gear Details',className="graph-titles"),
            dcc.Graph(
                className="Graph",
                id='graph1',
                figure=fig,
            ),
        ],
            className="Leftbox-page4",
        ),
        html.Div([
            html.Div([
            html.Div('Comparison',className="Graph-details",
                style={'padding-top': '10px',
                    'font-size': '27px',}
            ),
            html.Div(str(gear_1_name),className="Graph-details",
                style={'font-size': '20px', 'padding-top': '10px',}
            ),
            html.Div('Total Runs- '+str(gear_1_count),className="Graph-details"),
            html.Div('Distance Covered- '+str(gear_1_distance)+" km",className="Graph-details"),
            html.Div('Overall average speed- '+str(gear_1_average_speed)+' kmph',className="Graph-details"),
            html.Div('Max Speed Achieved- '+str(gear_1_max_speed)+' kmph',className="Graph-details"),
            html.Div(str(gear_2_name),className="Graph-details",
                style={'font-size': '20px','padding-top': '10px',}
            ),
            html.Div('Total Runs- '+str(gear_2_count),className="Graph-details"),
            html.Div('Distance Covered- '+str(gear_2_distance)+' km',className="Graph-details"),
            html.Div('Overall average speed- '+str(gear_2_average_speed)+' kmph',className="Graph-details"),
            html.Div('Max Speed Achieved- '+str(gear_2_max_speed)+' kmph',className="Graph-details"),
            ],className="graph-1-box",
            style={'height':'420px'}
            ),
        ],className="Rightbox-page4"),
        
    ],className="container",
        style={'height':'600px'}
    ),

    html.Div(className="Bottom"),
],
className="BG",
)
