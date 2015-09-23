Once you've scraped this data you can see what time people go running in different countries, as shown in this [interactive histogram](http://www.sunnysideworks.nyc/Simply-Run/blog1#histcontainer), or in a static image as below:

![Nordic countries' running start times](https://github.com/sunnysideprodcorp/EndomondoScraper/blob/master/images/nordic.png)
![Baltic countries' running start times](https://github.com/sunnysideprodcorp/EndomondoScraper/blob/master/images/baltic.png)

The images all came from around 150,000 run records, each of which looked something like the ones below:



A rough idea of the geographic distribution of EndoMondo users sampled can be gleaned from a plot of all runs documented in the data set:

![World map showing run locations](https://github.com/sunnysideprodcorp/EndomondoScraper/blob/master/images/world.png)


More details

This project was undertaken to see whether there are country-specific patterns to how people run, as far as could be ascertained by sampling publicly available data recorded via the EndomMondo running app between January and June of 2015. The data was scraped in two parts, first query the EndoMondo API to determined valid user IDs and then scraping the exercise history of those valid IDs. The IDs were discovered from a full sampling of a randomly selected set of 100,000 contiguous possible ID numbers. No trends were found in geographic distribution for these ID numbers, suggesting that this should constitute a fair geographic sampling of the users.

Within the user histories, geographic coordinates were provided for each round of exercise, but no named information about geographic location was provided. For each user, the Google reverse geocoding API was called to determine which country a user had exercised in once, with the assumption being that this could be a proxy for the user's country of residence.

