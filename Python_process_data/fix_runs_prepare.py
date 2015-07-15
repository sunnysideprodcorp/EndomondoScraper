import os
import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy

client = MongoClient()
db = client.endo
collection = db.users
collection_runs = db.runs

counter = 0
limit = 3000

db_results = db.runs.find().limit(limit).skip(counter*limit)
df = pd.DataFrame(rb_results)

#these include the data we'd like per run, when it's available
#not all data is available for all runs
author_list = ['gender', 'weight', 'height']
weather_list = ['temperature', 'humidity', 'wind_speed', 'type']
name_list= [ 'duration', 'distance', 'include_in_stats', 'ascent', 'descent', 'calories', 'heart_rate', 'heart_rate_max', 'steps', 'notes', 'speed_avg', 'heart_rate_avg', 'speed_max', 'local_start_time']

all_names = []
all_names.extend(author_list)
all_names.extend(weather_list)
all_names.extend(name_list)


#default to NAN because we know in some cases data is not available
for name in all_names:
    df[name] = numpy.nan

#all the info except the run-id is stored inside the subdocument with field key 'run_info'
run_info = df['run_info']

#explicitly indicate the few df columns that are of string type
df[['local_start_time']] = df[['local_start_time']].astype(str)
df[['notes']] = df[['notes']].astype(str)

#as we go through each run, we extract values nested within subdocuments of subdocument to create
#more natural, flatter structure
for i in range(len(df['run'])):
    print("now at run %d"%i)
    run = run_info[i]
    if run.get('weather'):
        for name in weather_list:
            if run.get('weather').get(name):
                df.set_value(i, name, run['weather'][name])

    if run.get('author'):
        for name in author_list:
            if run.get('author').get(name):
                df.set_value(i, name, run['author'][name])

    for name in name_list:
        if run.get(name):
            if name is 'local_start_time' or name is 'notes':
                try:
                    df.set_value(i, name, str(run[name])[0:19])
                except:
                    pass       
            else:
                df.set_value(i, name, run[name])


#we don't need the large run_info column of df as we have extracted all values of interest
#to their own columns
del df['run_info']

#we save to one .csv
#in some cases this causes trouble, in which case break up results into multiple csv files
#by looping over df rows and printing small range to many separate csv fiels
df.to_csv("all_runs.csv", encoding='utf-8')
                
        


 

