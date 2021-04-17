import json
import requests

BASE = "https://spshurl.herokuapp.com/"

# username and password
USERNAME, PASSWORD = '''{ username }''' , '''{ password }'''
loginLink = BASE + "login/" + f"{USERNAME}/" + PASSWORD

# retrieve userID
userID = (requests.post().json())['userid']

# url to be shortened or extracted
URL = '''{ original url }'''
postLink = BASE + "details/" + f"{userID}/" + URL

# retrieve details relating to given link/ shorten link if new in database (json format)
details = requests.post(postLink).json()

