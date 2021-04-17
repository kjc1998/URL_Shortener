import json
import requests
import urllib

USERNAME, PASSWORD = "cer0cifer", "Ckj1ckj1"
BASE = "https://spshurl.herokuapp.com/"
userID = (requests.post(BASE + "login/" + USERNAME + "/" + PASSWORD).json())['userid']
print(userID)

# url to be shortened or extracted
URL = "https://docs.katalon.com/katalon-studio/videos/create_basic_automation_test_case_katalon_studio.html"
postLink = BASE + "details/" + f"{userID}/" + URL

details = requests.post(postLink).json()
print(details)