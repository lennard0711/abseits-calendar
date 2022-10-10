import os
import sys
from datetime import date
from datetime import datetime

## We'll try to use the local caldav library, not the system-installed
sys.path.insert(0, "..")
sys.path.insert(0, ".")

import caldav

## Set calendar vars
caldav_url = os.environ.get('CALDAV_URL')
username = os.environ.get('CALDAV_USER')
password = os.environ.get('CALDAV_PASSWORD')

## Initiate DAVClient object
client = caldav.DAVClient(url=caldav_url, username=username, password=password)

## Fetch a principal object.
my_principal = client.principal()

## Fetch principals calendars
calendars = my_principal.calendars()

## Let's try to find or create a calendar ...
try:
    ## This will raise a NotFoundError if calendar does not exist
    my_calendar = my_principal.calendar(name=os.environ.get('CALDAV_CALENDAR'))
    assert my_calendar
    ## calendar did exist, probably it was made on an earlier run
    ## of this script
except caldav.error.NotFoundError:
    ## Let's create a calendar
    my_calendar = my_principal.calendar(name=os.environ.get('CALDAV_CALENDAR'))

all_events = my_calendar.events()

print("test")