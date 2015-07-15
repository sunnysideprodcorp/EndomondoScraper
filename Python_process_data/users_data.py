import os
import pymongo
from pymongo import MongoClient
import pandas as pd


'''Here we retrieve all relevant data for users who run, minimally process the data, and save it to a csv for easy trieval'''


client = MongoClient()
db = client.endo
collection = db.users
collection_runs = db.runs

#update these values 
limit = 200000 #choose your limit

from_db = db.users.aggregate([{'$project':{"endo":True, "activityArray.local_start_time":True,  "activityArray.distance":True,  "activityArray.duration":True,  "activityArray.speed_avg":True, "activityArray.altitude_max":True, "activityArray.sport":True,  "activityArray.altitude_min":True,  "activityArray.speed_max":True,  "activityArray.ascent":True,  "activityArray.descent":True,  "activityArray.title":True, "lengthArray":{'$size':"$activityArray"}}}, {'$limit':limit}])
df = pd.DataFrame(from_db)
names_list = ['sport', 'local_start_time', 'distance', 'duration', 'speed_avg', 'altitude_max', 'altitude_min', 'speed_max', 'ascent', 'descent', 'title']

'''for each of the values of interest, as definied in names_list, we determine whether that info is available for each document
in the activityArray. If it's available, we record the value, if not we record -999 as indicating a missing value
all these arrays must match, so we must have a placeholder missing value (-999) to keep arrays aligned
for example we want the local_start_time and distance arrays to match in length and order so we can easily retrieve all values for a given activity
depending on which index we choose. all arrays should contain data for the same activity (same day, same activity, same person) per index'''
for name in names_list:
    total_list = []
    for activity in df['activityArray']:
        if len(activity) > 0:
            #we record the value or a missing data value of -999 for each entry in the relevant array
            entry_value = [A[name] if A.get(name) else -999  for A in activity]
        else:
            #this only if activityArray is empty
            entry_value = []
        total_list.append(entry_value)
    df.loc[:, name] = total_list


total_list = []
for activity in df['sport']:
    #a value of 1 indicates running, other values correlate to other activities (artifactor of Endomondo API)
    num_runs = sum([1 if A is 1 else 0 for A in activity])
    total_list.append(num_runs)
df.loc[:,'num_runs'] = total_list

df.loc[:, 'percent_runs'] = df.loc[:, 'num_runs']/df.loc[:, 'lengthArray']
del df['activityArray']

#only include users who show at least one run among their activities
df = df[df.num_runs>0]

#save to csv for easy portability/not redoing initial data processing work
df.to_csv("users_all.csv")



