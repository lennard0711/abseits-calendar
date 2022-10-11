import os
import sys
import caldav
import requests
import bs4
import pandas
from datetime import date
from datetime import datetime

# We'll try to use the local caldav library, not the system-installed
sys.path.insert(0, "..")
sys.path.insert(0, ".")

# Set calendar vars
caldav_url = os.environ.get('CALDAV_URL')
caldav_user = os.environ.get('CALDAV_USER')
caldav_password = os.environ.get('CALDAV_PASSWORD')
# Set abseits.biz vars
abseits_uid = os.environ.get('ABSEITS_UID')
abseits_kader = os.environ.get('ABSEITS_KADER')
abseits_user = os.environ.get('ABSEITS_USER')
abseits_password = os.environ.get('ABSEITS_PASSWORD')

def main():
    session = requests.Session()

    # login
    request = session.post("https://abseits.biz/php/login/loginControl.php", data={
        "login": "1",
        "username": abseits_user,
        "passwort": abseits_password,
        "OK": "Submit",
    })

    # Check if login was successful
    assert "falsch!" not in request.text

    get_full_table = session.post("https://abseits.biz/php/tools/AJAXTools.php", data=[
        ('rs', 'GetSpieleTableFullLayer'),
        ('rst', ''),
        ('rsrnd', '1665444178344'),
        ('rsargs[]', abseits_uid),
        ('rsargs[]', abseits_kader),
        ('rsargs[]', '0'),
        ('rsargs[]', ''),
        ('rsargs[]', ''),
    ])

    raw = get_full_table.text[50:-9].replace("\\", "")
    dirty_table = pandas.read_html(raw)[0]
    clean_table = dirty_table.to_string().replace("u00e4", "ä").replace("u00c4", "Ä").replace("u00fc", "ü").replace("u00dc", "Ü").replace("u00f6", "ö").replace("u00d6", "Ö").replace("u00df", "ß")

    # Initiate DAVClient object
    client = caldav.DAVClient(url=caldav_url, username=caldav_user, password=caldav_password)

    # Fetch a principal object.
    my_principal = client.principal()

    # Fetch principals calendars
    calendars = my_principal.calendars()

    # Let's try to find or create a calendar ...
    try:
        # This will raise a NotFoundError if calendar does not exist
        my_calendar = my_principal.calendar(name=os.environ.get('CALDAV_CALENDAR'))
        assert my_calendar
        # calendar did exist, probably it was made on an earlier run
        # of this script
    except caldav.error.NotFoundError:
        # Let's create a calendar
        my_calendar = my_principal.calendar(name=os.environ.get('CALDAV_CALENDAR'))

    all_events = my_calendar.events()

if __name__ == '__main__':
    main()
