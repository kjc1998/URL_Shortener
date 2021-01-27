import requests
import json
import urllib

#userid = post request (username & password)#

BASE = "http://127.0.0.1:5000/"
long_link = "https://www.google.com"

userID = (requests.post(BASE + "login/" +
                        "kaijie" + "/kaijie")).json()['userid']
print(userID)
short = requests.post(
    BASE+"details/"+userID+'/'+long_link)
shortened = short.json()['short_url']
print(shortened)
