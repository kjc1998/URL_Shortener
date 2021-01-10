import requests
import json

#userid = post request (username & password)#

BASE = "http://127.0.0.1:5000/login/"

userID = requests.post(BASE + "kaijiechow" + "/qwe")
print(userID.json())
