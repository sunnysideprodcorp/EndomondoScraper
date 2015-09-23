library(ggmap)
library(rworldmap)
library(ggplot2)

working_directory = "D:/data/MyProjects/EndoMondoScraping/"
setwd(working_directory)
lat_lon_file = "lon_lat.csv"
lat_lon = fread(lat_lon_file)
setnames(lat_lon, c("latitude", "longitude"))

#draw a world map in outline
newmap <- getMap(resolution = "low")
plot(newmap,  asp=1)
points(lat_lon$longitude, lat_lon$latitude, col="red", cex = .05)

#draw a map of Europe with Google API to get better details from higher user density area
newmap <- get_map(location = 'Europe', zoom = 4)
mappoints = ggmap(newmap) + geom_point(aes(x = longitude, y = latitude), size =5, color="red"), data = lat_lon)
mappoints

