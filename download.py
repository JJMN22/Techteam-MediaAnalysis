import requests
import json
import pandas as pd
import datetime
from dateutil import rrule
import re

# Uses Guardian API. Find documentation at
# https://github.com/prabhath6/theguardian-api-python
# https://gist.github.com/dannguyen/c9cb220093ee4c12b840
# https://open-platform.theguardian.com/documentation/

GUARDIAN_KEY = "91e63133-0adb-493f-9e76-33db7e78a7d2"
API_ENDPOINT = 'http://content.guardianapis.com/search'
GUARDIAN_PARAMETERS = {
    'from-date': "2016-05-04",
    'to-date': "2020-05-04",
    'order-by': "newest",
    'show-fields': 'all',
    'page-size': 200,
    'q' : "electric AND cars AND vehicle",
    'api-key': GUARDIAN_KEY
}
JSON_PATH = 'data.json'
CSV_PATH = 'data.csv'

# downloads the data as a JSON

print("Downloading data")
all_results = []
current_page = 1
total_pages = 1
while current_page <= total_pages:
  print("...page", current_page)
  GUARDIAN_PARAMETERS['page'] = current_page
  resp = requests.get(API_ENDPOINT, GUARDIAN_PARAMETERS)
  data = resp.json()
  all_results.extend(data['response']['results'])
  # if there is more than one page
  current_page += 1
  total_pages = data['response']['pages']

  with open(JSON_PATH, 'w') as f:
    print("Writing to", JSON_PATH)
    
    # re-serialize it for pretty indentation
    f.write(json.dumps(all_results, indent=2))


# Turns the data into a CSV file
title = []
date = []
text = []
# read the JSON_PATH 
with open(JSON_PATH, 'r') as f:
  articles = json.load(f)
  for doc in articles:
    title.append(doc["webTitle"])
    text.append(doc["fields"]["body"])
    date.append(doc['webPublicationDate'])
  
# writing data into CSV file
print("Rewriting", JSON_PATH, "as CSV:", CSV_PATH)
df = {'title': title, 'date': date, 'text': text}
df = pd.DataFrame(df)
df = df.to_csv(CSV_PATH)

