import json
import requests

BASE = "http://127.0.0.1:5000/"
userID = requests.post(BASE + "login/" + "cer0cifer/" + "Kj1chow!")
print(userID.json())
