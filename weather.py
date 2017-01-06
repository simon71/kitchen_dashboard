import json
import urllib.request
from bs4 import BeautifulSoup
from datetime import date
import time
import os

def hours(s):
    return [x.string+":00" for x in s.find('tr', class_="time").findAll("span", class_="hour")]

def conditions(s):
    return [x['title'] for x in s.find('tr', class_='weather-type').findAll('img')]

def fatal(s):
    sys.exit(s)

def day_img(condition):
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
        }.get(condition, None)

def night_img(condition):
    return {
            'Clear Sky':'night_clear_sky.png',

            'Partly Cloudy':'night_partly_cloudy.png',
            'Light Cloud':'night_partly_cloudy.png',
            'Thick Cloud':'night_thick_cloudy.png',
            'Mist':'fog.png',
            'Fog':'fog.png',

            'Heavy Thunder':'night_heavy_thunder.png',
            'Drizzle':'night_light_showers.png',
            'Light Rain':'night_light_showers.png',
            'Light Rain Shower':'night_light_showers.png',

            'Heavy Rain':'night_heavy_showers.png',
            'Heavy Rain Shower':'night_heavy_showers.png',

            'Sleet':'sleet.png',
            'Light Snow':'night_light_snow.png',
            'Light Snow Shower':'night_light_snow.png',
            'Light Snow Rain Showers':'night_snow_rain_showers.png',
            'Heavy Snow':'night_heavy_snow.png',
            'Heavy Hail':'night_heavy_hail.png',
        }.get(condition, None)

url = "http://www.bbc.co.uk/weather/en/2644037/daily/" + date.today().strftime("%Y-%m-%d")
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, "html5lib")
#table = soup.find("table", {'class':'weather moving-window three-hourly-0 one-hourly-21'})

hrs = hours(soup)
condition = conditions(soup)
if len(hrs) != len(condition):
    fatal('Unable to display weather at this moment in time. Please check back later')

day_hrs = ["05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00"]

presentHour = time.strftime('%H')+':00'

# dictionary where the key is the hour, and the value is the weather condition
# at that time.
weather_cond = dict(zip(hrs, condition))
# dictionary where the key is the hour, and the value is the name of the image
# representng the weather condition

#########################
#temperature
#########################
temp = [x.contents[0] for x in soup.find('tr', {'class':'temperature'}).findAll('span', {'class': 'units-value temperature-value temperature-value-unit-c'})]
#dict of hour and temp
weather_temp = dict(zip(hrs, temp))

#########################
#humidity
#########################
humidity = [x.string.strip() for x in soup.find('tr', {'class': 'humidity'}).findAll('td', {'class':'value hours-1'})]
#dict hours and humidity
weather_humidity = dict(zip(hrs, humidity))

###########################
#wind speed
###########################
windS = [x.contents[0].strip() for x in soup.find('tr', {'class':'windspeed'}).findAll('span', {'class':'units-value windspeed-value windspeed-value-unit-mph'})]
weather_wind_speed = dict(zip(hrs, windS))

windD = [x.string for x in soup.find('tr', {'class':'wind-direction'}).findAll('abbr')]
weather_wind_direction = dict(zip(hrs, windD))

weather_img = {}
for h in weather_cond:
    if h in day_hrs:
        weather_img[h] = (day_img(weather_cond[h]))
    else:
        weather_img[h] = (night_img(weather_cond[h]))

for i in hrs:
    if i > presentHour:
        weather_data_post= {}
        weather_data_post[i] = weather_cond[i], weather_img[i], weather_temp[i], weather_humidity[i], weather_wind_speed[i], weather_wind_direction[i]

for i in hrs:
    if i < presentHour:
        weather_data_pre= {}
        weather_data_pre[i] = weather_cond[i], weather_img[i], weather_temp[i], weather_humidity[i], weather_wind_speed[i], weather_wind_direction[i]





#writes the json data to file
with open('weather_data_pre.json', 'w') as outfile:
    json.dump(weather_data_pre, outfile, indent=4, sort_keys=True)

with open('weather_data_post.json', 'w') as outfile:
    json.dump(weather_data_post, outfile, indent=4, sort_keys=True)


#returns the sun rise time from the BBC weather website
sun_rise = soup.find('div', {'class':'sunrise-sunset'}).find('span', {'class':'sunrise'}).text.strip()

#returns the sun set time from the BBC weather website
sun_set = soup.find('div', {'class':'sunrise-sunset'}).find('span', {'class':'sunset'}).text.strip()
