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
from ServerRequests import update_power, update_exposure, get_illuminance, get_water_level, get_total_energy

# Set up network details
base = 'http://127.0.0.1:5000'
interval = 0.25 # [hrs] -- time interval between sensor readings

def time_reset(time):
    hour = 7
    local_tz = pytz.timezone("America/Los_Angeles")
    delta = datetime.timedelta(1)
    if time.hour >= hour:
        time_7AM = local_tz.localize(datetime.datetime(time.year, time.month, time.day, hour, 0, 0), is_dst=None).astimezone(tz=pytz.utc) + delta
    else:
        time_7AM = local_tz.localize(datetime.datetime(time.year, time.month, time.day, hour, 0, 0), is_dst=None).astimezone(tz=pytz.utc)
    return time_7AM

def exposure_calc(exp, total):
    new_total = total + exp * interval
    return new_total

def roof_config():
    threshold = 12500 # [lux] -- illuminance threshold for utilizing natural sunlight

    # GET the most recent records of illuminances from left and right light sensors
    left_ill = get_illuminance(base, 'left_light')
    right_ill = get_illuminance(base, 'right_light')

    # Use logic to determine roof position [left, right]
    left_roof = int(right_ill >= left_ill and right_ill >= threshold)
    right_roof = int(left_ill > right_ill and left_ill >= threshold)
    if left_roof + right_roof == 0:
        center_roof = 1
    else:
        center_roof = 0

    return left_roof, right_roof, center_roof

def flushing(now, time_last_flush):
    min_waterlvl = 50 # [mm] -- distance from water level meter to water surface
    flush_interval = datetime.timedelta(1)
    delta = now - time_last_flush

    # GET the most recent records of water levels from lower and upper water level meters
    lower_waterlvl = get_water_level(base, 'lower_water_level')
    upper_waterlvl = get_water_level(base, 'upper_water_level')

    # Use logic to determine if flushing is required
    if lower_waterlvl > min_waterlvl or upper_waterlvl > min_waterlvl or delta > flush_interval:
        flush = 1
        time_last_flush = now
    else:
        flush = 0

    return flush, time_last_flush

def power_consumption(now, LED_set):
    if LED_set == 1:
        LED_kW = 0.06 # [kW] -- wattage of LED
    else:
        LED_kW = 0

    # TO-DO: ADD IF PUMP AND VALVE IS OPEN
    #        AND INCLUDE IN TOTAL POWER

    update_power(LED_kW, now, 'led_power', base, success=False)

    # Calculate total energy and update database
    total_energy = get_total_energy(now, base, interval)
    update_power(total_energy, now, 'total_energy', base, success=False)

def analysis(exposure, now, time_last_flush):
    # Add to exposure count and update database
    exposure = exposure_calc(get_illuminance(base, 'center_light'), exposure)
    update_exposure(exposure, now, base, success=False)

    # Check whether exposure is sufficient
    req_exp = 300000 # [lux*hrs] -- minimum required exposure
    if exposure >= req_exp:
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

    # Determine whether flushing is required
    flush, time_last_flush = flushing(now, time_last_flush)

    # Calculate power consumption
    power_consumption(now, LED_set)

    # Collate actuation markers in dictionary
    act_sets = {
        'left_roof': left_roof,
        'right_roof': right_roof,
        'center_roof': center_roof,
        'LED': LED_set,
        'flush': flush
    }

    return act_sets, time_last_flush, exposure
