from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from icalendar import Calendar, Event
from datetime import datetime
import pytz
import time
import json
import sys


verbose = True
total_course_count = 0
sleep_error = "Error: try setting the sleep property to a larger value"

def error(browser, message):
    try:
        browser.close()
    except:
        pass
    print(message)

    sys.exit(0)

def get_phantomjs_path():
    platform = sys.platform
    if platform == 'linux2' or platform == 'darwin':
        return "./phantomjs"
    elif platform == "win32" or platform == "cygwin":
        return "./phantomjs.exe"

def get_browser(name):
    """
    codes:
        FireFox: 'firefox'
        PhantomJS: 'headless'
    """

    # only support for FireFox and PhantomJS
    try:
        if verbose:
            print("Initalizing webdriver...")
        if name == 'firefox':
            browser = webdriver.Firefox() # Get local session of firefox
        elif name == 'headless':
            browser = webdriver.PhantomJS(get_phantomjs_path())
        browser.set_window_size(1120, 550) # necessary when using PhantomJS
    except:
        error(None, "Could not initialize " + name + "!")
    if verbose:
        print("Webdriver initialized!")
    return browser

def get_info():
    global verbose
    if verbose:
        print("Reading configurations...")
    f = open('config.json')
    data = json.loads('\n'.join([line for line in f]))

    try:
        username = data["username"]
        password = data["password"]
        browser = data["browser"]
        months = data["months"]
        sleep = data["sleep"]
        verbose = data["verbose"]
        outfile = data["outfile"]
    except:
        error(None, "Error in configuration file!")

    if verbose:
        print("Finished reading configuration file!")
    return username, password, browser,  months, sleep, outfile

def login(browser, username, password):
    if verbose:
        print("Attempting to login...")
        print("Entering UTORid and password...")
    elem = browser.find_element_by_name("user") # Find the username box
    elem.send_keys(username)

    elem = browser.find_element_by_name("pass") # Find the password box
    elem.send_keys(password + Keys.RETURN)

    success = browser.title == "ACORN"

    if verbose and success:
        print("Sucessfully logged in!")
    return success

def timetable_view(browser):
    href = "/sws/timetable/main.do?main.dispatch#/calendar"

    if verbose:
        print("Finding timetable...")
    # Find the timetable link
    elem = browser.find_elements_by_xpath("//a[@href='" + href + "']")[0]
    elem.click()

    if verbose:
        print("Timetable found!")

def list_view(browser):
    if verbose:
        print("Finding list view...")

    # Find the List view link
    for e in browser.find_elements_by_css_selector("button"):
        if e.get_attribute("innerHTML").strip() == "List":
            elem = e
            elem.click()
            break

    if verbose:
        print("List view found!")

def view(browser, username, password, sleep):
    try:
        browser.get("http://acorn.utoronto.ca") # Load page

        if not login(browser, username, password):
            error(browser, "Login error! Check your credentials")

        if verbose:
            print("Waiting for page to load...")
        time.sleep(sleep) # Allow time for page to fully load

        timetable_view(browser)

        if verbose:
            print("Waiting for page to load...")
        time.sleep(sleep) # Allow time for page to fully load

        list_view(browser)

        if verbose:
            print("Waiting for page to load...")
        time.sleep(sleep) # Allow time for page to fully load
    except IndexError:
        error(browser, sleep_error)

def get_month_year(month_year_element):
    if verbose:
        print("Finding month and year...")
    return month_year_element.get_attribute("innerHTML").strip().split(" ")

# Mapping abbreviations to expanded text
day_of_week_names = {"Sun": "Sunday",
                     "Mon": "Monday",
                     "Tue": "Tuesday",
                     "Wed": "Wednesday",
                     "Thu": "Thursday",
                     "Fri": "Friday",
                     "Sat": "Saturday"}

def get_date(day):
    if verbose:
        print("Finding date...")
    date_element = day.find_elements_by_xpath('.//div[@data-ng-bind="currentEventDate|date:\'d\'"]')[0]
    day_of_week_element = day.find_elements_by_xpath('.//div[@data-ng-bind="currentEventDate|date:\'EEE\'"]')[0]
    return date_element.get_attribute("innerHTML").strip(), day_of_week_names[day_of_week_element.get_attribute("innerHTML").strip()]

