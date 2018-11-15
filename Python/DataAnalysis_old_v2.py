'''

University of California, Berkeley
CE 186 Design of Cyber-Physical Systems (Fall Term 2018)
Hanging Gardens: DataAnalysis.py
Group 6

DESCRIPTION

'''









# Import required modules
import requests
import json
import datetime
import pytz

def time_reset(time):
    hour = 7
    local_tz = pytz.timezone("America/Los_Angeles")
    delta = datetime.timedelta(1)
    if time.hour >= hour:
        time_7AM = local_tz.localize(datetime.datetime(time.year, time.month, time.day, hour, 0, 0), is_dst=None).astimezone(tz=pytz.utc)
    else:
        time_7AM = local_tz.localize(datetime.datetime(time.year, time.month, time.day, hour, 0, 0), is_dst=None).astimezone(tz=pytz.utc) - delta
    return time_7AM

def count_exposure(points_start):
    base = 'http://127.0.0.1:5000'
    header = {}

    daily_exp = 0

    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    query = {
        'points-start': points_start,
        'points-end': now
    }
    endpoint = '/networks/local/objects/light_sensor/streams/center_light/points'
    response = requests.request('GET', base + endpoint, params=query, headers=header, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200:
        print 'Error reading data'
    for dict in resp['points']:
        daily_exp += dict['value']

    print "Total daily light exposure:", daily_exp

    query = {
        'stream-name': 'Daily light exposure',
        'points-type': 'i' # 'i', 'f', or 's'
    }
    endpoint = '/networks/local/objects/light_sensor/streams/daily_exposure'
    response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120)
    resp = json.loads(response.text)
    if resp['stream-code'] == 201:
        print 'Create stream: ok'

    endpoint = '/networks/local/objects/light_sensor/streams/daily_exposure/points'
    query = {
        'points-value': daily_exp,
        'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    response = requests.request('POST', base + endpoint, params=query, headers=header, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200:
        print 'Update processed data points: error'
        print response.text

    return daily_exp

def roof_config():
    base = 'http://127.0.0.1:5000'
    header = {}

    light_thr = 12500

    query = {
        'points-limit': 1
    }

    # Left light sensor
    endpoint = '/networks/local/objects/light_sensor/streams/left_light/points'
    response = requests.request('GET', base + endpoint, params=query, headers=header, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200:
        print 'Error reading data'
    left_exp = resp['points'][0]['value']

    # Right light sensor
    endpoint = '/networks/local/objects/light_sensor/streams/right_light/points'
    response = requests.request('GET', base + endpoint, params=query, headers=header, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200:
        print 'Error reading data'
    right_exp = resp['points'][0]['value']

    # Use logic to determine roof position [left, right]
    left_roof = int(right_exp > left_exp and right_exp > light_thr)
    right_roof = int(left_exp > right_exp and left_exp > light_thr)
    if left_roof + right_roof == 0:
        center_roof = 1
    else:
        center_roof = 0

    return left_roof, right_roof, center_roof

def flushing(time_last_flush):
    base = 'http://127.0.0.1:5000'
    header = {}

    min_waterlvl = 50
    flush_interval = datetime.timedelta(hours=24)
    now = datetime.datetime.utcnow()
    delta = now - time_last_flush

    query = {
        'points-limit': 1
    }

    # Lower water level meter
    endpoint = '/networks/local/objects/water_level_meter/streams/lower_water_level/points'
    response = requests.request('GET', base + endpoint, params=query, headers=header, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200:
        print 'Error reading data'
    lower_waterlvl = resp['points'][0]['value']

    # upper water level meter
    endpoint = '/networks/local/objects/water_level_meter/streams/upper_water_level/points'
    response = requests.request('GET', base + endpoint, params=query, headers=header, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200:
        print 'Error reading data'
    upper_waterlvl = resp['points'][0]['value']

    # Use logic to determine if flushing is required
    if lower_waterlvl > min_waterlvl or upper_waterlvl > min_waterlvl or delta > flush_interval:
        flush = 1
        time_last_flush = now
    else:
        flush = 0

    return flush, time_last_flush

def LED_energy_usage(LED_set):
    base = 'http://127.0.0.1:5000'
    header = {}

    timeInterval = 0.25 # [hrs] -- time interval between readings
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    if LED_set == 1:
        LED_kW = 0.06 # [kW] -- wattage of LED
    else:
        LED_kW = 0

    query = {
        'object-name': 'Energy consumption'
    }
    endpoint = '/networks/local/objects/energy'
    response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120)
    resp = json.loads(response.text)
    if resp['object-code'] == 201:
        print 'Create object: ok'


    query = {
        'stream-name': 'Total energy consumption',
        'points-type': 'f' # 'i', 'f', or 's'
    }

    endpoint = '/networks/local/objects/energy/streams/total'
    response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120)
    resp = json.loads(response.text)
    if resp['stream-code'] == 201:
        print 'Create stream: ok'

    query = {
        'stream-name': 'LED',
        'points-type': 'f' # 'i', 'f', or 's'
    }

    endpoint = '/networks/local/objects/energy/streams/LED'
    response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120)
    resp = json.loads(response.text)
    if resp['stream-code'] == 201:
        print 'Create stream: ok'

    endpoint = '/networks/local/objects/energy/streams/LED/points'
    query = {
        'points-value': LED_kW*1000,
        'points-at': now
    }
    response = requests.request('POST', base + endpoint, params=query, headers=header, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200:
        print 'Update processed data points: error'
        print response.text

    total_energy = 0

    query = {
        'points-end': now
    }
    endpoint = '/networks/local/objects/energy/streams/LED/points'
    response = requests.request('GET', base + endpoint, params=query, headers=header, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200:
        print 'Error reading data'
    for dict in resp['points']:
        total_energy += dict['value']*timeInterval

    print "Total energy consumption:", total_energy, "kWh"

    endpoint = '/networks/local/objects/energy/streams/total/points'
    query = {
        'points-value': total_energy,
        'points-at': now
    }
    response = requests.request('POST', base + endpoint, params=query, headers=header, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200:
        print 'Update energy data points: error'
        print response.text



def analysis(time_last_flush, t):
    if t == 2:
        max_exp = 300000
        local_time = datetime.datetime.now()
        time_7AM = time_reset(local_time).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        exposure = count_exposure(time_7AM)
        if exposure >= max_exp:
            LED_set = 0
            left_roof = 0
            right_roof = 0
            center_roof = 1
        else:
            left_roof, right_roof, center_roof = roof_config()
            if center_roof == 1:
                LED_set = 1
            else:
                LED_set = 0
        LED_energy_usage(LED_set)
    else:
        left_roof, right_roof, center_roof = roof_config()
        if center_roof == 1:
            LED_set = 1
        else:
            LED_set = 0


    flush, time_last_flush = flushing(time_last_flush)

    settings = {
        'left_roof': left_roof,
        'right_roof': right_roof,
        'center_roof': center_roof,
        'LED': LED_set,
        'flush': flush
    }

    return settings, time_last_flush