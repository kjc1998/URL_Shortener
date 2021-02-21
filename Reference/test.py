import requests
import json
import urllib

#userid = post request (username & password)#

BASE = "https://spshurl.herokuapp.com/"
BASE_LOCAL = "http://127.0.0.1:5000/"
long_link = "https://www.youtube.com"

userID = (requests.post(BASE + "login/" +
                        "cer0cifer" + "/kaijie")).json()['userid']
short = requests.post(
    BASE + "details/"+userID+'/'+long_link)
shortened = short.json()
