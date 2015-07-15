Web scraping and data entry were accomplished in 5 distinct steps:

(1) part1.py: Query Endo API for a series of putative user ID's only some of which were true user ID's, as determined by which user ID's returned content. For each valid user ID, create a directory and store each month's activities per user in a JSON-containing file. Use Scrapy package. The API formatting and location were determined by examining AJAX calls from URL's of this format: 'https://www.endomondo.com/users/USER_ID/workouts?before=DATE_!&after=DATE_2' Endomondo is known to make user data public and display it in this format where users consent to public data.

(2) part2.py: Insert user data into MongoDB, with one document per user, synthesizing information from all files saved per user in step (1).

(3) part3.py: Query Endo API for additional information about each run made by each user. Not all users as identified in (1) performed any runs. Also not all runs indicated in (1) (which provides a short summary of each activity) showed additional information in (3). Create a second MongoDB collection, with each run included as a separate document.

(4) part4.py: Identify runs that include a latitude/longitude. Move this information to the top-level of the document for each run. Mark any runs that do not include latitude/longitude so they will not be repetitively searched.

(5) part5.py: One run at a time, reverse geocode the user's latitude/longitude to determine country in which run took place for a run that includes a latitude/longitude. Each time a country is determined, search all runs for latitude/longitude pairings within a reasonable distance of the point with a known country and assign those runs to the same country. You can adjust the latitude/longitude selectivity to suit. This minimizes calls to Google API (limited to 2500 requests per 24 hour period) without producing too many errors. It's not usually possible to geocode all entries needing country information in a 24 hour period, so this is maintained as a cron job that sends the administrator notice each time it has been run

Tools used:
MongoDB, Scrapy, Google reverse-geocoding API, Endomondo API


