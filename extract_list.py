from bs4 import BeautifulSoup
import requests
import pandas as pd
import statistics
import numpy as np
import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt


list_of_event = {}

# Base URL for SEAS events
url_seas = "https://seas.yale.edu/news-events/events/"

# List of months to scrape
months = ['2024-04', '2024-05', '2024-06']
list_of_event_seas = {}

for month in months:
    url = url_seas + month
    response_seas = requests.get(url)
    html_content_seas = response_seas.content

    soup_seas = BeautifulSoup(html_content_seas, "html.parser")
    events_seas = soup_seas.find_all("div", {"class": "item-list"})
    
    events_for_month = {}
    events = soup_seas.find_all("div", {"class": "views-field-title"})
    times = soup_seas.find_all("div", {"class": "views-field-field-event-time-value"})
    for event, time in zip(events, times):
        event_title = event.text.strip()
        event_time = time.text.strip()
        events_for_month[event_title] = event_time


        # Store events for this month in the dictionary
    list_of_event_seas[month] = events_for_month

    
final_list = []
# Print the events for each month
for month, events in list_of_event_seas.items():
    for event in events:
        final_list.append({'title': event, 'date': month, 'department': 'seas'})
    #print("Events for", month)
    #for event_title, event_time in events.items():
        #print(f"Event: {event_title}, Time: {event_time}")

print(final_list)
print(final_list[2])


list_of_event_cs = {}

# URL for CS department events
url_cs = "https://cpsc.yale.edu/calendar/upcoming-events"
response_cs = requests.get(url_cs)
html_content_cs = response_cs.content

soup_cs = BeautifulSoup(html_content_cs, "html.parser")

# Find all event items
events = soup_cs.find_all("td", {"class": "views-field views-field-title"})
times = soup_cs.find_all("td", {"class": "views-field views-field-field-event-time"})


# Extract event titles and times
for event, time in zip(events, times):
    event_title = event.text.strip()
    event_time = time.text.strip()
    print(event_title)
    print()
    final_list.append({'title': event_title, 'date': event_time, 'department': 'cs'})
    list_of_event_cs[event_title] = event_time

for item in final_list:
    print(item)

list_of_event_ap = {}

# URL for AP department events
url_ap = "https://appliedphysics.yale.edu/calendar"
response_ap = requests.get(url_ap)
html_content_ap = response_ap.content

soup_ap = BeautifulSoup(html_content_ap, "html.parser")

# Find all event items
events_ap = soup_ap.find_all("td", {"class": "views-field views-field-title"})
times_ap = soup_ap.find_all("td", {"class": "views-field views-field-field-event-time-1"})

# Extract event titles and times
for event, time in zip(events_ap, times_ap):
    event_title = event.text.strip()
    event_time = time.text.strip()
    list_of_event_ap[event_title] = event_time
    final_list.append({'title': event_title, 'date': event_time, 'department': 'ap'})
# fix the time
