import urllib.request
from bs4 import BeautifulSoup

url = "http://www.bbc.co.uk/weather/en/2644037/?day1"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, "html5lib")

weekWeather = soup.find('div', {'class':'daily-window'})

day = [x.text.strip() for x in weekWeather.findAll('div', {'class':'daily__day-header'})]

condition = [x["title"] for x in weekWeather.findAll('span', {'class':'weather-type-image weather-type-image-40'})]

max_temp = [x.text.strip() for x in weekWeather.findAll('span', {'class':'max-temp max-temp-value'})]

a = weekWeather.findAll('span', {'class':'max-temp max-temp-value'})
for match in soup.findAll('span'):
    match.unwrap()
print(a)
