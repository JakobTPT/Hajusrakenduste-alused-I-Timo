from datetime import datetime
import requests

headers = {"name": "name@example.com"}
response = requests.get("https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.437&lon=24.7536", headers = headers)

if response.status_code == 200:
    data = response.json()
    timeseries = data['properties']['timeseries']
    for entry in timeseries[:7]:
        utc_time = entry['time']
        utc = datetime.fromisoformat(utc_time.replace("Z", "+00:00"))
        time = utc.astimezone()
        temp = entry['data']['instant']['details']['air_temperature']
        print(f"kell {time.strftime('%H:%M')} on temperatuur: {temp} °C")
else:
    print("Error")