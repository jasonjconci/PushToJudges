# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 00:37:14 2017

@author: Jason
"""

import gather_keys_oauth2 as gather
import fitbit
import pandas as pd


# storing Fitbit app info external to this program

#print(display_name)

date='2018-08-15'
activities = ["calories", "steps", "distance", "floors", "elevation", "heart"]



def extract_daily_series(data, activity):
    timestamps = []
    values = []
    for datapoint in data:
        timestamps.append(datapoint["dateTime"])
        if(activity == "heart"):
            try:
                print(datapoint['value']['restingHeartRate'])
                values.append(datapoint['value']['restingHeartRate'])
            except:
                values.append(0)
        else:
            values.append(datapoint['value'])
    ser = pd.Series(values, index=timestamps)
    return ser


def collect_daily_activity_data(authd_client, date, activities, start_date, stop_date):
    activity_dictionary = {}
    for activity in activities:
        res = 'activities/' + activity
        daily = authd_client.time_series(res, base_date='today', period='1w')
        daily_data = daily['activities-' + activity]
        day_series = extract_daily_series(daily_data, activity)
        if(activity == 'heart'):
            activity += '_resting'
        activity_dictionary[activity] = day_series
    df = pd.DataFrame(activity_dictionary).reset_index().set_index('index')
    print(df)
    return df


def get_json(start_date, stop_date):
    # we've got the plain text id and secret in a text file for jerry rigging
    in_file = open(r"fitbit_client_keys.txt", "r")
    app_info = in_file.readlines()
    CLIENT_ID = app_info[0].strip()
    CLIENT_SECRET = app_info[1].strip()
    server = gather.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
    # using oauth2 to access
    print(CLIENT_ID)
    server.browser_authorize()
    # getting all of our tokens
    USER_ID = server.fitbit.client.session.token['user_id']
    ACCESS_TOKEN =  server.fitbit.client.session.token['access_token']
    REFRESH_TOKEN =  server.fitbit.client.session.token['refresh_token']
    # authd client is the actual Fitbit object we'll use to gather information
    authd_client = fitbit.Fitbit(USER_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
    # Here, we're having collect_daily_activity_data get each of our daily values (each listed in activities)
    # and putting them into JSON format so we can use it in our website
    df = collect_daily_activity_data(authd_client, date, activities, start_date, stop_date)
    json_format = df.to_json()
    return json_format
