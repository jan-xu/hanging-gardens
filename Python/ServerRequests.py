'''

University of California, Berkeley
CE 186 Design of Cyber-Physical Systems (Fall Term 2018)
Hanging Gardens: ServerRequests.py
Group 6

DESCRIPTION

'''

import requests
import json

def create_object(name, obj_id, base, error=False):
    query = {
        'object-name': name
    }
    endpoint = '/networks/local/objects/'+obj_id
    response = requests.request('PUT', base + endpoint, params=query, headers={}, timeout=120)
    resp = json.loads(response.text)
    if resp['object-code'] == 201:
        print 'Object created:', name
    elif resp['object-code'] == 405 and error:
        print 'Error: object not created (object already exists)'
    elif resp['object-code'] != 201 and error:
        print 'Error: object not created'
        print response.text

def create_stream(name, dtype, obj_id, strm_id, base, error=False):
    query = {
        'stream-name': name,
        'points-type': dtype
    }
    endpoint = '/networks/local/objects/'+obj_id+'/streams/'+strm_id
    response = requests.request('PUT', base + endpoint, params=query, headers={}, timeout=120)
    resp = json.loads(response.text)
    if resp['stream-code'] == 201:
        print 'Stream created:', name
    elif resp['stream-code'] == 405 and error:
        print 'Error: stream not created (stream already exists)'
    elif resp['stream-code'] != 201 and error:
        print 'Error: stream not created'
        print response.text

def update_point(x, time, obj_id, strm_id, base, success=True, error=False):
    query = {
        'points-value': x,
        'points-at': time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    endpoint = '/networks/local/objects/'+obj_id+'/streams/'+strm_id+'/points'
    response = requests.request('POST', base + endpoint, params=query, headers={}, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] == 200 and success:
        print 'Data point updated:', x
    elif resp['points-code'] != 200 and error:
        print 'Error: data point not updated'
        print response.text

def update_exposure(exp, time, base, success=True, error=False):
    query = {
        'points-value': exp,
        'points-at': time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    endpoint = '/networks/local/objects/exposure/streams/exposure/points'
    response = requests.request('POST', base + endpoint, params=query, headers={}, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] == 200 and success:
        print 'Light exposure updated:', exp
    elif resp['points-code'] != 200 and error:
        print 'Error: light exposure not updated'
        print response.text

def update_power(x, time, strm_id, base, success=True, error=False):
    query = {
        'points-value': x,
        'points-at': time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    endpoint = '/networks/local/objects/energy/streams/'+strm_id+'/points'
    response = requests.request('POST', base + endpoint, params=query, headers={}, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] == 200 and success:
        print 'Power consumption updated:', exp
    elif resp['points-code'] != 200 and error:
        print 'Error: power consumption not updated'
        print response.text

def get_illuminance(base, strm_id, error=False):
    query = {
        'points-limit': 1
    }

    endpoint = '/networks/local/objects/light_sensor/streams/'+strm_id+'/points'
    response = requests.request('GET', base + endpoint, params=query, headers={}, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200 and error:
        print 'Error reading illuminance data from left light sensor'
    ill = resp['points'][0]['value']

    return ill

def get_water_level(base, strm_id, error=False):
    query = {
        'points-limit': 1
    }

    # Water level meter
    endpoint = '/networks/local/objects/water_level_meter/streams/'+strm_id+'/points'
    response = requests.request('GET', base + endpoint, params=query, headers={}, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200 and error:
        print 'Error reading water level data from lower rack'
    waterlvl = resp['points'][0]['value']

    return waterlvl

def get_total_energy(now, base, interval, error=False):
    total_energy = 0

    # LED energy
    query = {
        'points-end': now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    endpoint = '/networks/local/objects/energy/streams/led_power/points'
    response = requests.request('GET', base + endpoint, params=query, headers={}, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200 and error:
        print 'Error reading LED energy data'
    for dict in resp['points']:
        total_energy += dict['value']*interval

    # Pump energy

    # Valve energy

    print "Total energy consumption since start:", total_energy, "kWh"
    return total_energy

def get_exposure(exp_reset_time_today, base, error=False):
    exposure = 0

    query = {
        'points-start': exp_reset_time_today.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        'points-limit': 1
    }
    endpoint = '/networks/local/objects/exposure/streams/exposure/points'
    response = requests.request('GET', base + endpoint, params=query, headers={}, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200 and error:
        print 'Error reading exposure data'
    if resp['points'] != []:
        exposure = resp['points'][0]['value']

    print "Initial light exposure for plants today:", exposure, "lux*hours"
    print ""

    return exposure
