import requests
import json
import urllib

#userid = post request (username & password)#

BASE = "https://spshurl.herokuapp.com/"
long_link = "https://www.youtube.com"

userID = (requests.post(BASE + "login/" +
                        "cer0cifer" + "/kaijie")).json()['userid']
print(userID)
'''short = requests.post(
    BASE+"details/"+userID+'/'+long_link)
shortened = short.json()['short_url']
print(shortened)'''
