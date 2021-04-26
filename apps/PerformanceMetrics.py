import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from plotly.graph_objs import *
import datetime

df = pd.read_csv('datasets/activities.csv')
fig = px.scatter(df, x="average_speed", y="distance",color="gear_name", hover_name="name", size="max_speed",
                 labels={
                     "distance": "Distance (m)",
                     "average_speed": "Average speed (kmph)",
                     "moving_time": "Total time (s)",
                     "gear_id":"Gear",
                     "max_speed":'Max speed (kmph)',
                     "gear_name":"Gear name",
                 },
                 )
fig.layout.paper_bgcolor = 'rgb(255, 255, 255, 0.5)'
totaldistance=round(df['distance'].sum()/1000,2)
avgspeed=round(df['average_speed'].mean(),2)
max_speed=round(df['max_speed'].max(),2)
maxspeedindex=df.max_speed.idxmax()
max_name=df.iloc[maxspeedindex][4]
distance_covered=round(df.distance.sum()/1000,2)


months=pd.read_csv('datasets/months.csv')
fig2 = px.pie(months, values='runs', names='month',template="ggplot2", hover_data=["distance"], labels={
                     'month': "Month",
                     'runs': "No of runs",
                     "distance":"Distance covered (kms)",
                 },)
fig2.layout.paper_bgcolor = 'rgb(255, 255, 255, 0.5)'

noofruns=months.runs.sum()
mostrunscount=months['runs'][0]
mostruns=months['month'][0]
mostdistance=months['distance'][0]


dates=[]
for x in range(0,df.shape[0]):
    dateformat=datetime.datetime.strptime(df['start_date'][x], '%Y-%m-%dT%H:%M:%SZ')
    dateformat=dateformat.strftime('%Y-%m-%d')
    dates.append(dateformat)
df2=pd.DataFrame({'date':dates})
df2.date=pd.to_datetime(df2.date)
df2['count']=df2.date.diff().dt.days.ne(-1).cumsum()
df['date']=df2['date']
df['count']=df2.groupby(['count']).cumcount()+1
index=df['count'].idxmax()
max_count=df['count'].max()
x=index-max_count+1
y=index+1
end=str(df['date'][x])
start=str(df['date'][y-1])
d=round(df.iloc[x:y].distance.sum()/1000,2)

fig6 = px.bar(df.iloc[x:y], y="distance", x="date", hover_name='name',
    labels={
        'distance':'Distance (m)',
        'date':'Date'
    }
)
fig6.layout.paper_bgcolor = 'rgb(255, 255, 255, 0.5)'
fig6.layout.plot_bgcolor = 'rgb(255, 255, 255)'


splits=pd.read_csv('datasets/splits.csv')
splits=splits.round(2)
fig3 = px.scatter(splits, x="elevation_difference", y="moving_time", color="split",
            trendline="ols", template="simple_white",
            labels={
                     'elevation_difference': "Elevation Difference",
                     'moving_time': "Moving time (mins)",
                 },
            )

split=splits['split'].unique()
avg_speeds=[]
moving_times=[]
for x in split:
    y=splits.loc[(splits['average_speed']!=0) & (splits['split']==x)]
    avg_speeds.append(y.average_speed.sum()/y.shape[0])
    moving_times.append(y.moving_time.sum()/y.shape[0])

fig3.layout.paper_bgcolor = 'rgb(255, 255, 255, 0.5)'

fig4 = px.scatter(df, x='moving_time', y='distance',hover_name="name",
            labels={
                     'moving_time': "Moving time (mins)",
                     "distance":"Distance covered (kms)",
                 },
                    )
fig4.update_traces(marker=dict(
            color='SkyBlue',
            size=20,
            line=dict(
                color='MediumPurple',
                width=2
            ),))

import math
total_moving_time=round(df['moving_time'].sum()/60,2)
average_moving_time=round(df['moving_time'].mean(),2)
average_distance=math.floor(df['distance'].mean()/1000)
dist=df['distance']
no_of_5k=len(list(x for x in dist if x>=5000.0 ))
no_of_10k=len(list(x for x in dist if x>=10000.0 ))


from sklearn import linear_model
x=df[['distance']]
y=df['moving_time']
regr=linear_model.LinearRegression()
regr.fit(x,y)
three_k=round(regr.predict([[3000]])[0],2)
five_k=round(regr.predict([[5000]])[0],2)
ten_k=round(regr.predict([[10000]])[0],2)

fig4.layout.paper_bgcolor = 'rgb(255, 255, 255, 0.5)'


