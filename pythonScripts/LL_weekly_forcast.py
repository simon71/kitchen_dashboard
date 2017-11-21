import urllib.request
from bs4 import BeautifulSoup
import json
import re

def weather_img(conditions):
    return {
            'Clear Sky':'sun.png',
            'Sunny':'sun.png',
            'Sunny Intervals':'sunny_intervals.png',

            'Partly Cloudy':'light_cloud.png',
            'Light Cloud':'light_cloud.png',
            'Thick Cloud':'thick_cloud.png',
            'Grey Cloud':'light_cloud.png',
            'Mist':'fog.png',
            'Fog':'fog.png',

            'Thundery Shower':'heavy_thunder_showers.png',
            'Heavy Thunder':'heavy_thunder.png',
            'Drizzle':'light_rain.png',
            'Light Rain':'light_rain.png',
            'Light Rain Shower':'light_rain_showers.png',

            'Heavy Rain':'heavy_rain.png',
            'Heavy Rain Shower':'heavy_rain_showers.png',

            'Sleet':'sleet.png',
            'Light Snow':'light_snow.png',
            'Light Snow Shower':'light_snow_showers.png',
            'Light Snow Rain Showers':'light_snow_rain_showers.png',
            'Heavy Snow':'heavy_snow.png',
            'Heavy Hail':'heavy_hail.png',
        }.get(conditions, None)

def wind_direction(windDir):
    return{
            'Northerly':'wind/N.png',
            'North North Easterly':'wind/NE.png',
            'North East':'wind/NE.png',
            'North East Easterly':'wind/NE.png',
            'Easterly':'wind/E.png',
            'East South Easterly':'wind/SE.png',
            'South Easterly':'wind/SE.png',
            'South South Easterly':'wind/SE.png',
            'Southerly':'wind/S.png',
            'South South Westerly':'wind/SW.png',
            'South Westerly':'wind/SW.png',
            'Sount West Westerly':'wind/SW.png',
            'Westerly':'wind/W.png',
            'West North Westerly':'wind/NW.png',
            'North West':'wind/NW.png',
            'North North Westerly':'wind/NW.png',
            '':'wind/none.png'
        }.get(windDir, None)


url = "http://www.bbc.co.uk/weather/en/6296559/?day1"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, "html5lib")


weekWeather = soup.find('div', {'class':'daily-window'})

day = [x.text.strip() for x in weekWeather.findAll('div', {'class':'daily__day-header'})]

condition = [x["title"] for x in weekWeather.findAll('span', {'class':'weather-type-image weather-type-image-40'})]


max_temp = [x.text[:-2].strip() for x in weekWeather.findAll('span', {'class':'units-value temperature-value temperature-value-unit-c'})][::2]#select every other element from array

min_temp = [x.text[:-2].strip() for x in weekWeather.findAll('span', {'class':'units-value temperature-value temperature-value-unit-c'})][1::2]#selects every other element starting with first

windSpeed = [x.text[:-4] for x in weekWeather.findAll('span', {'class': 'units-value windspeed-value windspeed-value-unit-mph'})]

windDirT = [x.text for x in weekWeather.findAll('span', {'class':'description blq-hide'})]

windDir = ["".join([item[0] for item in x.text.split()])
 for x in weekWeather.select('span.description.blq-hide')]


wk = [0,1,2,3,4,5]

dCond = dict(zip(wk,condition))
dWind = dict(zip(wk,windDir))
wImg = {}
for wk in dCond:
    wImg[wk] = (weather_img(condition[wk]))

windImg={}
for wk in dWind:
    windImg[wk] = (wind_direction(windDirT[wk]))

wkForecast = {}
wks = [0,1,2,3]
for i in wks:
    wkForecast[i] = day[i], condition[i], max_temp[i], min_temp[i], windSpeed[i], windDir[i], wImg[i], windImg[i]

with open("./jsonData/ll_wkforecast.json", 'w') as outfile:
    json.dump(wkForecast, outfile, indent=4, sort_keys=True)
