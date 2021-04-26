from numpy.lib.function_base import gradient
import requests
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
import os

def get():

    os.chdir(r'datasets')
    auth_url = "https://www.strava.com/oauth/token"

    #replace variables with values for your account
    payload = {
        'client_id': "",
        'client_secret': '',
        'refresh_token': '',
        'grant_type': "refresh_token",
        'f': 'json'
    }

    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']
    #print("Access Token = {}\n".format(access_token))
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    profile_url= "https://www.strava.com/api/v3/athlete"
    activities = requests.get(activites_url, headers=header, params=param).json()
    profile= requests.get(profile_url, headers=header, params=param).json()
    with open('activities.json', 'w') as json_file:
        json.dump(activities, json_file)
    with open('profile.json', 'w') as json_file:
        json.dump(profile, json_file)
    
    noofactivities=len(activities)
    for x in range(0,10):
        id=activities[x]["id"]
        activity_url = "https://www.strava.com/api/v3/activities/"+str(id)
        activity = requests.get(activity_url, headers=header, params=param).json()
        with open('activity%d.json'%x, 'w') as json_file:
            json.dump(activity, json_file)

    df=pd.read_json('activities.json')
    df.to_csv('activities.csv')

    df2=pd.read_csv('activities.csv')
    gears=df2['gear_id'].unique()
  
    for x in range(len(gears)):
        id=gears[x]
        gear_url = "https://www.strava.com/api/v3/gear/"+str(id)
        gear = requests.get(gear_url, headers=header, params=param).json()
        with open('gear%d.json'%x, 'w') as json_file:
            json.dump(gear, json_file)

    df=pd.read_csv('activities.csv',parse_dates=['start_date_local'])
    df['moving_time']=df['moving_time']/60
    df['average_speed']=df['average_speed']*3.6
    df['max_speed']=df['max_speed']*3.6
    df['year']=df['start_date_local'].apply(lambda x: x.year)
    df['month']=df['start_date_local'].apply(lambda x: x.month_name())


    gears=df['gear_id'].unique()    
    gear_name=[]
    gear_distance=[]
    for x in range(len(gears)):
        file=open('gear%d.json'%x)
        gear= json.load(file) 
        gear_name.append(gear["name"])
        gear_distance.append(gear["distance"])

    df1=pd.DataFrame({'Name':gear_name,'Distance':gear_distance})
    df1=df1.set_index(gears)
    df1['gear_id']=gears
    df1.to_csv('gear.csv')
    df['gear_name']=df['gear_id'].apply(lambda x: df1['Name'][x])
    df=df.round(2)
    df.to_csv('activities.csv')

    #recent activities
    columns=['distance', 'elapsed_time', 'elevation_difference', 'moving_time',
    'split', 'average_speed', 'average_grade_adjusted_speed', 'pace_zone']
    splits=pd.DataFrame(columns=columns)
    calorie=[]
    exertion=[]
    for x in range(0,10):
        file=open('activity%d.json'%x)
        activity= json.load(file) 
        calorie.append(activity["calories"])
        exertion.append(activity["perceived_exertion"])
        activity_splits = pd.DataFrame(activity['splits_metric']) 
        splits = pd.concat([splits, activity_splits])


    splits = splits[(splits.distance > 950) & (splits.distance < 1050)]

    splits['average_speed']=splits['average_speed']*3.6
    splits['moving_time']=splits['moving_time']/60
    splits.round(2)
    splits.to_csv('splits.csv')

    df2=df.head(10)
    df2['calories']=calorie
    df2['exertion']=exertion
    df2.to_csv('recent_activities.csv')

    file=open('activity0.json')
    activity= json.load(file)
    z=activity["splits_metric"]
    df3=pd.DataFrame(z)
    df3['moving_time']=df3['moving_time']/60
    df3['average_speed']=df3['average_speed']*3.6
    df3=df3.round(2)
    df3.to_csv('recent.csv')

    df=pd.read_csv('activities.csv')
    months=pd.DataFrame(df.month.value_counts(),columns=['month','Runs'])
    months=months.reset_index()
    months.columns = ['month', 'runs','a']
    del months['a']
    index=months.shape[0]
    distance=[]
    for y in range(index):
        x=df.loc[(df['distance']>0) & (df['month'] == months['month'][y])].distance.sum()
        distance.append(x)
    months['distance']=distance
    months['distance']=months['distance']/1000
    months=months.round(2)
    months.to_csv('months.csv')

get()