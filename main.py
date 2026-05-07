import requests
import datetime
from geopy.geocoders import Nominatim
import timezonefinder

geolocator = Nominatim(user_agent="Prayer MacOS Menu Bar", timeout=15)

def get_coordinates(city: str, country: str):
    '''
    :param city:
    :param country:
    :return: Longitude and Latitude coordinates given a city and a country
    '''
    location_query = f"{city}, {country}"

    try:
        location = geolocator.geocode(location_query)

        if location:
            return location.latitude, location.longitude
        else:
            return "Coordinates could not be found"
    except Exception as e:
        return f"We ran into an error: {e}"

def prayer_times(lat: float, long: float):
    timezone = timezonefinder.timezone_at(lat=lat, lng=long)
    url = f"https://ummahapi.com/api/prayer-times?lat={lat}&lng={long}&timezone={timezone}"
    response = requests.get(url)
    data = response.json()
    timings = data['data']['prayer_times']
    times = {}
    for prayer, time in timings.items():
        if prayer.lower() in ["fajr", "dhuhr", "asr", "maghrib", "isha"]:
            times[prayer.upper()] = [time, datetime.datetime.strptime(time, "%H:%M").time()]
    return times


def next_prayers(lat: float, long: float):
    time_now = datetime.datetime.now()
    today = datetime.date.today()
    times = prayer_times(lat, long)

    for prayer, time in times.items(): # prayer - the actual prayer, time - the time for that prayer, it's also a list
        dt_prayer = datetime.datetime.combine(today, time[1])
        if dt_prayer > time_now:
            return prayer, time[0]
    first = list(times.items())[0]
    return first[0], first[1][0]