def get_course_elem(day):
    if verbose:
        print("Finding courses...")
    header = day.find_elements_by_xpath('.//div[@data-ng-bind="event.title"]')
    body = day.find_elements_by_class_name('event-body')
    return header, body

def get_calender(browser, months):
    global total_course_count
    cal = {}

    try:
        elem = browser.find_elements_by_class_name("fc-button-next")[-1]
        for i in range(months): # loop once for each month
            month_year_element = browser.find_elements_by_xpath('//h2[@data-ng-bind="currentDate|date:\'MMMM yyyy\'"]')[0]
            month, year = get_month_year(month_year_element)

            if verbose:
                print("Parsing " + month + " " + year + " calendar...")

            if year not in cal:
                cal[year] = {}
            cal[year][month] = {}

            day_elems = browser.find_elements_by_class_name('list-item-container')
            for day in day_elems:
                date, day_of_week = get_date(day)
                courses = []
                headers, bodies = get_course_elem(day)

                # Not sure why its needed, but there are some hidden elements for days that don't exist
                if not day.is_displayed():
                    continue

                course_count = len(headers)

                for i, header, body in zip(range(1, course_count + 1), headers, bodies):
                    if verbose:
                        print("\tParsing course " + str(i) + " of " + str(course_count))
                    course = {}
                    course["course_name"] = header.get_attribute("innerHTML").strip()
                    course["time"] = body.find_elements_by_class_name("event-time")[0].get_attribute("innerHTML").strip()
                    location = body.find_elements_by_class_name("event-location")[0].get_attribute("innerHTML")
                    course["location"] = location[: location.find('<')].strip()
                    course["location_details"] = body.find_elements_by_class_name("event-sub-location")[0].get_attribute("innerHTML").strip()
                    course["code"], course["section"] = body.find_elements_by_class_name("event-description")[0].get_attribute("innerHTML").strip().split(" ")
                    total_course_count += 1
                    courses.append(course)

                cal[year][month][date] = courses

            if i + 1 != months:
                elem.click()
            time.sleep(1)
    except IndexError:
        error(browser, sleep_error)


    return cal

def hour_minute(time):
    hour, minute = time.split(':')
    return int(hour.strip()), int(minute.strip())

# Mapping month name to the numeric value
month_numbers = {"January": 1,
                 "February": 2,
                 "March": 3,
                 "April": 4,
                 "May": 5,
                 "June": 6,
                 "July": 7,
                 "August": 8,
                 "September": 9,
                 "October": 10,
                 "November": 11,
                 "December": 12}

def to_ical(calendar):
    cal = Calendar()
    cal.add('prodid', '-//UofTiCal')
    cal.add('version', '2.0')

    if verbose:
        counter = 1;

    for year in calendar:
        for month in calendar[year]:
            for date in calendar[year][month]:
                for course in calendar[year][month][date]:
                    if verbose:
                        print("Creating event " + str(counter) + " of " + str(total_course_count))
                    evt = Event()
                    evt.add('summary', course["code"] + " (" + course["section"] + "): " + course["course_name"])
                    evt.add('location', course["location"] + " " + course["location_details"])
                    times = course["time"].split(' ')
                    start_hour, start_minute = hour_minute(times[0])
                    end_hour, end_minute = hour_minute(times[3])
                    evt.add('dtstart', datetime(int(year), month_numbers[month], int(date), start_hour, start_minute, tzinfo=pytz.timezone("America/Toronto")))
                    evt.add('dtend', datetime(int(year), month_numbers[month], int(date), end_hour, end_minute, tzinfo=pytz.timezone("America/Toronto")))
                    evt.add('dtstamp', datetime.now())
                    cal.add_component(evt)

    return cal

def main():
    username, password, browser_name, months, sleep, outfile = get_info()

    browser = get_browser(browser_name)

    view(browser, username, password, sleep)

    cal = get_calender(browser, months)

    ical = to_ical(cal)

    f = open(outfile, 'wb')
    if verbose:
        print("Writing data to file...")
    f.write(ical.to_ical())
    f.close()

    browser.close()

    if verbose:
        print("Finished!")

if __name__ == '__main__':
    main()
