#!/bin/bash
PATH=/opt/someApp/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin


# declare the NOW varaiable
DATE=$(date +"%d-%m-%y")
TIME=$(date +"%T")

# Adds the date to each entry
echo -e "{\nDate: $DATE" >> ./speedtest.log

# Adds Time to  each entry
echo  "Time: $TIME" >> ./speedtest.log

#Runs the speedtest.cli package and logs the results into speedtest.log
speedtest-cli --simple >> ./speedtest.log

#Adds a blank line between each entry
echo "}" >> ./speedtest.log


