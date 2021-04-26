import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import datetime
import math

recent=pd.read_csv('datasets/recent.csv')
fig1 = px.bar(recent, x='split', y='moving_time',range_y=[3,7],template="ggplot2",
        labels={
            'split':'Split',
            'moving_time':'Split time (mins)',
        }
    )

fig1.layout.plot_bgcolor = 'rgb(255, 255, 255)'
fig1.layout.paper_bgcolor = 'rgb(255, 255, 255, 0.5)'

df2=pd.read_csv('datasets/recent_activities.csv')
fig2 = px.scatter(df2, x="calories", y="moving_time",log_x=True,color="exertion",size="distance",
labels={
                     "calories": "Calories burnt (kcal)",
                     "moving_time":"Time (mins)",
                     "exertion":"Exertion level",
                     "distance":"Distance(m)",
                 },
)

fig2.layout.paper_bgcolor = 'rgb(255, 255, 255, 0.5)'

recent_name=df2['name'][0]
dateformat=datetime.datetime.strptime(df2['start_date'][0], '%Y-%m-%dT%H:%M:%S%fZ')
dateformat=dateformat.strftime('%d %b %Y')
recent_dist=df2['distance'][0]
recent_time=df2['moving_time'][0]
recent_avg=df2['average_speed'][0]
recent_gear=df2['gear_name'][0]
recent_calorie=df2['calories'][0]

total_distance=round(df2['distance'].sum()/1000,2)
total_time=round(df2['moving_time'].sum()/60,2)
total_exertion=math.floor((df2['exertion'].mean()))
total_calories=round(df2['calories'].sum(),2)

avg_dist=round(total_distance/df2.shape[0],2)
avg_time=round((total_time/df2.shape[0])*60,2)
avg_speed=round(df2['average_speed'].mean(),2)
max_dist=df2['distance'].max()
maxdistindex=df2.distance.idxmax()
max_name=df2.iloc[maxdistindex][4]


fig3 = px.scatter(df2, x=[10,9,8,7,6,5,4,3,2,1], y='distance',hover_name="name",
                    labels={
                        'distance':'Distance Covered (m)',
                        'x':'Recent Activities',
                    }
                )
fig3.update_traces(
                            mode='lines+markers',
                            marker=dict(size=12,color='DarkBlue',
                              line=dict(width=2,
                                        color='black')),
)

fig3.layout.paper_bgcolor = 'rgb(255, 255, 255, 0.5)'


layout=html.Div([   
    html.Nav(
        children=[
            html.A("",className="logo",href='/home'),
            html.Div(['RUNALYZE'], className="app-title"),
            html.A('Performance Metrics',
            className="button1", href='/apps/performancemetrics'),
            html.A('Recent Activities',
            className="button2",style={'background-color': 'rgb(255, 255, 255, 0.5)'}),
            html.A('Gear Comparison',
            className="button3",href='/apps/gearcomparison'),
    ],
    className="NavBar",
    ),
    html.Div(className="Top"),
    html.Div([
        html.Div([
            html.Div('Most Recent Activity',className="graph-titles"),
            dcc.Graph(
                className="Graph",
                id='graph1',
                figure=fig1,
            ),
            html.Div('Calories and Exertion',className="graph-titles"),
            dcc.Graph(
                className="Graph",
                id='graph2',
                figure=fig2,
            ),
            html.Div('Distance Covered',className="graph-titles"),
            dcc.Graph(
                className="Graph",
                id='graph3',
                figure=fig3,
                style={'margin-bottom':'10px'},
            ),
        ],
        className="Leftbox-page3",
    ),
    html.Div([
        html.Div([
            html.Div(str(recent_name)+' ('+str(dateformat)+")",className="Graph-details",
                style={'padding-top': '10px',
                    'font-size': '25px',}
                ),
            html.Div('Distance - '+str(recent_dist)+' m',className="Graph-details"),
            html.Div('Time taken- '+str(recent_time)+' mins',className="Graph-details"),
            html.Div('Average speed- '+str(recent_avg)+' kmph',className="Graph-details"),
            html.Div('Calories Burnt- '+str(recent_calorie),className="Graph-details"),
            html.Div('Gear- '+str(recent_gear),className="Graph-details"),
        ],className="graph-1-box"),

        html.Div(className='graph-spacing'),
    
        html.Div([
            html.Div('Last 10 Activities',className="Graph-details",
                style={'padding-top': '20px',
                    'font-size': '25px'},
                ),
            html.Div('Total distance - '+str(total_distance)+' km',className="Graph-details"),
            html.Div('Total time- '+str(total_time)+' hrs',className="Graph-details"),
            html.Div('Calories burnt- '+str(total_calories)+' kcal',className="Graph-details"),
            html.Div('Average exertion- '+str(total_exertion)+'/10',className="Graph-details"),
        ],className="graph-1-box"),

        html.Div(className='graph-spacing'),
        
        html.Div([
            html.Div('Last 10 Activities',className="Graph-details",
                style={'padding-top': '20px',
                    'font-size': '25px',}
                ),
            html.Div('Average distance - '+str(avg_dist)+' km',className="Graph-details"),
            html.Div('Average time- '+str(avg_time)+' mins',className="Graph-details"),
            html.Div('Overall average speed- '+str(avg_speed)+' kmph',className="Graph-details"),
            html.Div('Maximum distance- '+str(max_dist)+' km ('+str(max_name)+')',className="Graph-details"),
            ],className="graph-1-box"),

        ],className="Rightbox-page3"),

    ],className="container"),
    
    html.Div(className="Bottom"),
],
className="BG",
)
