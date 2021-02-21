# URL_Shortener

# API

Provides a simpler means of adding or inspecting a given URL through flask framework

How it works:
1) Must first have a registered account through the webpage.
2) Set up a BASE_URL variable that links to "https://spshurl.herokuapp.com/".
3) Obtain individual specific userID in JSON format via request method as given in the example below:
    request.post(BASE + "login/" + "{{ username }}/" + "{{ password }}")
4) Run another post request to either add or obtain information related to a given URL:
    request.post(BASE + "details/" + "{{ userID }}/" + "{{ URL }}")
   which should return a JSON serialised dictionary with all relevant details
# WebPage

Heroku WebPage: https://spshurl.herokuapp.com/

# Author

Kai Jie Chow - Project Lead

Daniel Goh - Backend Designer

Ben Wo Yew - Data Analytics

Jeremy Lee - Frontend Designer
