import requests
import json
import urllib

#userid = post request (username & password)#

BASE = "http://127.0.0.1:5000/"
long_link = "https://www.youtube.com"

userID = (requests.post(BASE + "login/" +
                        "danielgay" + "/daniel")).json()['userid']
print(userID)
short = requests.post(
    BASE+"details/"+userID+'/'+long_link)
shortened = short.json()['short_url']
print(shortened)
