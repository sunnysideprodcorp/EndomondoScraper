import time
import random
from pymongo import MongoClient
import json
import requests

#Databases info 
client = MongoClient()
db = client.endo
collection = db.users
collection_runs = db.runs


'''Now that we have a MongoDB collection of all individual runs, we return to the Endo API, where additional information
is sometimes available for each run. Sometimes additional info is not available, and if this is the case, we mark the failure of the API.
Where additional information is available, we delete irrelevant fields (non-meaningful polylines).
Of API calls that return additional information, some have a point-by-point time series called "laps" and some have a point-by-point time series called "points".
The former ("laps") can be in metric or imperial units, while the latter ("points") seems always to be returned in metric units.
There is no formal guide to the API, so these surmises may be incorrect but they are a best guess based on inspection of API returns.
'''
cursor = collection_runs.find({"run_info" : {'$exists':False}, "failed_url":{'$exists':False}}, no_cursor_timeout=True)
for result_object in cursor:
    user_string = result_object["endo"]
    user_workout = result_object["run"]
    timesleep = random.uniform(.1, 2)
    time.sleep(timesleep)
    UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0'
    url = 'https://www.endomondo.com/rest/v1/users/%s/workouts/%s'%(user_string, user_workout)
    r = requests.get(url, headers = {'User-Agent':UA})

    try:
        jsonobject = r.json()
        
        #if returned data includes "laps" parse these to dictionarys and remove polylines
        #retain information about which units are used as additional entry in dictionray
        if 'laps' in jsonobject and jsonobject['laps'] is not None:
            if 'imperial' in jsonobject['laps']:
                laps_array = jsonobject['laps']['imperial']
                type = 'imperial'
            if 'metric' in jsonobject['laps']:
                laps_array = jsonobject['laps']['metric']
                type = 'metric'
            if laps_array is not None:
                jsonobject['laps_correct'] = dict()
                jsonobject['laps_correct'][type] = list()
                for document in laps_array:
                    if document.__class__.__name__ == "dict":
                        document_dict = document
                    else:
                        document_dict = json.loads(document)
                    if 'small_encoded_polyline' in document_dict and document_dict['small_encoded_polyline'] is not None:
                        del document_dict['small_encoded_polyline']
                        document = document_dict
                        jsonobject['laps_correct'][type].append(document_dict)
                jsonobject['laps'] = jsonobject.pop('laps_correct')

        #if returned data includes "points" parse these to dictionarys and remove polylines
        if 'points' in jsonobject and jsonobject['points'] is not None:
            if 'points' in jsonobject['points']:
                points_array = jsonobject['points']['points']
                jsonobject['points_correct'] = dict()
                jsonobject['points_correct']['points'] = list()
                if points_array is not None:
                    for document in points_array:
                        if document.__class__.__name__ == "dict":
                            document_dict = document
                        else:
                            document_dict = json.loads(document)
                            if 'small_encoded_polyline' in document_dict and document_dict['small_encoded_polyline'] is not None:
                                del document_dict['small_encoded_polyline']
                                document = document_dict
                                jsonobject['points_correct']['points'].append(document_dict)
                jsonobject['points'] = jsonobject.pop('points_correct')

        if 'small_encoded_polyline' in jsonobject and jsonobject['small_encoded_polyline'] is not None:
            del jsonobject['small_encoded_polyline']           

    except ValueError as e:
        #Endo API failed to offer additional information about a run. We mark this to avoid requerying the API
        collection_runs.update({"run":user_workout}, {'$set':{"failed_url":1}}, upsert= False)
    else:
        #If Endo API provided additional information, we insert this in the MongoDB runs collection
        collection_runs.update({"run":user_workout}, {'$set':{"run_info":jsonobject}}, upsert= False)