layout=html.Div([   
    html.Nav(
        children=[
            html.A("",className="logo",href='/home'),
            html.Div(['RUNALYZE'], className="app-title"),
            html.A('Performance Metrics',
            className="button1",
            style={'background-color': 'rgb(255, 255, 255, 0.5)'}),
            html.A('Recent Activities',
            className="button2",href='/apps/recentactivities'),
            html.A('Gear Comparison',
            className="button3",href='/apps/gearcomparison'),
    ],
    className="NavBar",
    ),
    html.Div(className="Top"),
    html.Div([
        html.Div([
            html.Div('Monthly Activity',className="graph-titles"),
            dcc.Graph(
                className="Graph",
                id='graph1',
                figure=fig2,
            ),
            html.Div('Speed Comparison',className="graph-titles"),
            dcc.Graph(
                className="Graph",
                id='graph2',
                figure=fig,
            ),
            html.Div('Running Streak',className="graph-titles"),
            dcc.Graph(
                className="Graph",
                id='graph6',
                figure=fig6,
            ),
            html.Div('Split Analysis',className="graph-titles"),
            dcc.Graph(
                className="Graph",
                id='graph3',
                figure=fig3,
            ),
            html.Div('Distance Metrics',className="graph-titles"),
            dcc.Graph(
                className="Graph",
                id='graph4',
                figure=fig4,
                style={'margin-bottom': '30px'},
            ),
        ],
        className="Leftbox-page2",
    ),
    html.Div([
        html.Div([
            html.Div('Activities- {}'.format(df.loc[1]['year']),className="Graph-details",
                style={'padding-top': '10px',
                        'font-size': '25px',}
            ),
            html.Div('Total Runs this year - '+str(noofruns),className="Graph-details"),
            html.Div('Most Runs- '+str(mostruns),className="Graph-details"),
            html.Div('No of Runs- '+str(mostrunscount),className="Graph-details"),
            html.Div('Distance covered- '+str(mostdistance)+" km",className="Graph-details"),
            html.Div('Average distance per run- '+str(round(mostdistance/mostrunscount,2))+' km',className="Graph-details"),
        ],className="graph-1-box"),

        html.Div(className='graph-spacing'),

        html.Div([
            html.Div('Distance and Speed Analysis',className="Graph-details",
                style={'padding-top': '10px',
                        'font-size': '25px',}
                ),
            html.Div('Total Distance - '+str(totaldistance)+" km",className="Graph-details"),
            html.Div('Average speed overall- '+str(avgspeed)+" kmph",className="Graph-details"),
            html.Div('Max speed achieved- '+str(max_speed)+' kmph ('+str(max_name)+")",className="Graph-details"),
            html.Div('Average distance per run- '+str(round(distance_covered/noofruns,2))+' km',className="Graph-details"),
        ],className="graph-1-box"),

        html.Div(className='graph-spacing'),

        html.Div([
            html.Div('Longest Streak',className="Graph-details",
                style={'padding-top': '10px',
                        'font-size': '25px',}
                ),
            html.Div(str(max_count)+" days",className="Graph-details"),
            html.Div('From '+str(start[0:10])+" to "+str(end[0:10]),className="Graph-details"),
            html.Div('Total Distance- '+str(d)+' km',className="Graph-details"),
        ],className="graph-1-box",
        ),

        html.Div(className='graph-spacing',
        style={'height':'300px'}
        ),

        html.Div([
            html.Div('Split Details',className="Graph-details",
                style={'padding-top': '10px',
                        'font-size': '25px',}
                ),
            html.Div('Overall stats (split distance ~1000m)',className="Graph-details",
                style={ 'font-size': '20px',}
                ),
            html.Div('Best Split no- '+str(avg_speeds.index(max(avg_speeds))+1),className="Graph-details"),
            html.Div('Average moving time of best split- '+str(min(moving_times))+' mins',className="Graph-details"),
            html.Div('Average speed time of best split- '+str(max(avg_speeds))+' kmph',className="Graph-details"),
        ],className="graph-1-box"),

        html.Div(className='graph-spacing',
            style={'height':'220px'},
        ),

        html.Div([
            html.Div('Distance vs Time',className="Graph-details",
                style={'padding-top': '10px',
                    'font-size': '25px',}
            ),
            html.Div('Total moving time- '+str(total_moving_time)+' hrs',className="Graph-details"),
            html.Div('Average moving time- '+str(average_moving_time)+' mins',className="Graph-details"),
            html.Div("No of 5k's- "+str(no_of_5k),className="Graph-details"),
            html.Div('No of 10k''s- '+str(no_of_10k),className="Graph-details"),
            html.Div('Average Estimated Timings',className="Graph-details",
            style={'font-size': '25px'}),
            html.Div('3k- '+str(three_k)+' mins',className='Graph-details'),
            html.Div('5k- '+str(five_k)+' mins',className='Graph-details'),
            html.Div('10k- '+str(ten_k)+' mins',className='Graph-details'),
        ],className="graph-1-box",
            style={'height':'335px'},
        ),
    ],className="Rightbox-page2"),

    ],className="container",
    style={'height':'2650px'},
    ),

    html.Div(className="Bottom"),
    ],
className="BG",
)
