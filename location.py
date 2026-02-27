import requests
import json

def get_ip_geolocation():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()

        if 'loc' in data:
            lat_long = data['loc'].split(',')
            latitude = float(lat_long[0])
            longitude = float(lat_long[1])
            city = data.get('city', 'Unknown')
            country = data.get('country', 'Unknown')

            print("Your IP Address:", data.get('ip'))
            print("Location:", city, country)
            print("Coordinates: (Lat:", latitude, "Lng:", longitude, ")")
            return latitude, longitude, city, country
        else:
            print("Location data not available.")
            return None, None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP location: {e}")
        return None, None, None, None

def get_longitute():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()

        if 'loc' in data:
            lat_long = data['loc'].split(',')
            longitude = float(lat_long[1])
            return longitude
        else:
            print("Location data not available.")
            return None, None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP location: {e}")
        return None, None, None, None

def get_latitute():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()

        if 'loc' in data:
            lat_long = data['loc'].split(',')
            latitude = float(lat_long[0])
            return latitude
        else:
            print("Location data not available.")
            return None, None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP location: {e}")
        return None, None, None, None


print(get_ip_geolocation())
