from requests import get
from pprint import PrettyPrinter
import pyttsx3
engine = pyttsx3.init()

Base_URL = 'http://api.weatherapi.com/v1/current.json?key=5bba435e99704325b2f103928250607&q=London&aqi=yes'

printer = PrettyPrinter()

def get_weather():
    find = input('Enter the place: ')

    url = f'http://api.weatherapi.com/v1/current.json?key=5bba435e99704325b2f103928250607&q={find}&aqi=yes'
    engine.say(f'The entered place for weather resuls is: {find}')
    engine.runAndWait()

    try:
        response = get(url)
        response.raise_for_status()

        data = response.json()
        current = data.get('current', {})
        weather_info = {
            'temp_c': current.get('temp_c'),
            'wind_kph': current.get('wind_kph'),
            'humidity': current.get('humidity'),
            'heatindex_c': current.get('feelslike_c'),
            'dewpoint_c': current.get('dewpoint_c', 'N/A')  # 'dewpoint_c' may not be present
        }
        data = list(weather_info.items())
    except Exception as e:
        print('Something went wrong!',e)
        return

    printer.pprint(data)
    engine.say(data)
    engine.say(str(weather_info))
    engine.runAndWait()

get_weather()


