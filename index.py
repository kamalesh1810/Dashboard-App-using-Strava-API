import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from app import app
from app import server
from apps import PerformanceMetrics,GearComparison,RecentActivities
from dash.dependencies import Input, Output
import json
import datetime


app.layout=html.Div([ 
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content',children=[]),
    ])

def home():
    df=pd.read_csv('datasets/activities.csv')
    file=open('datasets/profile.json')
    profile= json.load(file)
    dateformat=datetime.datetime.strptime(profile['created_at'], '%Y-%m-%dT%H:%M:%S%fZ')
    dateformat=dateformat.strftime('%d %b %Y')
    username=profile['username']
    name=profile['firstname']+" "+profile['lastname']
    total_distance=round(df.distance.sum()/1000,2)
    dp=profile['profile']
    country=profile['country']

    layout= html.Div([
    html.Nav(
        children=[
            html.A(href='/home',className="logo"),
            html.Div(['RUNALYZE'], className="app-title"),
            html.A('Performance Metrics',
            className="button1",href='/apps/performancemetrics'),
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
                html.Img(src=dp,className='DP'),
                html.Div([
                html.Div('Athlete Details',className="Header"),
                html.Div('Name - '+name,className="Para"),
                html.Div('Username - '+username,className="Para"),
                html.Div('Country- '+country,className="Para"),
                html.Div('Joined - '+str(dateformat),className="Para"),
                html.Div('Total Activities - '+str(df.shape[0]),className="Para"),
                html.Div('Total Distance - '+str(total_distance)+' kms',className="Para"),
                ]
                    ,className='athlete-details-box',
                ),
                html.Div(' ',className="spacing-box"),
            ]
                ,className='Leftbox'),
            html.Div([
                html.Div('Welcome to Runalyze',className="Welcome"),
                html.Div('Dashboard for Strava Runners',className="WelcomeText")
            ]
                ,className='Rightbox'),
        ],
            className="container"),
    html.Div(className="Bottom"),
    ],
    className="BG"
    ) 

    return layout

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/performancemetrics':
        return PerformanceMetrics.layout
    if pathname == '/apps/recentactivities':
        return RecentActivities.layout
    if pathname == '/apps/gearcomparison':
        return GearComparison.layout
    else:
        return home()

if __name__== '__main__':
    app.run_server(debug=True)