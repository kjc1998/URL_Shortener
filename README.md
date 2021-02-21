# URL_Shortener

# WebPage

Heroku WebPage: https://spshurl.herokuapp.com/
A standard URL shortener webpage with additional GUI extensions for better and more convenient usage.

To gain access, user(s) should first create an account via the website's registration page.

Tabs | About
--- | --- 
Home | url shortening input & authors' backgrounds

# API

Provides a simpler means of adding or inspecting related contents on a given URL.

How it works:
1) Must first have a registered account at the hosted webpage.
2) Set up a BASE_URL variable that links to "https://spshurl.herokuapp.com/".
3) Obtain individual specific userID in JSON format via request method as given in the example below:
    request.post(BASE + "login/" + "{username}/" + "{password}")
4) Run another post request to either add or obtain information related to a given URL:
    request.post(BASE + "details/" + "{userID}/" + "{URL}")
   which should return a JSON serialised dictionary with all relevant details

# Author

Kai Jie Chow - Project Lead

Daniel Goh - Backend Designer

Ben Wo Yew - Data Analytics

Jeremy Lee - Frontend Designer
