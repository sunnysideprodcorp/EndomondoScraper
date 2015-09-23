from pymongo import MongoClient
import csv

'''
Determine which runs include latitude/longitude information and move this information to highest document level for easy retrieval that is independent of 
whether time series of location per run is stored in 'laps' or 'points' field. Also mark runs that do not include any location information as such
so they are not searched more than once.
'''

client = MongoClient()
db = client.endo
collection_runs = db.runs

cursor = collection_runs.find({'$and':[{"latitude_fail":{'$exists':False}}, {"run_info":{'$exists':True}}, {"latitude":{'$exists':False}}, {'$or':[{"run_info.points":{'$exists':1}}, {"run_info.laps":{'$exists':1} }]}]}, no_cursor_timeout = True)

writer = csv.writer(open('lon_lat.csv', 'w'))

for result_object in cursor:

   latitude = 0
   longitude = 0

   #some documents contain a 'laps' field that often has a latitude/longitude included within an 'imperial' or 'metric' subdocument
   if(result_object["run_info"].get("laps", None)):
       if(result_object["run_info"].get("laps", None).get("metric", None)):
          location= result_object["run_info"].get("laps", None).get("metric", None)[0]
          latitude =  location.get("begin_latitude", None)
          longitude = location.get("begin_longitude", None)
   elif(result_object["run_info"].get("laps", None)):
       if(result_object["run_info"].get("laps", None).get("imperial", None)):
          location= result_object["run_info"].get("laps", None).get("imperial", None)[0]
          latitude =  location.get("begin_latitude", None)
          longitude = location.get("begin_longitude", None)

   #other documents have a 'points' field that includes subdocuments with latitude/longitide data
   elif(result_object["run_info"].get("points", None)):
      if(result_object["run_info"].get("points", None).get("points", None)):
         location= result_object["run_info"].get("points", None).get("points", None)[0]
         latitude =  location.get("latitude", None)
         longitude = location.get("longitude", None)
   
   #if we found a latitude, longitude pair, save at highest level of document
   #otherwise mark document as not containing a latitude, longitude pair so we do not check again
   if latitude and longitude:
      print("got this latitude and longitude %f and %f for run #%s"%(latitude, longitude, result_object["run"]))
      collection_runs.update({"run":result_object["run"]}, {'$set':{"latitude":latitude}, '$set':{"longitude":longitude}})
      writer.writerow([latitude, longitude])
   else:
      collection_runs.update({"run":result_object["run"]}, {'$set':{"latitude_fail":1}})


