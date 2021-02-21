import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from dateutil import rrule
import re
import nltk

nltk.download("stopwords")
nltk.download('wordnet')
nltk.download('punkt')

JSON_PATH = "data.json"
CSV_PATH = "data.csv"
df = pd.read_csv(CSV_PATH)

# Strips links from the text
def clean(text):
    output = re.sub('<[^>]+>', '', text)
    output = output.replace("\n"," ")
    return output

df['text'] = df['text'].map(clean)

# Counts the number of items in the pandas dataframe
def count_rows():
  return df.shape[0]

# Counts the number of words in the pandas dataframe
def count_words(table='no', plot='no'):
    df['word_count'] = df['text'].apply(lambda x: len(str(x).split(" ")))
    if table == "yes":
      print(df[['text','word_count']].head())
    if plot == "yes":
      df['word_count'].plot.bar()

