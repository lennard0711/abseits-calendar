import os
import sys
import re
import caldav
import requests
import bs4
import pandas as pd
import time
from datetime import date, datetime, timedelta

# Get caldav vars from system environment variables set by Docker
caldav_url = os.environ.get('CALDAV_URL')
caldav_user = os.environ.get('CALDAV_USER')
caldav_password = os.environ.get('CALDAV_PASSWORD')
# Get abseits.biz vars from system environment variables set by Docker
abseits_uid = os.environ.get('ABSEITS_UID')
abseits_kader = os.environ.get('ABSEITS_KADER')
abseits_user = os.environ.get('ABSEITS_USER')
abseits_password = os.environ.get('ABSEITS_PASSWORD')
# Create unix timestamp in ms for the AJAX request
unix_time = round(time.time() * 1000)


def main():
    session = requests.Session()

    # Login to abseits.biz 
    request = session.post("https://abseits.biz/php/login/loginControl.php", data={
        "login": "1",
        "username": abseits_user,
        "passwort": abseits_password,
        "OK": "Submit",
    })

    # Check if the login was successful
    assert "falsch!" not in request.text

    # get the table with all games
    get_full_table = session.post("https://abseits.biz/php/tools/AJAXTools.php", data=[
        ('rs', 'GetSpieleTableFullLayer'),
        ('rst', ''),
        ('rsrnd', unix_time),
        ('rsargs[]', abseits_uid),
        ('rsargs[]', abseits_kader),
        ('rsargs[]', '0'),
        ('rsargs[]', ''),
        ('rsargs[]', ''),
    ])

    # Get the data from abseits.biz, clean it up and put it in a pandas dataframe
    raw = get_full_table.text[50:-9].replace("u00e4", "ä").replace("u00c4", "Ä").replace("u00fc", "ü").replace("u00dc", "Ü").replace("u00f6", "ö").replace("u00d6", "Ö").replace("u00df", "ß").replace("\\", "")
    clean_html = re.sub("\(Spielort:\s[^)]*\)", "", raw)
    df = pd.read_html(clean_html, header=[0])[0]
    df = df[["Datum", "Liga", "Paarung"]]

    # Initiate DAVClient object
    client = caldav.DAVClient(url=caldav_url, username=caldav_user, password=caldav_password)

    # Fetch a principal object
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
        exit()

    ##
    ## Here happens the actual work
    ##

    # iterrate through all rows in the dataframe
    for row in df.itertuples(index=False):
        # create datetime object with match time start from coloumn 0 of each row
        match_time = datetime.strptime(row[0], "%d.%m.%Y (%H:%M)")
        # each event should start 2 hours before the match time
        event_start = match_time + timedelta(hours=-2)
        # each event should end 3 hours after match time
        event_end = match_time + timedelta(hours=3)
        # the event name should consist of the league in coloumn 2 and the matchup in coloumn 3
        event_name = row[1] + " | " + row[2]

        # check all events during the event timeframe
        events_fetched = my_calendar.date_search(
            start=event_start, end=event_end, expand=True
        )

        # Initialize variable event_exist for later
        event_exist = False

        # Check all events in our timeframe and compare the summary
        for event in events_fetched:
            found_event = event.icalendar_instance.subcomponents[0]["summary"]
            if found_event == event_name:
                # If the found event equals the summary of our event set event_exist to True
                event_exist = True

        # Id the event exist, continue with our for-loop.
        # Else create our event
        if event_exist == True:
            continue
        else:
            print("Create event " + event_name)
            create_event = my_calendar.save_event(
                dtstart=event_start,
                dtend=event_end,
                summary=event_name,
            )

if __name__ == '__main__':
    # We're in Docker, so run forever but only every 30min (1800s)
    while True:
        main()
        time.sleep(1800)
