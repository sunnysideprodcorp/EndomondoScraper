library(plyr)
library(dplyr)
library(data.table)

#READ IN AND FORMAT DATA

working_directory = "D:/data/running"
user_file = "users_all.csv"

#get individual user name
setwd(working_directory)
user_data = fread(user_file)
user_data[ , c("X", "X_id", "title") := NULL]

#now we'll add in individual info about runs
working_directory = "D:/data/running/runs_many_files"
setwd(working_directory)
names_to_delete = c("location_fail", "failed_url", "no_location", "row", "X")
run_info <- NULL
for(i in 0:29){
  print(i)
  file1 = paste0("runs_big_", i, ".csv")
  df1 = fread(file1)
  df1[ , eval(names_to_delete) :=NULL]
  run_info = rbind(run_info, df1)  
}


#and we'll add info about weather
working_directory = "D:/data/running/weather_data/dir_weather/dir_weather"
setwd(working_directory)
weather <- NULL
for(i in 0:36){
  file1 = paste0("weather_", i, ".csv")
  df1 = fread(file1)
  df1[ , c("V1", "_id") := NULL]
  weather = rbind(weather, df1)   
}


full = merge(x = run_info, y = user_data, by="endo", all.x = TRUE)
full = merge(x=full, y = weather, by="run", all.x=TRUE)
full[ , hour_start_per_run := as.numeric(substr(local_start_time.x, 12, 13))]


