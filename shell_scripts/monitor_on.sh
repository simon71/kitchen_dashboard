#! /bin/bash

vcgencmd display_power 1
#sudo tvservice -p && fbset -depth 8 && fbset -debth 16

python3 home/simon/www/magic_mirror/pythonScripts/weather.py

python3 home/simon/www/magic_mirror/pythonScripts/daily_weather.py

exit
