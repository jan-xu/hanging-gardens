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

print(time_reset(datetime.datetime.now()).strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
print(type(time_reset(datetime.datetime.now()).strftime("%Y-%m-%dT%H:%M:%S.%fZ")))
