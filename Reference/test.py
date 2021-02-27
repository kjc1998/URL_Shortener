import json
import requests

BASE = "http://127.0.0.1:5000/"
userID = requests.post(BASE + "login/" + "jeremyleejr/" + "Jlee1998$")
print(userID.json())
