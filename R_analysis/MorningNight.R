#see if countries where a morning time is the running peak show performance differences from countries where an evening time is the running peak

country = c("Sweden", "Denmark", "Mexico", "Brazil", "Indonesia", "Malaysia", "Switzerland", "Austria")
region = rep (c("Scandinavia", "LatinAmerica", "SoutheastAsia", "CentralEurope"), each = 2)
type = rep(c("morning", "evening"), 4)

working_directory = "D:/data/running"
full_file = "full.csv"
full = fread(full_file)

median_ascent = lapply(country, function(x) get_median(x, "ascent.x", full))
median_ascent = as.numeric(median_ascent)
median_duration = lapply(country, function(x) get_median(x, "duration.x", full))
median_duration = as.numeric(median_duration)/60

morning_night_dt = data.table(country = country, region = region, type = type, median_ascent = median_ascent, median_duration = median_duration)
working_directory = "D:/data/running"
morning_night_file = "morning_night.csv"
setwd(working_directory)
write.csv(morning_night_dt, morning_night_file)


p = ggplot(morning_night_dt, aes(x = median_ascent, y = median_duration)) + geom_point(guide=FALSE, aes(color=type, shape=region, size = 3000)) + 
  geom_text(size = 7, aes(label=country, color = type), , hjust = 1, vjust = 1) + 
  xlim(25, 80) + ylim(20, 45) + theme(legend.text=element_text(size=18), axis.title = element_text(size=18)) +
  xlab("Median cumulative ascent (m)") + ylab("Median duration (minutes)")
p = p + theme(axis.text = element_text(size = 20))
p +  scale_color_brewer(palette="Set1")


#processing function
get_median <- function(country, name , df = full){
  print(country)
  rows = which(df$country==country)
  f = df[rows, name, with=FALSE]
  median(f[[name]], na.rm=TRUE)
}
