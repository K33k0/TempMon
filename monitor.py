#from influxdb_client import InfluxDBClient, Point, WritePrecision
#from influxdb_client.client.write_api import SYNCHRONOUS
import os
import time
import Adafruit_DHT
import json
from urllib.request import urlopen
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

load_dotenv()

LATITUDE = os.environ.get('LATITUDE')
LONGITUDE = os.environ.get('LONGITUDE')
DHT_PIN = os.environ.get('DHT_PIN')
INFLUX_URL = os.environ.get('INFLUX_URL')
INFLUX_TOKEN = os.environ.get('INFLUX_TOKEN')
INFLUX_ORG = os.environ.get('INFLUX_ORG')
INFLUX_BUCKET = os.environ.get('INFLUX_BUCKET')

weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'


DHT_SENSOR = Adafruit_DHT.DHT22

humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)

open_meteo_result = json.load(urlopen(weather_url))
pred_temp = open_meteo_result['current_weather']['temperature']

with InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)
    data = [f"mem,host=host1 temperature_c={temperature}",
            f"mem,host=host1 pred_temperature_c={pred_temp}",
            f"mem,host=host1 humidity={humidity}"]
    write_api.write(INFLUX_BUCKET, INFLUX_ORG, data)


