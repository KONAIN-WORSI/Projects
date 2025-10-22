from geopy.geocoders import Nominatim
import time

for attempt in range(3):
        try:
            geolocator = Nominatim(user_agent="geo_app")
            location = geolocator.geocode("Itahari", country_codes='np')
            if location:
                print("Address:", location.address)
                print("Coordinates:", location.latitude, location.longitude)
            else:
                print("Location not found.")
            break
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(1)
   
