import urllib
import urllib.request
from bs4 import BeautifulSoup
import requests
from datetime import date


#build api url
t = str(date.today())
urla ="http://www.bbc.co.uk/weather/en/2644037/daily/"
urlb ="?day="

url = urla+t+urlb+"0"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, "html5lib")

#sun rise and sunset
# rise_set = soup.find('div', attrs={'class':'sunrise-sunset'})
# sunrise = rise_set.find('span', attrs={'class':'sunrise'}).text
# sunset = rise_set.find('span', attrs={'class':'sunset'}).text

#last updated
# a = soup.find('div', attrs={'class':'detail-container group'})
# last_update = a.p.text

#splits table up
table_head = soup.thead
table_main = soup.tbody
table_foot = soup.tfoot

#time
# thead_rows = table_head.findAll('tr')
# for h_tr in thead_rows:
#     h_td = h_tr.findAll('th')
#     time = [i.text.replace('\xa0hours', '').strip() for i in h_td]


#conditions
#conditions = [img['alt'] for img in table_main.select('img[alt]')]

#Temp
c = table_main.findAll('span', attrs={'class':'units-value temperature-value temperature-value-unit-c'})
c_temp = 
# f = table_main.find('span', attrs={'class':'units-value temperature-value temperature-value-unit-f'}).text

#wind
wind = table_main.find('span', attrs={'class':'units-value windspeed-value windspeed-value-unit-kph'}).text

print(c)
