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
abseits_url = os.environ.get('ABSEITS_URL')
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

    get_full_table = session.post("https://abseits.biz/php/tools/AJAXTools.php", data="rs=GetSpieleTableFullLayer&rst=&rsrnd=1665442831994&rsargs[]=400000000205&rsargs[]=BZL&rsargs[]=0&rsargs[]=&rsargs[]=")


    # get table
    page = session.get(abseits_url)

    parsed = bs4.BeautifulSoup(page.text, "lxml")
    container = parsed.find("div", {"id": "FullLayer400000000205"})
    table = container.find("table")

    table_str = str(table)
    a = pandas.read_html(table_str)[0]

    #print(a)

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

    print("test")


if __name__ == '__main__':
    main()