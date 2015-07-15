import time
from pymongo import MongoClient
import json
from urllib.request import urlopen
import smtplib






#Each degree of latitude is approximately 69 miles
#Degrees of longitude vary from 69 miles to zero depending on latitude
LATITUDE_OFFSET = 4 # about 50 miles
LONGITUDE_OFFSET = 1 # also about 50 miles

#variables to customize
admin_email = "hello@example.com"
api_key = "api_key_goes_here" #ENTER YOUR API KEY


client = MongoClient()
db = client.endo
collection_runs = db.runs


def update_from_insert(latitude, longitude, country):
    '''this function assumes that any run within ~50 miles of a known latitude/longitude is in the same country as that latitude/longitude. So it updates records that have no recorded country and that happened within 50 miles of a record with a known country. Note also that for areas at +/- 180 degrees this method does not do a full search but does the naive adding/sutbracting, so parts of Russia/US/New Zealand/Pacific Island nations are not classified when they otherwise could be but this likely affects small number of records if at all and will not result in any misclassification'''
    #define box region of acceptable latitude/longitude pairs where country can be accurately guessed
    lat_l = latitude - LATITUDE_OFFSET
    lat_h = latitude + LATITUDE_OFFSET
    lon_l = longitude - LONGITUDE_OFFSET
    lon_h = longitude + LONGITUDE_OFFSET

    
    result_object = collection_runs.find_one({"run_info.latitude":{'$gte':lat_l, '$lte':lat_h}, "run_info.longitude":{'$gte':lon_l, '$lte':lon_h},  "country":{'$exists':False}}, {"run":True, "endo":True})
    cursor = collection_runs.find{"run_info.latitude":{'$gte':lat_l, '$lte':lat_h}, "run_info.longitude":{'$gte':lon_l, '$lte':lon_h},  "country":{'$exists':False}}, {"run":True, "endo":True})
    for result_object in cursor:
        collection_runs.update({"run":result_object["run"]}, {'$set':{"country":country}}) 
        

def insert_try(response, result_object, latitude, longitude):
'''Determine whether API call returned a country, if so insert it into the database and call update_from_insert
to look for other data points near this data point with a known country. If no country was returned,
mark the run as a failued reverse-geocoding query so that the query will not be repeated.
'''
   try:
      str_response = response.readall().decode('utf-8')
      jsonresponse = json.loads(str_response)
   except:
      insert_fail(result_object)
   else:
      results = jsonresponse.get("results", None)
      if results:
          #successful query
          address_components = results[0].get("address_components", None)
          country =  [data.get("long_name", None) for data in address_components if "country" in g.get("types", None)]
          collection_runs.update({"run":result_object["run"]}, {'$set':{"country":country[0]}}, upsert = False)
          update_from_insert(latitude, longitude, f[0])
      else:
          #failed query
         insert_fail(result_object)


def insert_fail(result_object):
'''sometimes the Google API does not identify the country of a latitude/longitude pair. In such cases
the failure is marked so the query is not repeated.'''
    collection_runs.update({"run":result_object["run"]}, {'$set':{"no_location":1}}, upsert = False)
    
#main event
#get only one result object at a time since we are updating many records for each return from API query
#if we retrieve many records at once, some may already be updated and waste an API query
#also we limit API query to 2500 per script-run since that is the geocoding API daily call imit
result_object = collection_runs.find_one({'$and':[{"no_location":{'$exists':False}}, {"run_info":{'$exists':True}}, {"country":{'$exists':False}}, {"latitude":{'$exists':True}} ] })
api_count = 1

while result_object and api_count < 2500:
   latitude = result_object['latitude']
   longitude = result_object['longitude']  
   url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=%s"%(latitude, longitude, api_key)
   response = urlopen(url)
   insert_try(response, result_object, latitude, longitude)
   result_object = collection_runs.find_one({'$and':[{"no_location":{'$exists':False}}, {"run_info":{'$exists':True}}, {"country":{'$exists':False}}, {'$or':[{"run_info.points":{'$exists':1}}, {"run_info.laps":{'$exists':1} }]} ] })
   api_count += 1
   time.sleep(1)


#sendemail indicating that script ran (since it will likely be run as a daily cron job 
#due to API call limit being much smaller than data set requirements
try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(admin_email, admin_email, "reverse-geocoding ran today")         
except SMTPException:
    pass

