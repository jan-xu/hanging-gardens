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

def count_exposure(now, time_reset, base, error=False):
    daily_exp = 0

    query = {
        'points-start': time_reset.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        'points-end': now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    endpoint = '/networks/local/objects/light_sensor/streams/center_light/points'
    response = requests.request('GET', base + endpoint, params=query, headers={}, timeout=120)
    resp = json.loads(response.text)
    if resp['points-code'] != 200:
        print 'Error reading light data'
    for dict in resp['points']:
        daily_exp += dict['value']

    print "Initial light exposure for plants today:", daily_exp, "lux*s"
