#!/usr/bin/env python
# coding: utf-8


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
final_list = []


# Base URL for SEAS events
url_seas = "https://seas.yale.edu/news-events/events/"

# List of months to scrape
months = ['2024-04', '2024-05', '2024-06']
list_of_event_seas = {}
final_list = []

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
        event_link = soup_seas.find("div", {"class": "views-field-title"}).find('a')['href']
        events_for_month[event_title] = event_time
        final_list.append({'title': event_title, 'link': "seas.yale.edu" + event_link ,'date': event_time, 'department': ['seas', 'engineering', "biomedical engineering", 
              "chemical & environmental engineering", "electrical engineering", 
              "mechanical engineering", "materials science", "bme", "cee", "ee", "mems"]})


    # Store events for this month in the dictionary
    list_of_event_seas[month] = events_for_month

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
    event_link = event.find('a')['href']
    
    final_list.append({'title': event_title, 'link': "cpsc.yale.edu" + event_link, 'date': event_time, 'department': ['cs', 'computer science']})
    list_of_event_cs[event_title] = event_time


list_of_event_wc = {}

# URL for West campus events
url_wc = "https://westcampus.yale.edu/calendar/upcoming-events"
response_wc = requests.get(url_wc)
html_content_wc = response_wc.content

soup_wc = BeautifulSoup(html_content_wc, "html.parser")

# Find all event items
events = soup_wc.find_all("td", {"class": "views-field views-field-title"})
times = soup_wc.find_all("h3")


# Extract event titles and times
for event, time in zip(events, times):
    event_title = event.text.strip()
    event_time = time.text.strip()
    event_link = event.find('a')['href']
    final_list.append({'title': event_title, 'link': "westcampus.yale.edu" + event_link, 'date': event_time, 'department': ['wc', 'west campus']})
    list_of_event_wc[event_title] = event_time


list_of_event_ap = {}

# URL for Applied Physics department events
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
    event_link = event.find('a')['href']
    list_of_event_ap[event_title] = event_time
    final_list.append({'title': event_title, 'link': "appliedphysics.yale.edu" + event_link, 'date': event_time, 'department': ['ap', 'applied physics']})


# Function to convert date string to desired format
def convert_date(date_str):
    try:
        # Split the date string based on the dash (-) character and take the first part
        date_str = date_str.split(' - ')[0]
        # Parse the date string
        date_obj = datetime.strptime(date_str, '%A, %B %d, %Y') #Monday, May 20, 2024 - 2:30pm - 4:00pm
        # Format the date object to desired format
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        pass
    try:
        # Parse the date string
        date_obj = datetime.strptime(date_str, '%B %d, %Y') # April 19, 2024
        # Format the date object to desired format
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return None

# Iterate over the list and update the date format
for event in final_list:
    event['date'] = convert_date(event['date'])

# Print the updated list
for event in final_list:
    print(event)

