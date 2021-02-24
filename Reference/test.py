import json
import urllib
import requests

#userid = post request (username & password)#

BASE = "https://spshurl.herokuapp.com/"
BASE_LOCAL = "http://127.0.0.1:5000/"
long_link = "https://www.google.com/"

userID = (requests.post(BASE + "login/" +
                        "cer0cifer" + "/Kj1chow!")).json()['userid']
print(userID)
'''short = requests.post(
    BASE + "details/"+userID+'/'+long_link)
shortened = short.json()
print("userID:", userID)
print("Values:", shortened)'''
