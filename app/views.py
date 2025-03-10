from django.http import JsonResponse
from Adafruit_IO import Client, MQTTClient
from dotenv import load_dotenv
import os, pytz
from datetime import datetime

def format_datetime(dt_string):
    if dt_string.endswith('Z'):
        dt_string = dt_string.replace('Z', '+00:00')
        
        # Parse the ISO datetime string with timezone info
    dt = datetime.fromisoformat(dt_string)
    
    # Option 1: Convert to Vietnam timezone (UTC+7)
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    dt = dt.astimezone(vietnam_tz)

    return dt.strftime("%Y/%m/%d %H:%M:%S")


load_dotenv()

AIO_USERNAME = os.getenv('AIO_USERNAME')
AIO_KEY = os.getenv('AIO_KEY')

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.connect()
client.loop_background()

aio = Client(AIO_USERNAME, AIO_KEY)


def getData(request):
    temperature_feeds = aio.data('bbc-temperature')
    light_feeds = aio.data('bbc-light')
    humidity_feeds = aio.data('bbc-humidity')
    soil_feeds = aio.data('bbc-soil-moisture')
    temp_threshold = aio.data('bbc-temperature-threshold')
    soil_threshold = aio.data('bbc-soil-moisture-threshold')
    
    data = {
        'temperature': temperature_feeds[0].value,
        'light': light_feeds[0].value,
        'humidity': humidity_feeds[0].value,
        'soilMoisture': soil_feeds[0].value,
        'tempThreshold': temp_threshold[0].value,
        'soilThreshold': soil_threshold[0].value,
        'humidityHistory': [(x.value, format_datetime(x[1])) for x in humidity_feeds[0:30]],
        'temperatureHistory': [(x.value, format_datetime(x[1])) for x in temperature_feeds[0:30]],
        'lightHistory': [(x.value, format_datetime(x[1])) for x in light_feeds[0:30]],
        'soilMoistureHistory': [(x.value, format_datetime(x[1])) for x in soil_feeds[0:30]]
    }
    return JsonResponse(data)

def manualWatering(request):
    status = aio.data('bbc-manual-watering')
    client.publish('bbc-manual-watering', 1 - int(status[0].value))
    return JsonResponse({'status': 1 - int(status[0].value)})

def manualVentilate(request):
    status = aio.data('bbc-manual-temperature')
    client.publish('bbc-manual-temperature', 1 - int(status[0].value))
    return JsonResponse({'status': 1 - int(status[0].value)})