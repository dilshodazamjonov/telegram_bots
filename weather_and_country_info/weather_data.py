from datetime import datetime
from tempfile import template
import requests
from time import strftime

parametrs = {
    'appid': '', # your API id from the https://openweathermap.org/api
    'units': 'metric',
    'lang': 'eng'
}

def get_weather_country(city):
    parametrs['q'] = city

    try:
        weather = requests.get('http://api.openweathermap.org/data/2.5/forecast?', params=parametrs).json()
        city = weather['city']['name']
        timezone = weather['city']['timezone']
        sunrise = datetime.utcfromtimestamp(weather['city']['sunrise'] +
                                                timezone).strftime('%Y.%m.%d %H:%M:%S')
        sunset = datetime.utcfromtimestamp(weather['city']['sunset'] +
                                                timezone).strftime('%Y.%m.%d %H:%M:%S')
        degree = weather['list'][0]['main']['temp']
        description = weather['list'][0]['weather'][0]['description']
        wind_speed = weather['list'][0]['wind']['speed']
        return f'''City: {city}
Current Temperature: {degree} °C
Description: {description} 
Wind Speed: {wind_speed} kmph
Sunrise at: {sunrise} 
Sunset at: {sunset}
    '''
    except:
        return 'Wrong country! Try again'