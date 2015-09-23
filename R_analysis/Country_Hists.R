library(ggplot2)

#load/reload data
working_directory="D:/data/running"
setwd(working_directory)
ordered_tally = fread("country_tally.csv")
country_hours = fread("country_hours.csv")


#for plotting purposes
x = list(baltic_countries, slavic_countries, soviet_countries, germanic_countries, latin_countries, nordic_countries,
         anglo_countries, asian_countries, spanish_countries, portugese_countries, middleeastern_countries,
         african_countries, oceania_countries,  morning, evening, unique(country_hours$countries) )
m = lapply(x, function(x) make_country_plot(x, country_hours))


#get all hists to save to csv
hists = lapply(sort(unique(country_hours$country)), function(x) get_hist_per_country(x, country_hours ) )
hists_df = data.frame(hists)
colnames(hists_df) = sort(unique(country_hours$country))
write.csv(hists_df[, as.character(sort(ordered_tally$country[ordered_tally$user_count>50], decreasing=FALSE))], "country_hists.csv")


#get all hists to save to csv
#hists = lapply(sort(unique(country_hours$country)), function(x) get_hist_per_country_dt(x, country_hours ) )
#hists_dt = data.table(lapply(hists, cbind))
#colnames(hists_dt) = sort(unique(country_hours$country))
#write.csv(hists_df[, as.character(sort(ordered_tally$country[ordered_tally$user_count>50], decreasing=FALSE))], "country_hists.csv")




#countries to look at
baltic_countries = c( "Lithuania","Latvia","Estonia")
slavic_countries = c("Poland", "Czech Republic", "Russia")
soviet_countries = c("Poland","Lithuania",  "Latvia", "Czech Republic", "Estonia", "Russia"  )
latin_countries = c("Spain", "France", "Italy")
germanic_countries = c( "Netherlands", "Germany",  "Austria", "Belgium", "Switzerland")
nordic_countries = c("Denmark", "Norway", "Sweden", "Finland")
anglo_countries = c("United Kingdom", "United States", "South Africa", "Australia", "Ireland")
asian_countries = c( "Thailand", "India","Taiwan", "Indonesia", "Malaysia", "China", "Hong Kong")
portugese_countries = c("Brazil", "Portugal")
middleeastern_countries = c("Israel")
african_countries = c("South Africa")
oceania_countries = c("Australia")
spanish_countries = c( "Spain","Argentina", "Mexico",  "Chile")
morning = c("Sweden", "Mexico", "Indonesia", "Switzerland")
evening = c("Denmark", "Brazil", "Malaysia", "Austria")




#functions to prepare plots and data
get_hist_per_country = function(country, df){
  hours = df$hours[which(df$country==country)]
  h = hist(hours, breaks = c(0:25), freq=FALSE)
  h$density
}

get_hist_per_country_dt = function(country, df){
  hours = df$hours[df$country==country]
  h = hist(hours, breaks = c(0:25), freq=FALSE)
  h$density
}

make_country_plot<-function(user_countries, country_hours_pre)
{
  country_hours = country_hours_pre[which(country_hours_pre$country %in% user_countries) ,]
  country_hours$country = factor(country_hours$country, levels = c(user_countries))
  p = ggplot(data=country_hours, aes(x=hours, color=country))
  p = p + geom_density(size = 3, aes(color=country), adjust=1)
  p = p + ggtitle(deparse(substitute(user_countries) )) + theme(plot.title = element_text(lineheight=.8, face="bold"))
  p = p +  scale_fill_discrete(breaks = user_countries) + theme(legend.position = "top")
  p = p + theme(axis.title.y = element_text(hjust=0.1, size = 20), axis.title.x = element_text(hjust=0.1, size = 20), legend.text = element_text(size=24))
  p = p + theme(axis.text = element_text(size = 20))
  p = p + xlab("Hour of the day") + ylab("Proportion of runs")
  }
