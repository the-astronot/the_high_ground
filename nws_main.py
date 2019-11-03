"""
This script gets data from the National Weather Service and sends it to the database

Author: Max Marshall
Hack RPI 2019
"""
import firebase_admin
from firebase_admin import firestore
import requests
import time
from lxml import html


# Gets city data from firebase
def get_cities(city_ref):
    cities_data = []
    docs = city_ref.stream()

    for doc in docs:
        cities_data.append((doc.id, doc.to_dict()))
    return cities_data


# Scrapes national weather service for hazards containing the word flood
# Search is done by coordinates
def get_weather(city_data):
    for item in city_data[1]:
        if item == "Latitude":
            lat = city_data[1]["Latitude"]
        elif item == "Longitude":
            lon = city_data[1]["Longitude"]
        elif item == "Flood":
            flood = city_data[1]["Flood"]
    url = "https://forecast.weather.gov/MapClick.php?lat={}&lon={}".format(lat, lon)
    page = requests.get(url)
    tree = html.fromstring(page.content)

    warnings = (tree.xpath('//div[@class="headline-title"]/text()'))
    for warning in warnings:
        print("{} : {}".format(city_data[0], warning))
        if "Flood" in warning:
            flood = "True"
        else:
            flood = "False"

    if len(warnings) == 0:
        flood = "False"

    city_data[1]["Flood"] = flood
    new_city_data = city_data

    return new_city_data


# Sends updated data back to firebase
def send_data(c_data, database1):
    for item in c_data:
        new_data_ref = db.collection(u'{}'.format(database1)).document(u'{}'.format(item[0]))
        new_data = dict()
        for dict_item in item[1]:
            new_data[u'{}'.format(dict_item)] = u'{}'.format(item[1][dict_item])
        new_data_ref.set(new_data)


# Gets user data
def get_users(u_data):
    users_data = []
    docs = u_data.stream()

    for doc in docs:
        users_data.append((doc.id, doc.to_dict()))
    return users_data


# Determines whether or not a user should receive a warning
def get_user_data(u_data, c_data):
    cities = []
    for city in c_data:
        cities.append((city[0], city[1]["Latitude"], city[1]["Longitude"], city[1]["Flood"]))

    user = [u_data[0], u_data[1]["Latitude"], u_data[1]["Longitude"]]

    for city in cities:
        if float(city[1]) - .1 < float(user[1]) < float(city[1]) + .1:
            if float(city[2]) - .1 < float(user[2]) < float(city[2]) + .1:
                if city[3] == "True":
                    u_data[1]["Warning"] = "True"
                else:
                    u_data[1]["Warning"] = "False"

    return u_data


cities_data = []
new_cities_data = []
new_users_data = []
database = "flood alerts"
users = "users"


# Guard
if __name__ == '__main__':
    # Connecting to the Database
    cred = firebase_admin.credentials.Certificate("..\\the_high_ground\\keys\\"
                                                  "intricate-yew-257819-firebase-adminsdk-20d4l-42b875fcc5.json")
    firebase_admin.initialize_app(cred)
    db = firebase_admin.firestore.client()

    # Loop through getting city info, getting flood info for those cities, and updating the database
    while True:
        city_ref = db.collection(u'{}'.format(database))
        cities_data = get_cities(city_ref)
        for city_data in cities_data:
            new_city_data = get_weather(city_data)
            new_cities_data.append(new_city_data)
        send_data(new_cities_data, database)
        time.sleep(2.5)
        user_ref = db.collection(u'{}'.format(users))
        users_data = get_users(user_ref)
        for user_data in users_data:
            new_user_data = get_user_data(user_data, new_cities_data)
            new_users_data.append(new_user_data)
        send_data(new_users_data, users)
        time.sleep(2.5)
